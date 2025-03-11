import argparse
import time
import os
import json

from typing import List, Tuple, Dict, Any
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from langchain_core.documents import Document

from get_embedding_function import get_embedding_function

CHROMA_PATH = os.getenv("CHROMA_PATH")
DATA_PATH = os.getenv("DATA_PATH")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
URL_PATH = os.getenv("URL_PATH")
TOP_K_RESULTS = 3
TIMEOUT = 60

def get_prompt_template(num_questions):
    if num_questions == 1:
        template = """
Kamu adalah guru profesional yang ahli membuat soal ujian berkualitas tinggi.

Kriteria Pembuatan Soal:
- Hasilkan TEPAT 1 pasangan pertanyaan dan jawaban
- Pertanyaan harus mendalam dan menguji pemahaman konseptual
- Jawaban singkat, akurat, dan berbasis dokumen (maks 3 kalimat)
- Gunakan Bahasa Indonesia yang baku dan jelas

Konteks Dokumen:
{context}

PENTING: 
- Output harus dalam format JSON valid yang dapat diparse oleh Python
- Jangan sertakan penjelasan atau teks apapun di luar format JSON
- Jika tidak bisa membuat soal dari dokumen, hasilkan JSON dengan pesan error

Format JSON yang dihasilkan harus sebagai berikut:
{{
  "questions": [
    {{
      "question": "Pertanyaan yang spesifik dan mendalam",
      "answer": "Jawaban yang singkat dan faktual"
    }}
  ],
  "metadata": {{
    "count": 1,
    "status": "success"
  }}
}}
"""
    else:
        template = """
Kamu adalah guru profesional yang ahli membuat soal ujian berkualitas tinggi.

Kriteria Pembuatan Soal:
- Hasilkan TEPAT {num_questions} pasangan pertanyaan dan jawaban
- Pertanyaan harus mendalam dan menguji pemahaman konseptual
- Jawaban singkat, akurat, dan berbasis dokumen (maks 3 kalimat)
- Gunakan Bahasa Indonesia yang baku dan jelas

Konteks Dokumen:
{context}

PENTING: 
- Output harus dalam format JSON valid yang dapat diparse oleh Python
- Jangan sertakan penjelasan atau teks apapun di luar format JSON
- Jika tidak bisa membuat soal dari dokumen, hasilkan JSON dengan pesan error

Format JSON yang dihasilkan harus sebagai berikut:
{{
  "questions": [
    {{
      "question": "Pertanyaan 1 yang spesifik dan mendalam",
      "answer": "Jawaban 1 yang singkat dan faktual"
    }},
    ...
  ],
  "metadata": {{
    "count": {num_questions},
    "status": "success"
  }}
}}
"""
    return template

def get_similarity_search(
    query_text: str, 
    embedding_function, 
    top_k: int = TOP_K_RESULTS
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
            timeout=TIMEOUT
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
        
        prompt = prompt_template.format(context=context_text, num_questions=num_questions)

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
        
        model = OllamaLLM(
            model=OLLAMA_MODEL,
            timeout=TIMEOUT
        )
        
        prompt_template_str = get_prompt_template(num_questions)
        
        prompt_template_str = prompt_template_str.replace(
            "Konteks Dokumen:\n{context}", 
            "Buat pertanyaan dan jawaban tentang topik: \"{query_text}\""
        )

        prompt_template = ChatPromptTemplate.from_template(prompt_template_str)
        prompt = prompt_template.format(query_text=query_text, num_questions=num_questions)
        
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