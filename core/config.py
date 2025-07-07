# core/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Source API
    SOURCE_API_BASE_URL: str = os.getenv("SOURCE_API_BASE_URL")

    # MySQL DB
    MYSQL_HOST: str = os.getenv("MYSQL_HOST")
    MYSQL_USER: str = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD")
    MYSQL_DB: str = os.getenv("MYSQL_DB")

    # AI Translation API
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    GENAI_API_KEY: str = os.getenv("GENAI_API_KEY")
    OPENAI_EMBEDDING_MODEL: str = os.getenv("OPENAI_EMBEDDING_MODEL")
    OPENAI_EMBEDDING_DIM: int = int(os.getenv("OPENAI_EMBEDDING_DIM"))
    GENAI_MODEL: str = os.getenv("GENAI_MODEL")

    # FAISS DB
    FAISS_INDEX_FILE: str = os.getenv("FAISS_INDEX_FILE")
    FAISS_MAP_FILE: str = os.getenv("FAISS_MAP_FILE")

    # Notion API
    NOTION_API_KEY: str = os.getenv("NOTION_API_KEY")
    NOTION_DATABASE_ID: str = os.getenv("NOTION_DATABASE_ID")
    NOTION_BASE_URL: str = os.getenv("NOTION_BASE_URL")
    NOTION_PAGE_URL: str = os.getenv("NOTION_PAGE_URL")
    NOTION_QUERY_URL: str = os.getenv("NOTION_QUERY_URL")

settings = Settings()
