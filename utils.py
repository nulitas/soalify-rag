import argparse
import time
import os

from typing import List, Tuple
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
    template = """
Kamu adalah guru profesional yang ahli membuat soal ujian berkualitas tinggi.

Kriteria Pembuatan Soal:
- Hasilkan TEPAT {num_questions} pasangan pertanyaan dan jawaban
- Pertanyaan harus mendalam dan menguji pemahaman konseptual
- Jawaban singkat, akurat, dan berbasis dokumen (maks 3 kalimat)
- Gunakan Bahasa Indonesia yang baku dan jelas

Konteks Dokumen:
{context}

Format Wajib Dihasilkan:
"""
    if num_questions == 1:
        template += """
Pertanyaan: [Pertanyaan spesifik dan mendalam]
Jawaban: [Jawaban singkat dan faktual]
"""
    else:
        template += """
Untuk setiap pasangan soal, gunakan format berikut dan beri nomor untuk setiap pasangan:

"""
        for i in range(1, min(3, num_questions + 1)):
            template += f"""
Pertanyaan {i}: [Pertanyaan spesifik dan mendalam]
Jawaban {i}: [Jawaban singkat dan faktual]
"""
    template += """
PENTING: 
- Pastikan untuk menghasilkan BAIK pertanyaan MAUPUN jawaban untuk SEMUA {num_questions} soal yang diminta.
- Jika tidak bisa membuat pertanyaan dan jawaban, respon dengan "Tidak dapat membuat soal dari dokumen ini."
- JANGAN tambahkan penjelasan, komentar, atau teks tambahan di luar format yang ditentukan.
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
) -> str:
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
            return "Unable to find relevant documents."
        context_text = "\n\n---\n\n".join([
            doc.page_content for doc, _score in results
        ])

        prompt_template_str = get_prompt_template(num_questions)
        prompt_template = ChatPromptTemplate.from_template(prompt_template_str)
        
        prompt = prompt_template.format(context=context_text, num_questions=num_questions)

        response_text = model.invoke(prompt)
        
        print(f"Total processing time: {time.time() - start_time:.2f} seconds")
        return response_text
    
    except Exception as e:
        print(f"Error in RAG query: {e}")
        return "An error occurred in processing the query."
    
def direct_llm_questions(query_text: str, num_questions: int = 1) -> str:
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
        return response_text
    
    except Exception as e:
        print(f"Error generating direct questions: {e}")
        return "There was an error in making the question."

def main():
    parser = argparse.ArgumentParser(description="RAG Query Assistant")
    parser.add_argument("query_text", type=str, help="Query text for RAG search")
    parser.add_argument("--num_questions", type=int, default=1, 
                        help="Number of question-answer pairs to generate (default: 1)")
    args = parser.parse_args()
    
    query_rag(args.query_text, args.num_questions)

if __name__ == "__main__":
    main()