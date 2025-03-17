import os
from dotenv import load_dotenv

load_dotenv()
CHROMA_PATH = os.getenv("CHROMA_PATH")
DATA_PATH = os.getenv("DATA_PATH")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
URL_PATH = os.getenv("URL_PATH")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
DATABASE_URL = os.getenv("DATABASE_URL")