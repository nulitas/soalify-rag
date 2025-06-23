import argparse
import json
import os
import re
import shutil
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import logging

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from rag_core import reset_chroma_db
from rag_core import query_rag
from get_embedding_function import get_embedding_function
from var import DATA_PATH, CHROMA_PATH

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====================== Configuration ======================
@dataclass
class SearchConfig:
    """Configuration for similarity search"""
    top_k: int = 5  
    chunk_size: int = 512  
    chunk_overlap: int = 128  
    batch_size: int = 50
    max_retries: int = 3
    timeout: int = 120
    keyword_threshold: float = 0.5 

# ====================== Document Processing ======================
class DocumentProcessor:
    """Handle document processing and chunking with improved parameters"""
    
    def __init__(self, config: SearchConfig):
        self.config = config
        
    def calculate_chunk_ids(self, chunks: List[Document]) -> List[Document]:
        """Calculate unique IDs for document chunks"""
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

    def process_documents(self, filename: str) -> bool:
        """Process and add documents to ChromaDB"""
        try:
            file_path = os.path.join(DATA_PATH, filename)
            
            if not os.path.exists(file_path):
                logger.error(f"File {filename} not found in {DATA_PATH}")
                return False
            
            documents = self._load_documents(file_path, filename)
            if not documents:
                return False
                
            chunks = self._create_chunks(documents)
            if not chunks:
                return False
                
            return self._add_to_database(chunks, filename)
            
        except Exception as e:
            logger.error(f"Error processing document {filename}: {e}")
            self._cleanup_file(filename)
            return False
            
    def _load_documents(self, file_path: str, filename: str) -> List[Document]:
        """Load documents from PDF file with permission handling"""
        try:
            os.makedirs(DATA_PATH, exist_ok=True)
            
            temp_dir = os.path.join(DATA_PATH, "temp_processing")
            os.makedirs(temp_dir, exist_ok=True)
            
            temp_file_path = os.path.join(temp_dir, filename)
            shutil.copy2(file_path, temp_file_path)
            
            document_loader = PyPDFDirectoryLoader(temp_dir)
            documents = [doc for doc in document_loader.load() 
                        if doc.metadata['source'].endswith(filename)]
            
            try:
                os.remove(temp_file_path)
                os.rmdir(temp_dir)
            except Exception as clean_error:
                logger.warning(f"Error cleaning temp directory: {clean_error}")
            
            if not documents:
                logger.error(f"No documents loaded from {filename}")
            
            return documents
            
        except Exception as e:
            logger.error(f"Error loading documents: {e}")
            return []
        
    def _create_chunks(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks with improved parameters"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap,
            separators=["\n\n", "\n", ". ", "? ", "! ", ", ", " ", ""], 
            length_function=len,
            is_separator_regex=False,
        )
        
        chunks = text_splitter.split_documents(documents)
        if not chunks:
            logger.error("No chunks created from documents")
            return []
            
        return self.calculate_chunk_ids(chunks)
        
    def _add_to_database(self, chunks: List[Document], filename: str) -> bool:
        """Add chunks to ChromaDB in batches"""
        try:
            from rag_core import ChromaDBManager
            db_manager = ChromaDBManager(CHROMA_PATH, get_embedding_function())
            
            existing_items = db_manager.db.get(include=[])
            existing_ids = set(existing_items["ids"]) if existing_items["ids"] else set()
            
            new_chunks = [chunk for chunk in chunks 
                         if chunk.metadata["id"] not in existing_ids]
            
            if not new_chunks:
                logger.info(f"No new chunks to add from {filename}")
                return True
                
            for i in range(0, len(new_chunks), self.config.batch_size):
                batch = new_chunks[i:i + self.config.batch_size]
                db_manager.db.add_documents(batch)
                logger.info(f"Added batch {i//self.config.batch_size + 1}: {len(batch)} chunks")
            
            logger.info(f"Successfully added {len(new_chunks)} new chunks from {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding documents to database: {e}")
            return False
            
    def _cleanup_file(self, filename: str):
        """Clean up file after processing error with permission handling"""
        try:
            file_path = os.path.join(DATA_PATH, filename)
            if os.path.exists(file_path):
                try:
                    os.chmod(file_path, 0o777)
                except:
                    pass
                    
                os.remove(file_path)
                logger.info(f"Deleted file after processing error: {filename}")
        except Exception as e:
            logger.error(f"Failed to delete file {filename}: {e}")

# ====================== Convenience Functions ======================
def process_documents(filename: str):
    """Process documents using DocumentProcessor"""
    config = SearchConfig()
    processor = DocumentProcessor(config)
    return processor.process_documents(filename)

def _create_no_results_response(selected_documents: Optional[List[str]]) -> Dict[str, Any]:
    """Create response when no results found"""
    message = "Unable to find relevant documents."
    if selected_documents:
        message += f" No relevant content found in selected documents: {', '.join(selected_documents)}"
    
    return {
        "questions": [],
        "metadata": {
            "count": 0,
            "status": "error",
            "message": message,
            "selected_documents": selected_documents
        }
    }

# ====================== CLI Main Function ======================
def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description="RAG Query Assistant")
    parser.add_argument("query_text", type=str, help="Query text for RAG search")
    parser.add_argument("--num_questions", type=int, default=1, 
                        help="Number of question-answer pairs to generate")
    parser.add_argument("--reset_db", action="store_true",
                        help="Reset the ChromaDB database")
    args = parser.parse_args()
    
    if args.reset_db:
        reset_chroma_db()
        return
    
    result = query_rag(args.query_text, args.num_questions)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()