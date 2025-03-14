
from langchain_huggingface import HuggingFaceEmbeddings

from var import EMBEDDING_MODEL

def get_embedding_function():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )