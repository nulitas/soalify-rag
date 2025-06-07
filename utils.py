import argparse
import time
import json
import os
import google.generativeai as genai
from typing import List, Tuple, Dict, Any, Optional
import re
from dataclasses import dataclass
from contextlib import contextmanager
import logging

from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from get_prompt_template import get_prompt_template
from get_embedding_function import get_embedding_function
from var import DATA_PATH, CHROMA_PATH, GEMINI_MODEL, GEMINI_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SearchConfig:
    """Configuration for similarity search"""
    top_k: int = 3
    chunk_size: int = 800
    chunk_overlap: int = 80
    batch_size: int = 50
    max_retries: int = 3
    timeout: int = 120

class GeminiLLM:
    """Optimized Gemini LLM wrapper with connection pooling"""
    
    def __init__(self, api_key: str, model_name: str = GEMINI_MODEL, timeout: int = 60):
        self.api_key = api_key
        self.model_name = model_name
        self.timeout = timeout
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        
        self.generation_config = genai.types.GenerationConfig(
            temperature=0.0,
            top_p=0.8,
            top_k=40
        )
        
    def _calculate_max_tokens(self, num_questions: int) -> int:
        """Calculate optimal token limit based on question count"""
        base_tokens = 1500
        tokens_per_question = 300
        return min(8192, base_tokens + (tokens_per_question * num_questions))
        
    def invoke(self, prompt: str, max_retries: int = 3, num_questions: int = 1) -> str:
        """Invoke model with exponential backoff retry"""
        max_tokens = self._calculate_max_tokens(num_questions)
        self.generation_config.max_output_tokens = max_tokens
        
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(
                    prompt,
                    generation_config=self.generation_config
                )
                
                if response.text:
                    return response.text.strip()
                else:
                    raise Exception("Empty response from Gemini API")
                    
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  
                else:
                    raise Exception(f"Gemini API error after {max_retries} attempts: {str(e)}")

class ChromaDBManager:
    """Manage ChromaDB operations with connection reuse"""
    
    def __init__(self, persist_directory: str, embedding_function):
        self.persist_directory = persist_directory
        self.embedding_function = embedding_function
        self._db = None
        
    @property
    def db(self):
        """Lazy-load database connection"""
        if self._db is None:
            self._db = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embedding_function
            )
        return self._db
        
    def get_collection_count(self) -> int:
        """Get total number of documents in collection"""
        try:
            return self.db._collection.count()
        except Exception as e:
            logger.error(f"Error getting collection count: {e}")
            return 0
            
    def search_with_filters(self, query_text: str, top_k: int, 
                          selected_documents: Optional[List[str]] = None) -> List[Tuple[Document, float]]:
        """Perform similarity search with optional document filtering"""
        collection_count = self.get_collection_count()
        if collection_count == 0:
            logger.warning("No documents found in ChromaDB collection")
            return []
            
        try:
            if selected_documents:
                return self._filtered_search(query_text, top_k, selected_documents, collection_count)
            else:
                return self._regular_search(query_text, min(top_k, collection_count))
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return self._fallback_search(query_text)
            
    def _filtered_search(self, query_text: str, top_k: int, 
                        selected_documents: List[str], collection_count: int) -> List[Tuple[Document, float]]:
        """Search within selected documents only"""
        all_results = self.db.similarity_search_with_score(query_text, k=collection_count)
        
        filtered_results = [
            (doc, score) for doc, score in all_results
            if os.path.basename(doc.metadata.get('source', '')) in selected_documents
        ]
        
        if not filtered_results:
            logger.warning(f"No results found in selected documents: {selected_documents}")
            return []
            
        logger.info(f"Found {len(filtered_results[:top_k])} results from selected documents")
        return filtered_results[:top_k]
        
    def _regular_search(self, query_text: str, k: int) -> List[Tuple[Document, float]]:
        """Regular similarity search"""
        return self.db.similarity_search_with_score(query_text, k=k)
        
    def _fallback_search(self, query_text: str) -> List[Tuple[Document, float]]:
        """Fallback search method when primary search fails"""
        try:
            logger.info("Using fallback search method")
            docs = self.db.similarity_search(query_text, k=1)
            return [(doc, 0.0) for doc in docs]
        except Exception as e:
            logger.error(f"Fallback search failed: {e}")
            return []

class JSONParser:
    """Utility class for parsing JSON from LLM responses"""
    
    @staticmethod
    def parse_json_from_llm_response(response_text: str) -> Dict[str, Any]:
        """Extract and parse JSON from LLM response with multiple strategies"""
        strategies = [
            JSONParser._try_direct_parse,
            JSONParser._try_markdown_parse,
            JSONParser._try_bracket_extraction,
            JSONParser._try_repair_parse
        ]
        
        for strategy in strategies:
            try:
                result = strategy(response_text)
                if result:
                    return result
            except Exception:
                continue
                
        logger.error("Failed to parse JSON from LLM response")
        return JSONParser._create_error_response(response_text)
    
    @staticmethod
    def _try_direct_parse(response_text: str) -> Optional[Dict]:
        """Try direct JSON parsing"""
        return json.loads(response_text.strip())
    
    @staticmethod
    def _try_markdown_parse(response_text: str) -> Optional[Dict]:
        """Try parsing JSON from markdown code blocks"""
        json_match = re.search(r'```json\s*\n(.*?)\n```', response_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1).strip())
        return None
    
    @staticmethod
    def _try_bracket_extraction(response_text: str) -> Optional[Dict]:
        """Try extracting JSON by bracket matching"""
        start_idx = response_text.find('{')
        if start_idx == -1:
            return None
            
        brace_count = 0
        for i, char in enumerate(response_text[start_idx:], start_idx):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    return json.loads(response_text[start_idx:i+1])
        return None
    
    @staticmethod
    def _try_repair_parse(response_text: str) -> Optional[Dict]:
        """Try repairing and parsing incomplete JSON"""
        start_idx = response_text.find('{')
        if start_idx == -1:
            return None
            
        json_part = response_text[start_idx:]
        
        open_braces = json_part.count('{') - json_part.count('}')
        open_brackets = json_part.count('[') - json_part.count(']')
        
        quote_count = json_part.count('"') - json_part.count('\\"')
        
        repaired = json_part
        if quote_count % 2 == 1:
            repaired += '"'
        repaired += ']' * open_brackets + '}' * open_braces
        
        return json.loads(repaired)
    
    @staticmethod
    def _create_error_response(response_text: str) -> Dict[str, Any]:
        """Create error response when JSON parsing fails"""
        return {
            "questions": [],
            "metadata": {
                "count": 0,
                "status": "error",
                "message": "Failed to parse JSON from LLM response",
                "raw_response": response_text[-500:] if len(response_text) > 500 else response_text
            }
        }

class DocumentProcessor:
    """Handle document processing and chunking"""
    
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
        """Load documents from PDF file"""
        document_loader = PyPDFDirectoryLoader(os.path.dirname(file_path))
        documents = [doc for doc in document_loader.load() 
                    if doc.metadata['source'].endswith(filename)]
        
        if not documents:
            logger.error(f"No documents loaded from {filename}")
            
        return documents
        
    def _create_chunks(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap,
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
        """Clean up file after processing error"""
        try:
            file_path = os.path.join(DATA_PATH, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Deleted file after processing error: {filename}")
        except Exception as e:
            logger.error(f"Failed to delete file {filename}: {e}")

def get_similarity_search(query_text: str, embedding_function, top_k: int = 3,
                         selected_documents: Optional[List[str]] = None) -> List[Tuple[Document, float]]:
    """Enhanced similarity search with improved performance"""
    start_time = time.time()
    
    db_manager = ChromaDBManager(CHROMA_PATH, embedding_function)
    results = db_manager.search_with_filters(query_text, top_k, selected_documents)
    
    logger.info(f"Similarity search took {time.time() - start_time:.2f} seconds")
    return results

def get_available_documents() -> List[str]:
    """Get list of available document sources"""
    try:
        if not os.path.exists(CHROMA_PATH):
            return []

        db_manager = ChromaDBManager(CHROMA_PATH, get_embedding_function())
        items = db_manager.db.get(include=["metadatas"])
        
        sources = {os.path.basename(metadata["source"]) 
                  for metadata in items["metadatas"] 
                  if metadata and "source" in metadata}

        return sorted(list(sources))
    except Exception as e:
        logger.error(f"Error getting available documents: {e}")
        return []

def parse_json_from_llm_response(response_text: str) -> Dict[str, Any]:
    """Parse JSON from LLM response - delegates to JSONParser"""
    return JSONParser.parse_json_from_llm_response(response_text)

def query_rag(query_text: str, num_questions: int = 1, embedding_function=None, 
              model=None, selected_documents: Optional[List[str]] = None) -> Dict[str, Any]:
    """Main RAG query function with improved error handling"""
    
    if embedding_function is None:
        embedding_function = get_embedding_function()
    
    if model is None:
        model = GeminiLLM(api_key=GEMINI_API_KEY, model_name=GEMINI_MODEL, timeout=120)

    try:
        start_time = time.time()
        
        results = get_similarity_search(query_text, embedding_function, selected_documents=selected_documents)
        
        if not results:
            return _create_no_results_response(selected_documents)
            
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])
        response_text = _generate_llm_response(context_text, num_questions, model)
        
        logger.info(f"Total RAG query took {time.time() - start_time:.2f} seconds")
        
        # Parse and enhance response
        json_output = parse_json_from_llm_response(response_text)
        _enhance_metadata(json_output, selected_documents, results)
        
        return json_output
    
    except Exception as e:
        logger.error(f"Error in RAG query: {e}")
        return _create_error_response(str(e), selected_documents)

def direct_llm_questions(query_text: str, num_questions: int = 1) -> Dict[str, Any]:
    """Generate questions directly from LLM without RAG"""
    try:
        start_time = time.time()
        
        model = GeminiLLM(api_key=GEMINI_API_KEY, model_name=GEMINI_MODEL, timeout=120)

        prompt_template_str = get_prompt_template(num_questions).replace(
            "Konteks Dokumen:\n{context}", 
            f"Buat pertanyaan dan jawaban tentang topik: \"{query_text}\""
        )

        prompt_template = ChatPromptTemplate.from_template(prompt_template_str)
        enhanced_prompt = prompt_template.format(
            query_text=query_text, 
            num_questions=num_questions
        ) + "\n\nIMPORTANT: Please ensure your response is complete and valid JSON."
        
        response_text = model.invoke(enhanced_prompt, num_questions=num_questions)
        
        logger.info(f"Direct LLM generation took {time.time() - start_time:.2f} seconds")
        
        return parse_json_from_llm_response(response_text)
    
    except Exception as e:
        logger.error(f"Error generating direct questions: {e}")
        return _create_error_response(f"Error in making the question: {str(e)}")

def process_documents(filename: str):
    """Process documents using DocumentProcessor"""
    config = SearchConfig()
    processor = DocumentProcessor(config)
    processor.process_documents(filename)

def reset_chroma_db() -> bool:
    """Reset ChromaDB database"""
    try:
        import shutil
        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)
            logger.info(f"Deleted corrupted ChromaDB at {CHROMA_PATH}")
        
        ChromaDBManager(CHROMA_PATH, get_embedding_function())
        logger.info("Created new ChromaDB database")
        return True
    except Exception as e:
        logger.error(f"Error resetting ChromaDB: {e}")
        return False

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

def _create_error_response(error_message: str, selected_documents: Optional[List[str]] = None) -> Dict[str, Any]:
    """Create error response"""
    return {
        "questions": [],
        "metadata": {
            "count": 0,
            "status": "error",
            "message": error_message,
            "selected_documents": selected_documents
        }
    }

def _generate_llm_response(context_text: str, num_questions: int, model: GeminiLLM) -> str:
    """Generate LLM response with context"""
    prompt_template_str = get_prompt_template(num_questions)
    prompt_template = ChatPromptTemplate.from_template(prompt_template_str)
    
    enhanced_prompt = prompt_template.format(
        context=context_text, 
        num_questions=num_questions
    ) + "\n\nIMPORTANT: Please ensure your response is complete and valid JSON."

    return model.invoke(enhanced_prompt, num_questions=num_questions)

def _enhance_metadata(json_output: Dict[str, Any], selected_documents: Optional[List[str]], 
                     results: List[Tuple[Document, float]]):
    """Enhance JSON output with metadata"""
    if "metadata" not in json_output:
        json_output["metadata"] = {}
        
    json_output["metadata"]["selected_documents"] = selected_documents
    json_output["metadata"]["sources_used"] = list(set([
        os.path.basename(doc.metadata.get('source', '')) 
        for doc, _ in results
    ]))

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