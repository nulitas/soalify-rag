import os
from fastapi import APIRouter, BackgroundTasks, UploadFile, File, Form, HTTPException, Depends, status
from fastapi.responses import JSONResponse, FileResponse 
from typing import List, Optional
import shutil
import time

from langchain_chroma import Chroma

from database import get_db
import models
import schemas
from auth import get_current_active_user

from utils import (
    query_rag,
    get_embedding_function,
    process_documents,
)

from rag_core import (direct_llm_questions, get_available_documents)
from schemas import QueryRequest

from var import (
    DATA_PATH,
    CHROMA_PATH
)

router = APIRouter(prefix="/database", tags=["RAG"])

questions_router = APIRouter(prefix="/questions", tags=["Question Generation"])

@router.get("/documents")
async def get_database_documents(
    current_user: models.User = Depends(get_current_active_user)
):
    start_time = time.time()
    try:
        documents = get_available_documents()
        
        end_time = time.time()
        print(f"Execution time: {end_time - start_time:.4f} seconds")

        return {
            "document_sources": documents
        }
    except Exception as e:
        print(f"Error getting database documents: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting database documents: {str(e)}"
        )

@router.get("/document-count")
async def get_document_count(
    current_user: models.User = Depends(get_current_active_user)
):
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
        print(f"Document count: {len(items['ids'])}, Execution time: {end_time - start_time:.4f} seconds")

        return {
            "document_count": len(items["ids"])
        }
    except Exception as e:
        print(f"Error getting document count: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting document count: {str(e)}"
        )

@router.post("/upload-documents")
async def upload_documents(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    current_user: models.User = Depends(get_current_active_user)
):

    if current_user.role_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to upload documents."
        )

    start_time = time.time()
    uploaded_files = []
    try:
        os.makedirs(DATA_PATH, exist_ok=True)

        for file in files:
            file_path = os.path.join(DATA_PATH, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            uploaded_files.append(file.filename)

            background_tasks.add_task(process_documents, file.filename)

        end_time = time.time()
        execution_time = end_time - start_time

        return {
            "message": f"Admin {current_user.email} uploaded {len(files)} files. Processing started.",
            "filenames": uploaded_files,
            "execution_time": execution_time
        }
    except Exception as e:
        print(f"Error uploading documents by admin {current_user.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading documents: {str(e)}"
        )

@router.delete("/source/{source_filename}")
async def delete_documents_by_source(
    source_filename: str,
    current_user: models.User = Depends(get_current_active_user)
):
    if current_user.role_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete documents."
        )

    try:
        if not os.path.exists(CHROMA_PATH):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Database does not exist")

        db = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=get_embedding_function()
        )

        items = db.get(include=["metadatas"]) 

        ids_to_delete = []
        for i, metadata in enumerate(items["metadatas"]):
            if metadata and "source" in metadata and os.path.basename(metadata["source"]) == source_filename:
                ids_to_delete.append(items["ids"][i])

        if not ids_to_delete:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No documents found with source filename: '{source_filename}'"
            )

        db.delete(ids=ids_to_delete)
        
        file_path = os.path.join(DATA_PATH, source_filename)
        file_deleted = False
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                file_deleted = True
                print(f"Successfully deleted physical file: {source_filename}")
            except Exception as file_error:
                print(f"Warning: Could not delete physical file {source_filename}: {file_error}")
        
        return {
            "message": f"Admin {current_user.email} successfully deleted {len(ids_to_delete)} documents from source: {source_filename}",
            "deleted_count": len(ids_to_delete),
            "file_deleted": file_deleted,
            "file_path_existed": os.path.exists(os.path.join(DATA_PATH, source_filename)) if not file_deleted else True
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting documents by admin {current_user.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting documents: {str(e)}"
        )

@router.get("/preview/{filename}")
async def get_file_preview(filename: str):
    """
    Serve PDF file for preview in browser (No authentication required)
    """
    try:
        file_path = os.path.join(DATA_PATH, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"File '{filename}' not found"
            )
        
        if not filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files can be previewed"
            )

        return FileResponse(
            file_path, 
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"inline; filename={filename}",
                "Cache-Control": "no-cache"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error serving file preview for {filename}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error serving file preview: {str(e)}"
        )

@questions_router.post("/generate")
async def generate_questions(request: QueryRequest):
    try:
        if request.use_rag:
            result = query_rag(
                request.query_text, 
                request.num_questions,
                selected_documents=getattr(request, 'selected_documents', None),
                target_learning_outcome=getattr(request, 'target_learning_outcome', None)
            )
            return {"result": result, "method": "rag"}
        else:
            result = direct_llm_questions(
                request.query_text, 
                request.num_questions,
                target_learning_outcome=getattr(request, 'target_learning_outcome', None)
            )
            return {"result": result, "method": "llm"}
    except Exception as e:
        error_msg = f"Error generating questions: {str(e)}"
        print(error_msg)
        return JSONResponse(
            status_code=500,
            content={"error": error_msg}
        )

@router.get("/document-info")
async def get_document_info(
    current_user: models.User = Depends(get_current_active_user)
):
    """Get detailed information about documents in the database"""
    try:
        if not os.path.exists(CHROMA_PATH):
            return {"documents": [], "total_chunks": 0}

        db = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=get_embedding_function()
        )

        items = db.get(include=["metadatas"])
        
        doc_info = {}
        for metadata in items["metadatas"]:
            if metadata and "source" in metadata:
                source = os.path.basename(metadata["source"])
                if source not in doc_info:
                    doc_info[source] = {
                        "filename": source,
                        "chunk_count": 0,
                        "pages": set() if "page" in metadata else None
                    }
                doc_info[source]["chunk_count"] += 1
                if "page" in metadata:
                    doc_info[source]["pages"].add(metadata["page"])

        documents = []
        for filename, info in doc_info.items():
            doc = {
                "filename": filename,
                "chunk_count": info["chunk_count"],
            }
            if info["pages"]:
                doc["page_count"] = len(info["pages"])
                doc["page_range"] = f"{min(info['pages'])}-{max(info['pages'])}"
            documents.append(doc)
        
        return {
            "documents": documents,
            "total_chunks": len(items["ids"])
        }
    except Exception as e:
        print(f"Error getting document info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting document info: {str(e)}"
        )