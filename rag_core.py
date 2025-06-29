import time
import json
import os
import google.generativeai as genai
from typing import List, Tuple, Dict, Any, Optional
import logging
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_core.documents import Document

from get_prompt_template import get_prompt_template
from get_embedding_function import get_embedding_function
from var import DATA_PATH, CHROMA_PATH, GEMINI_MODEL, GEMINI_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====================== JSON Parser ======================
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

# ====================== Extract Keywords ======================
def extract_primary_keyword(text: str) -> str:
    """Extract primary keyword using TF-IDF"""
    if len(text.split()) <= 2:
        return text
    
    try:
        vectorizer = TfidfVectorizer(stop_words=None, ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform([text])
        feature_names = vectorizer.get_feature_names_out()
        sorted_indices = np.argsort(tfidf_matrix.toarray()).flatten()[::-1]
        return feature_names[sorted_indices[0]]
    except Exception:
        return max(text.split(), key=len)

def keyword_match_score(doc_content: str, keyword: str) -> float:
    """Calculate keyword relevance score"""
    if not keyword or not doc_content:
        return 0.0
    
    count = doc_content.lower().count(keyword.lower())
    words = doc_content.split()
    return count / (len(words) + 1e-5)  

# ====================== Core Classes ======================
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
    """Manage ChromaDB operations with connection reuse and keyword-aware reranking"""
    
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
                          selected_documents: Optional[List[str]] = None,
                          keyword: Optional[str] = None) -> List[Tuple[Document, float]]:
        """Perform similarity search with optional document filtering and keyword reranking"""
        collection_count = self.get_collection_count()
        if collection_count == 0:
            logger.warning("No documents found in ChromaDB collection")
            return []
            
        try:
            search_k = min(collection_count, top_k * 3)
            
            if selected_documents:
                results = self._filtered_search(query_text, search_k, selected_documents, collection_count)
            else:
                results = self._regular_search(query_text, search_k)
                
            if keyword:
                results = self._keyword_reranking(results, keyword)
                
            return results[:top_k]
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return self._fallback_search(query_text)
            
    def _keyword_reranking(self, results: List[Tuple[Document, float]], keyword: str) -> List[Tuple[Document, float]]:
        """Rerank results based on keyword relevance"""
        if not results or not keyword:
            return results
            
        reranked = []
        for doc, score in results:
            k_score = keyword_match_score(doc.page_content, keyword)
            
            combined_score = (0.7 * score) + (0.3 * k_score)
            reranked.append((doc, combined_score))
        
        reranked.sort(key=lambda x: x[1], reverse=True)
        return reranked
            
    def _filtered_search(self, query_text: str, k: int, 
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
            
        logger.info(f"Found {len(filtered_results)} results from selected documents")
        return filtered_results[:k]
        
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

# ====================== Core RAG Functions ======================
def get_similarity_search(query_text: str, embedding_function, top_k: int = 5,
                         selected_documents: Optional[List[str]] = None,
                         keyword: Optional[str] = None) -> List[Tuple[Document, float]]:
    """Enhanced similarity search with keyword reranking"""
    start_time = time.time()
    
    db_manager = ChromaDBManager(CHROMA_PATH, embedding_function)
    results = db_manager.search_with_filters(
        query_text, 
        top_k, 
        selected_documents,
        keyword
    )
    
    logger.info(f"Similarity search took {time.time() - start_time:.2f} seconds")
    return results

def query_rag(query_text: str, num_questions: int = 1, embedding_function=None, 
              model=None, selected_documents: Optional[List[str]] = None,
              target_learning_outcome: Optional[str] = None) -> Dict[str, Any]:
    """Main RAG query function with keyword-aware retrieval"""
    
    if embedding_function is None:
        embedding_function = get_embedding_function()
    
    if model is None:
        model = GeminiLLM(api_key=GEMINI_API_KEY, model_name=GEMINI_MODEL, timeout=120)

    try:
        start_time = time.time()
        
        main_keyword = extract_primary_keyword(query_text)
        logger.info(f"Primary keyword extracted: {main_keyword}")
        
        results = get_similarity_search(
            query_text, 
            embedding_function, 
            top_k=10, 
            selected_documents=selected_documents,
            keyword=main_keyword
        )
        
        SIMILARITY_THRESHOLD = 0.65 
        filtered_results = [
            (doc, score) for doc, score in results 
            if score > SIMILARITY_THRESHOLD
        ]
        
        if not filtered_results:
            logger.warning("No relevant context found, using direct generation")
            return direct_llm_questions(query_text, num_questions, target_learning_outcome)
            
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in filtered_results])
        
        base_prompt = get_prompt_template(num_questions, target_learning_outcome)
        keyword_aware_prompt = (
            f"FOKUS PADA KATA KUNCI: '{main_keyword}'\n\n" +
            base_prompt
        )
        
        response_text = _generate_llm_response(
            context_text, 
            num_questions, 
            model,
            prompt_template_str=keyword_aware_prompt
        )
        
        logger.info(f"Total RAG query took {time.time() - start_time:.2f} seconds")
        
        json_output = JSONParser.parse_json_from_llm_response(response_text)
        _enhance_metadata(json_output, selected_documents, filtered_results)
        _log_rag_quality(query_text, json_output, filtered_results)  
        
        return json_output
    
    except Exception as e:
        logger.error(f"Error in RAG query: {e}")
        return _create_error_response(str(e), selected_documents)

def direct_llm_questions(query_text: str, num_questions: int = 1, 
                        target_learning_outcome: Optional[str] = None) -> Dict[str, Any]:
    """Generate questions directly from LLM with keyword focus"""
    try:
        start_time = time.time()
        
        model = GeminiLLM(api_key=GEMINI_API_KEY, model_name=GEMINI_MODEL, timeout=120)

        main_keyword = extract_primary_keyword(query_text)
        
        prompt_template_str = (
            f"FOKUS PADA KATA KUNCI: '{main_keyword}'\n\n" +
            get_prompt_template(num_questions, target_learning_outcome).replace(
                "Konteks Dokumen:\n{context}", 
                f"Buat {num_questions} pasang pertanyaan dan jawaban tentang topik: \"{query_text}\""
            )
        )

        prompt_template = ChatPromptTemplate.from_template(prompt_template_str)
        enhanced_prompt = prompt_template.format(
            query_text=query_text, 
            num_questions=num_questions
        ) + "\n\nIMPORTANT: Please ensure your response is complete and valid JSON."
        
        response_text = model.invoke(enhanced_prompt, num_questions=num_questions)
        
        logger.info(f"Direct LLM generation took {time.time() - start_time:.2f} seconds")
        
        return JSONParser.parse_json_from_llm_response(response_text)
    
    except Exception as e:
        logger.error(f"Error generating direct questions: {e}")
        return _create_error_response(f"Error in making the question: {str(e)}")
        
def _generate_llm_response(context_text: str, num_questions: int, model: GeminiLLM, 
                          prompt_template_str: str = None, 
                          target_learning_outcome: Optional[str] = None) -> str:
    """Generate LLM response with context and custom prompt"""
    if not prompt_template_str:
        prompt_template_str = get_prompt_template(num_questions, target_learning_outcome)
        
    prompt_template = ChatPromptTemplate.from_template(prompt_template_str)
    
    enhanced_prompt = prompt_template.format(
        context=context_text, 
        num_questions=num_questions
    ) + "\n\nIMPORTANT: Please ensure your response is complete and valid JSON."

    return model.invoke(enhanced_prompt, num_questions=num_questions)

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

# ====================== Helper Functions ======================
def _log_rag_quality(query_text: str, output: Dict[str, Any], 
                    context_results: List[Tuple[Document, float]]):
    """Log RAG quality metrics for continuous improvement"""
    try:
        keyword = extract_primary_keyword(query_text)
        keyword_hits = 0
        for qa in output.get("questions", []):
            if keyword.lower() in qa.get("question", "").lower():
                keyword_hits += 1
        
        context_scores = [score for _, score in context_results]
        avg_similarity = sum(context_scores) / len(context_scores) if context_scores else 0
        
        quality_metrics = {
            "query": query_text,
            "keyword": keyword,
            "keyword_coverage": keyword_hits / (len(output.get("questions", [1])) if output.get("questions") else 0),
            "avg_context_similarity": avg_similarity,
            "context_results": len(context_results),
            "generation_time": time.time(),
            "status": output.get("metadata", {}).get("status", "unknown")
        }
        
        logger.info(f"RAG_QUALITY: {json.dumps(quality_metrics)}")
    except Exception as e:
        logger.error(f"Error logging RAG quality: {e}")

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