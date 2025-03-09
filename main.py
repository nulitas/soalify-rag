import shutil
import os
import time

from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional

from langchain_ollama import OllamaLLM
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate

from utils import (
    query_rag, 
    get_embedding_function, 
    extract_questions_and_answers,
    get_prompt_template,
    get_similarity_search,
    direct_llm_questions,
    OLLAMA_MODEL,
    CHROMA_PATH,
    DATA_PATH,
    URL_PATH,
    TIMEOUT
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

class QueryRequest(BaseModel):
    query_text: str
    num_questions: int = 1
    use_rag: bool = True

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
            "document_sources": list(sources)
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error getting database status: {str(e)}"}
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

def calculate_chunk_ids(chunks):
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0
            
        chunk.metadata["id"] = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

    return chunks

def process_documents(reset_db: bool = False):
    try:
        if reset_db and os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)
        
        document_loader = PyPDFDirectoryLoader(DATA_PATH)
        documents = document_loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=80,
            length_function=len,
            is_separator_regex=False,
        )
        chunks = text_splitter.split_documents(documents)
        
        db = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=get_embedding_function()
        )
        
        chunks_with_ids = calculate_chunk_ids(chunks)
        
        existing_items = db.get(include=[])
        existing_ids = set(existing_items["ids"])
        
        new_chunks = [chunk for chunk in chunks_with_ids 
                     if chunk.metadata["id"] not in existing_ids]
        
        if new_chunks:
            db.add_documents(new_chunks)
            print(f"Added {len(new_chunks)} new chunks to database")
        else:
            print("No new chunks to add")
            
    except Exception as e:
        print(f"Error processing documents: {e}")

@app.post("/populate-database")
async def populate_database(background_tasks: BackgroundTasks):
    background_tasks.add_task(process_documents, False)
    return {"message": "Database population started in background"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)