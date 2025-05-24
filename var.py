import os
from dotenv import load_dotenv

load_dotenv()
CHROMA_PATH = os.getenv("CHROMA_PATH")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DATA_PATH = os.getenv("DATA_PATH")
URL_PATH = os.getenv("URL_PATH")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
DATABASE_URL = os.getenv("DATABASE_URL")
