import shutil
import os
import time

from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from passlib.context import CryptContext

from langchain_ollama import OllamaLLM
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate

from sqlalchemy.orm import Session
from database import engine, get_db
import models

models.Base.metadata.create_all(bind=engine)

from utils import (
    query_rag, 
    get_embedding_function, 
    get_prompt_template,
    get_similarity_search,
    direct_llm_questions,
    calculate_chunk_ids,
    process_documents
)

from var import (
    DATA_PATH, 
    CHROMA_PATH, 
    OLLAMA_MODEL, 
    URL_PATH
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[URL_PATH],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(DATA_PATH, exist_ok=True)


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# Pydantic models
class UserCreate(BaseModel):
    email: str
    password: str
    role_id: int = 1  

class UserResponse(BaseModel):
    user_id: int
    email: str
    role_id: int
    
    class Config:
        orm_mode = True

class TagCreate(BaseModel):
    tag_name: str

class TagResponse(BaseModel):
    tag_id: int
    tag_name: str
    
    class Config:
        orm_mode = True

class PackageCreate(BaseModel):
    package_name: str
    questions: Optional[str] = None
    tag_ids: List[int] = []

class PackageResponse(BaseModel):
    package_id: int
    package_name: str
    questions: Optional[str] = None
    user_id: int
    tags: List[TagResponse] = []
    
    class Config:
        orm_mode = True

class QueryRequest(BaseModel):
    query_text: str
    num_questions: int = 1
    use_rag: bool = True


# API routes
@app.post("/tags/", response_model=TagResponse)
async def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    db_tag = db.query(models.Tag).filter(models.Tag.tag_name == tag.tag_name).first()
    if db_tag:
        raise HTTPException(status_code=400, detail="Tag already exists")
    db_tag = models.Tag(tag_name=tag.tag_name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

@app.get("/tags/", response_model=List[TagResponse])
async def get_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tags = db.query(models.Tag).offset(skip).limit(limit).all()
    return tags

@app.post("/packages/", response_model=PackageResponse)
async def create_package(package: PackageCreate, db: Session = Depends(get_db), user_id: int = 1):
    db_package = models.QuestionPackage(
        package_name=package.package_name,
        questions=package.questions,
        user_id=user_id
    )
    
    if package.tag_ids:
        tags = db.query(models.Tag).filter(models.Tag.tag_id.in_(package.tag_ids)).all()
        db_package.tags = tags
    
    db.add(db_package)
    db.commit()
    db.refresh(db_package)
    return db_package

@app.get("/packages/", response_model=List[PackageResponse])
async def get_packages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    packages = db.query(models.QuestionPackage).offset(skip).limit(limit).all()
    return packages

@app.get("/packages/{package_id}", response_model=PackageResponse)
async def get_package(package_id: int, db: Session = Depends(get_db)):
    db_package = db.query(models.QuestionPackage).filter(models.QuestionPackage.package_id == package_id).first()
    if db_package is None:
        raise HTTPException(status_code=404, detail="Package not found")
    return db_package

@app.put("/packages/{package_id}", response_model=PackageResponse)
async def update_package(
    package_id: int,
    package: PackageCreate,
    db: Session = Depends(get_db)
):
    db_package = db.query(models.QuestionPackage).filter(models.QuestionPackage.package_id == package_id).first()
    if db_package is None:
        raise HTTPException(status_code=404, detail="Package not found")
    
    db_package.package_name = package.package_name
    if package.questions is not None:
        db_package.questions = package.questions
    
    if package.tag_ids:
        tags = db.query(models.Tag).filter(models.Tag.tag_id.in_(package.tag_ids)).all()
        db_package.tags = tags
    
    db.commit()
    db.refresh(db_package)
    return db_package

@app.delete("/packages/{package_id}")
async def delete_package(package_id: int, db: Session = Depends(get_db)):
    db_package = db.query(models.QuestionPackage).filter(models.QuestionPackage.package_id == package_id).first()
    if db_package is None:
        raise HTTPException(status_code=404, detail="Package not found")
    
    db.delete(db_package)
    db.commit()
    return {"detail": "Package deleted successfully"}


@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, password=hashed_password, role_id=user.role_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[UserResponse])
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@app.post("/roles/")
async def create_role(role_name: str, db: Session = Depends(get_db)):
    db_role = models.Role(role_name=role_name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return {"role_id": db_role.role_id, "role_name": db_role.role_name}

@app.get("/roles/")
async def get_roles(db: Session = Depends(get_db)):
    roles = db.query(models.Role).all()
    return [{"role_id": role.role_id, "role_name": role.role_name} for role in roles]


# RAG and LLM API
@app.post("/generate-questions")
async def generate_questions(request: QueryRequest):
    try:
        if request.use_rag:
            result = query_rag(request.query_text, request.num_questions)
            return {"result": result, "method": "rag"}
        else:
            result = direct_llm_questions(request.query_text, request.num_questions)
            return {"result": result, "method": "llm"}
    except Exception as e:
        error_msg = f"Error generating questions: {str(e)}"
        print(error_msg)
        return JSONResponse(
            status_code=500,
            content={"error": error_msg}
        )

@app.get("/database/status")
async def get_database_status():
    try:
        if not os.path.exists(CHROMA_PATH):
            return {"document_count": 0, "document_sources": []}
        
        db = Chroma(
            persist_directory=CHROMA_PATH, 
            embedding_function=get_embedding_function()
        )
        items = db.get(include=["metadatas"])
        
        sources = set()
        for metadata in items["metadatas"]:
            if metadata and "source" in metadata:
                sources.add(os.path.basename(metadata["source"]))
        
        return {
            "document_count": len(items["ids"]),
            "document_ids": items["ids"],
            "document_sources": list(sources)
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error getting database status: {str(e)}"}
        )

@app.get("/database/documents")
async def list_documents():
    try:
        if not os.path.exists(CHROMA_PATH):
            return {"documents": []}
        
        db = Chroma(
            persist_directory=CHROMA_PATH, 
            embedding_function=get_embedding_function()
        )
        
        items = db.get(include=["metadatas"])
        
        documents = []
        for i, doc_id in enumerate(items["ids"]):
            doc_info = {
                "id": doc_id,
                "metadata": items["metadatas"][i] if items["metadatas"][i] else {}
            }
            documents.append(doc_info)
        
        return {"documents": documents}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error listing documents: {str(e)}"}
        )

@app.post("/database/delete")
async def delete_documents(document_ids: list[str]):
    try:
        if not os.path.exists(CHROMA_PATH):
            return JSONResponse(
                status_code=404,
                content={"error": "Database does not exist"}
            )
        
        db = Chroma(
            persist_directory=CHROMA_PATH, 
            embedding_function=get_embedding_function()
        )
        
        db.delete(ids=document_ids)
        
        return {
            "message": f"Successfully deleted {len(document_ids)} documents",
            "deleted_ids": document_ids
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error deleting documents: {str(e)}"}
        )

@app.delete("/database/document/{document_id}")
async def delete_document(document_id: str):
    try:
        if not os.path.exists(CHROMA_PATH):
            return JSONResponse(
                status_code=404,
                content={"error": "Database does not exist"}
            )
        
        db = Chroma(
            persist_directory=CHROMA_PATH, 
            embedding_function=get_embedding_function()
        )
        
        db.delete(ids=[document_id])
        
        return {
            "message": f"Successfully deleted document",
            "deleted_id": document_id
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error deleting document: {str(e)}"}
        )

@app.post("/database/reset")
async def reset_database():
    try:
        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)
        return {"message": "Database reset successfully"}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error resetting database: {str(e)}"}
        )

@app.delete("/database/source/{source_filename}")
async def delete_documents_by_source(source_filename: str):
    try:
        if not os.path.exists(CHROMA_PATH):
            return JSONResponse(
                status_code=404,
                content={"error": "Database does not exist"}
            )
        
        db = Chroma(
            persist_directory=CHROMA_PATH, 
            embedding_function=get_embedding_function()
        )
        
        items = db.get(include=["metadatas"])
        
        source_path = f"data\\{source_filename}"  
        ids_to_delete = []
        
        for i, metadata in enumerate(items["metadatas"]):
            if metadata and "source" in metadata and metadata["source"] == source_path:
                ids_to_delete.append(items["ids"][i])
        
        if not ids_to_delete:
            return JSONResponse(
                status_code=404,
                content={"error": f"No documents found with source: {source_filename}"}
            )
        
        db.delete(ids=ids_to_delete)
        
        return {
            "message": f"Successfully deleted {len(ids_to_delete)} documents from source: {source_filename}",
            "deleted_count": len(ids_to_delete),
            "deleted_ids": ids_to_delete
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error deleting documents: {str(e)}"}
        )

@app.post("/database/upload-documents")
async def upload_documents(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    reset_db: Optional[bool] = Form(False)
):
    try:
        for file in files:
            file_path = os.path.join(DATA_PATH, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        
        background_tasks.add_task(process_documents, reset_db)
        
        return {
            "message": f"Uploaded {len(files)} files and started processing",
            "filenames": [file.filename for file in files]
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error uploading documents: {str(e)}"}
        )


@app.post("/populate-database")
async def populate_database(background_tasks: BackgroundTasks):
    background_tasks.add_task(process_documents, False)
    return {"message": "Database population started in background"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)