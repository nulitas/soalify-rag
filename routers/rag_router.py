import os
from fastapi import APIRouter, BackgroundTasks, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Optional
import shutil
import time

from langchain_chroma import Chroma

from utils import (
    query_rag, 
    get_embedding_function, 
    process_documents,
    direct_llm_questions
)
from var import (
    DATA_PATH, 
    CHROMA_PATH
)
from schemas import QueryRequest

router = APIRouter(prefix="/database", tags=["RAG"])

questions_router = APIRouter(prefix="/questions", tags=["Question Generation"])

@router.get("/documents")
async def get_database_documents():
    start_time = time.time()
    try:
        if not os.path.exists(CHROMA_PATH):
            return {"document_sources": []}
        
        db = Chroma(
            persist_directory=CHROMA_PATH, 
            embedding_function=get_embedding_function()
        )
        
        items = db.get(include=["metadatas"])
        
        sources = set()
        for metadata in items["metadatas"]:
            if metadata and "source" in metadata:
                sources.add(os.path.basename(metadata["source"]))
        
        end_time = time.time()
        print(f"Execution time: {end_time - start_time:.4f} seconds")
        
        return {
            "document_sources": list(sources)
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error getting database status: {str(e)}"}
        )

@router.get("/document-count")
async def get_document_count():
    start_time = time.time()
    try:
        if not os.path.exists(CHROMA_PATH):
            return {"document_count": 0}
        
        db = Chroma(
            persist_directory=CHROMA_PATH, 
            embedding_function=get_embedding_function()
        )
        
        items = db.get()
        
        end_time = time.time()
        print(f"Execution time: {end_time - start_time:.4f} seconds")

        return {
            "document_count": len(items["ids"])
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error getting document count: {str(e)}"}
        )

@router.post("/upload-documents")
async def upload_documents(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...)
):
    start_time = time.time()
    uploaded_files = []
    try:
        for file in files:
            file_path = os.path.join(DATA_PATH, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            uploaded_files.append(file.filename)
            
            background_tasks.add_task(process_documents, file.filename)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        return {
            "message": f"Uploaded {len(files)} files and started processing. Files will be automatically deleted after processing.",
            "filenames": uploaded_files,
            "execution_time": execution_time
        }
    except Exception as e:
        end_time = time.time()
        execution_time = end_time - start_time
        return JSONResponse(
            status_code=500,
            content={
                "error": f"Error uploading documents: {str(e)}",
                "execution_time": execution_time
            }
        )

@router.delete("/source/{source_filename}")
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

@questions_router.post("/generate")
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