import os

from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

def get_embedding_function():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
    )