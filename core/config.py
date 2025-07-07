# core/config.py
import os
from dotenv import load_dotenv

load_dotenv() # .env 파일 로드

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

    # Notion API
    NOTION_API_KEY: str = os.getenv("NOTION_API_KEY")
    NOTION_DATABASE_ID: str = os.getenv("NOTION_DATABASE_ID")

settings = Settings()
