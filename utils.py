import argparse
import time
import json
import os
import google.generativeai as genai
from typing import List, Tuple, Dict, Any
import re

from langchain_chroma import Chroma

from langchain.prompts import ChatPromptTemplate
from langchain_core.documents import Document

from get_prompt_template import get_prompt_template
from get_embedding_function import get_embedding_function

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from var import ( DATA_PATH, CHROMA_PATH, GEMINI_MODEL, GEMINI_API_KEY)


class GeminiLLM:
    def __init__(self, api_key: str, model_name: str = GEMINI_MODEL, timeout: int = 60):
        self.api_key = api_key
        self.model_name = model_name
        self.timeout = timeout
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        
    def invoke(self, prompt: str, max_retries: int = 3, num_questions: int = 1) -> str:
        base_tokens = 1500  
        tokens_per_question = 300  
        max_tokens = min(8192, base_tokens + (tokens_per_question * num_questions))
        
        for attempt in range(max_retries):
            try:
                generation_config = genai.types.GenerationConfig(
                    temperature=0.0,
                    max_output_tokens=max_tokens,
                    top_p=0.8,
                    top_k=40
                )

                response = self.model.generate_content(
                    prompt,
                    generation_config=generation_config
                )
                
                if response.text:
                    return response.text.strip()
                else:
                    raise Exception("Empty response from Gemini API")
                    
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2)  
                else:
                    raise Exception(f"Gemini API error after {max_retries} attempts: {str(e)}")


def get_similarity_search(
    query_text: str, 
    embedding_function, 
    top_k: int = 3
) -> List[Tuple[Document, float]]:
    try:
        start_time = time.time()
        
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        
        collection_count = db._collection.count()
        if collection_count == 0:
            print("No documents found in ChromaDB collection")
            return []
        
        actual_k = min(top_k, collection_count)
        
        try:
            results = db.similarity_search_with_score(query_text, k=actual_k)
        except Exception as search_error:
            print(f"Primary search failed: {search_error}")
            
            try:
                print("Trying fallback search with k=1")
                results = db.similarity_search_with_score(query_text, k=1)
            except Exception as fallback_error:
                print(f"Fallback search also failed: {fallback_error}")
                
                try:
                    print("Using basic similarity search without scores")
                    docs = db.similarity_search(query_text, k=1)
                    results = [(doc, 0.0) for doc in docs]  
                except Exception as final_error:
                    print(f"All search methods failed: {final_error}")
                    return []
        
        print(f"Similarity search took {time.time() - start_time:.2f} seconds")
        print(f"Found {len(results)} results from {collection_count} total documents")
        return results
        
    except Exception as e:
        print(f"Error in similarity search setup: {e}")
        return []


def parse_json_from_llm_response(response_text: str) -> Dict[str, Any]:
    """Extract and parse JSON from LLM response text with better error handling."""
    
    try:
        return json.loads(response_text.strip())
    except json.JSONDecodeError:
        pass
    
    try:
        json_match = re.search(r'```json\s*\n(.*?)\n```', response_text, re.DOTALL)
        if json_match:
            json_content = json_match.group(1).strip()
            return json.loads(json_content)
    except json.JSONDecodeError:
        pass
    
    try:
        start_idx = response_text.find('{')
        if start_idx == -1:
            raise ValueError("No JSON object found")
        
        brace_count = 0
        end_idx = -1
        
        for i in range(start_idx, len(response_text)):
            if response_text[i] == '{':
                brace_count += 1
            elif response_text[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_idx = i
                    break
        
        if end_idx != -1:
            json_str = response_text[start_idx:end_idx+1]
            return json.loads(json_str)
            
    except (ValueError, json.JSONDecodeError):
        pass
    
    try:
        json_str = attempt_json_repair(response_text)
        if json_str:
            return json.loads(json_str)
    except json.JSONDecodeError:
        pass
    
    print(f"Error parsing JSON: Unterminated or malformed JSON")
    print(f"Raw response: {response_text}")
    
    return {
        "questions": [],
        "metadata": {
            "count": 0,
            "status": "error",
            "message": "Failed to parse JSON from LLM response. Response may have been truncated.",
            "raw_response": response_text[-500:] if len(response_text) > 500 else response_text
        }
    }


def attempt_json_repair(response_text: str) -> str:
    """Attempt to repair incomplete JSON by adding missing closing brackets."""
    
    start_idx = response_text.find('{')
    if start_idx == -1:
        return None
    
    json_part = response_text[start_idx:]
    
    open_braces = json_part.count('{') - json_part.count('}')
    open_brackets = json_part.count('[') - json_part.count(']')
    
    in_string = False
    escaped = False
    quote_count = 0
    
    for char in json_part:
        if escaped:
            escaped = False
            continue
        if char == '\\':
            escaped = True
            continue
        if char == '"':
            quote_count += 1
            in_string = not in_string
    
    repaired = json_part
    if in_string and quote_count % 2 == 1:
        repaired += '"'
    
    repaired += ']' * open_brackets
    repaired += '}' * open_braces
    
    return repaired


def query_rag(
    query_text: str, 
    num_questions: int = 1,
    embedding_function=None, 
    model=None
) -> Dict[str, Any]:
    if embedding_function is None:
        embedding_function = get_embedding_function()
    
    if model is None:
        model = GeminiLLM(
            api_key=GEMINI_API_KEY,
            model_name=GEMINI_MODEL,
            timeout=120  
        )

    try:
        start_time = time.time()
        results = get_similarity_search(query_text, embedding_function)
        
        if not results:
            return {
                "questions": [],
                "metadata": {
                    "count": 0,
                    "status": "error",
                    "message": "Unable to find relevant documents."
                }
            }
            
        context_text = "\n\n---\n\n".join([
            doc.page_content for doc, _score in results
        ])

        prompt_template_str = get_prompt_template(num_questions)
        prompt_template = ChatPromptTemplate.from_template(prompt_template_str)
        
        enhanced_prompt = prompt_template.format(
            context=context_text, 
            num_questions=num_questions
        ) + "\n\nIMPORTANT: Please ensure your response is complete and valid JSON. Do not truncate the response."

        response_text = model.invoke(enhanced_prompt, num_questions=num_questions)
        
        print(f"LLM generation took {time.time() - start_time:.2f} seconds")
        
        json_output = parse_json_from_llm_response(response_text)
        return json_output
    
    except Exception as e:
        print(f"Error in RAG query: {e}")
        return {
            "questions": [],
            "metadata": {
                "count": 0,
                "status": "error",
                "message": f"An error occurred in processing the query: {str(e)}"
            }
        }
    

def direct_llm_questions(query_text: str, num_questions: int = 1) -> Dict[str, Any]:
    try:
        start_time = time.time()
        
        model = GeminiLLM(
            api_key=GEMINI_API_KEY,
            model_name=GEMINI_MODEL,
            timeout=120
        )
        
        prompt_template_str = get_prompt_template(num_questions)
        
        prompt_template_str = prompt_template_str.replace(
            "Konteks Dokumen:\n{context}", 
            "Buat pertanyaan dan jawaban tentang topik: \"{query_text}\""
        )

        prompt_template = ChatPromptTemplate.from_template(prompt_template_str)
        enhanced_prompt = prompt_template.format(
            query_text=query_text, 
            num_questions=num_questions
        ) + "\n\nIMPORTANT: Please ensure your response is complete and valid JSON. Do not truncate the response."
        
        response_text = model.invoke(enhanced_prompt, num_questions=num_questions)
        
        print(f"LLM generation took {time.time() - start_time:.2f} seconds")
        
        json_output = parse_json_from_llm_response(response_text)
        return json_output
    
    except Exception as e:
        print(f"Error generating direct questions: {e}")
        return {
            "questions": [],
            "metadata": {
                "count": 0,
                "status": "error",
                "message": f"There was an error in making the question: {str(e)}"
            }
        }


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


def process_documents(filename: str):
    try:
        file_path = os.path.join(DATA_PATH, filename)
        
        if not os.path.exists(file_path):
            print(f"File {filename} not found in {DATA_PATH}")
            return
        
        document_loader = PyPDFDirectoryLoader(os.path.dirname(file_path))
        documents = [doc for doc in document_loader.load() if doc.metadata['source'].endswith(filename)]

        if not documents:
            print(f"No documents loaded from {filename}")
            return

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=80,
            length_function=len,
            is_separator_regex=False,
        )
        chunks = text_splitter.split_documents(documents)
        
        if not chunks:
            print(f"No chunks created from {filename}")
            return
        
        try:
            db = Chroma(
                persist_directory=CHROMA_PATH,
                embedding_function=get_embedding_function()
            )
        except Exception as db_error:
            print(f"Error initializing ChromaDB: {db_error}")
            return
        
        chunks_with_ids = calculate_chunk_ids(chunks)
        
        try:
            existing_items = db.get(include=[])
            existing_ids = set(existing_items["ids"]) if existing_items["ids"] else set()
        except Exception as get_error:
            print(f"Error getting existing items: {get_error}")
            existing_ids = set()  
        
        new_chunks = [chunk for chunk in chunks_with_ids 
                    if chunk.metadata["id"] not in existing_ids]
        
        if new_chunks:
            try:
                batch_size = 50
                for i in range(0, len(new_chunks), batch_size):
                    batch = new_chunks[i:i + batch_size]
                    db.add_documents(batch)
                    print(f"Added batch {i//batch_size + 1}: {len(batch)} chunks")
                
                print(f"Successfully added {len(new_chunks)} new chunks from {filename} to database")
            except Exception as add_error:
                print(f"Error adding documents to database: {add_error}")
                return
        else:
            print(f"No new chunks to add from {filename}")
        
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Successfully deleted temporary file: {filename}")
        except Exception as delete_error:
            print(f"Warning: Could not delete temporary file {filename}: {delete_error}")
            
    except Exception as e:
        print(f"Error processing document {filename}: {e}")
        try:
            file_path = os.path.join(DATA_PATH, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted temporary file after error: {filename}")
        except Exception as del_error:
            print(f"Failed to delete temporary file: {filename}, error: {str(del_error)}")


def reset_chroma_db():
    """Reset the ChromaDB database if it gets corrupted."""
    try:
        import shutil
        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)
            print(f"Deleted corrupted ChromaDB at {CHROMA_PATH}")
        
        db = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=get_embedding_function()
        )
        print("Created new ChromaDB database")
        return True
    except Exception as e:
        print(f"Error resetting ChromaDB: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="RAG Query Assistant")
    parser.add_argument("query_text", type=str, help="Query text for RAG search")
    parser.add_argument("--num_questions", type=int, default=1, 
                        help="Number of question-answer pairs to generate (default: 1)")
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