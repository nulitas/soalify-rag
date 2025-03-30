
import argparse
import time
import json
import os

from typing import List, Tuple, Dict, Any

from langchain_chroma import Chroma

# LLM
from langchain_ollama import OllamaLLM
# from langchain_groq import ChatGroq 

# for document processing
from langchain.prompts import ChatPromptTemplate
from langchain_core.documents import Document

from get_prompt_template import get_prompt_template
from get_embedding_function import get_embedding_function

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# LLM imports
# from var import (CHROMA_PATH, GROQ_API_KEY, GROQ_MODEL, DATA_PATH)
from var import (OLLAMA_MODEL, CHROMA_PATH, DATA_PATH)


def get_similarity_search(
    query_text: str, 
    embedding_function, 
    top_k: int = 3
) -> List[Tuple[Document, float]]:
    try:
        start_time = time.time()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        results = db.similarity_search_with_score(query_text, k=top_k)
        
        print(f"Similarity search took {time.time() - start_time:.2f} seconds")
        return results
    except Exception as e:
        print(f"Error in similarity search: {e}")
        return []

def query_rag(
    query_text: str, 
    num_questions: int = 1,
    embedding_function=None, 
    model=None
) -> Dict[str, Any]:
    if embedding_function is None:
        embedding_function = get_embedding_function()
    
    if model is None:
        model = OllamaLLM(
            model=OLLAMA_MODEL, 
            timeout=60
        )
    # might use it later
    # if model is None:
    #     model = ChatGroq(
    #         api_key=GROQ_API_KEY, 
    #         model_name=GROQ_MODEL, 
    #         temperature=0.0,  
    #         timeout=60
    #     )

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
        
        prompt = prompt_template.format(context=context_text, num_questions=num_questions)

        # response_text = model.invoke(prompt).content 
        response_text = model.invoke(prompt)
        
        print(f"Total processing time: {time.time() - start_time:.2f} seconds")
        
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
        
        # might use it later
        # model = ChatGroq(
        #     api_key=GROQ_API_KEY,
        #     model_name=GROQ_MODEL,
        #     temperature=0.0,
        #     timeout=60
        # )

        model = OllamaLLM(
            model=OLLAMA_MODEL,
            timeout=60
        )
        
        prompt_template_str = get_prompt_template(num_questions)
        
        prompt_template_str = prompt_template_str.replace(
            "Konteks Dokumen:\n{context}", 
            "Buat pertanyaan dan jawaban tentang topik: \"{query_text}\""
        )

        prompt_template = ChatPromptTemplate.from_template(prompt_template_str)
        prompt = prompt_template.format(query_text=query_text, num_questions=num_questions)
        
        # response_text = model.invoke(prompt).content  
        response_text = model.invoke(prompt)  
        
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

def parse_json_from_llm_response(response_text: str) -> Dict[str, Any]:
    """Extract and parse JSON from LLM response text."""
    try:
        
        return json.loads(response_text)
    except json.JSONDecodeError:
        try:
            if "```json" in response_text:
                json_parts = response_text.split("```json")
                if len(json_parts) > 1:
                    json_content = json_parts[1].split("```")[0].strip()
                    return json.loads(json_content)
            
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}')
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx+1]
                return json.loads(json_str)
            
            return {
                "questions": [],
                "metadata": {
                    "count": 0,
                    "status": "error",
                    "message": "Failed to parse JSON from LLM response."
                }
            }
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            print(f"Raw response: {response_text}")
            return {
                "questions": [],
                "metadata": {
                    "count": 0,
                    "status": "error",
                    "message": f"Failed to parse JSON from LLM response: {str(e)}"
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
            print(f"Added {len(new_chunks)} new chunks from {filename} to database")
        else:
            print(f"No new chunks to add from {filename}")
            
    except Exception as e:
        print(f"Error processing document {filename}: {e}")


def main():
    parser = argparse.ArgumentParser(description="RAG Query Assistant")
    parser.add_argument("query_text", type=str, help="Query text for RAG search")
    parser.add_argument("--num_questions", type=int, default=1, 
                        help="Number of question-answer pairs to generate (default: 1)")
    args = parser.parse_args()
    
    result = query_rag(args.query_text, args.num_questions)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()