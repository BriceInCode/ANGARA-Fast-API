import os
from dotenv import load_dotenv

# Définir le chemin du fichier .env
dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(dotenv_path=dotenv_path)

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    GMAIL_EMAIL: str = os.getenv("GMAIL_EMAIL")      
    GMAIL_PASSWORD: str = os.getenv("GMAIL_PASSWORD")   
    GMAIL_USERNAME: str = os.getenv("GMAIL_USERNAME")
    DOCUMENTS_STORAGE_PATH: str = os.getenv("DOCUMENTS_STORAGE_PATH")

settings = Settings()
