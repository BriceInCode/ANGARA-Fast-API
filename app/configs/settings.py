import os
from dotenv import load_dotenv

# Chemin absolu du fichier .env
dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(dotenv_path=dotenv_path)

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    GMAIL_EMAIL: str = os.getenv("GMAIL_EMAIL")
    GMAIL_PASSWORD: str = os.getenv("GMAIL_PASSWORD")
    GMAIL_USERNAME: str = os.getenv("GMAIL_USERNAME")
    DOCUMENTS_STORAGE_PATH: str = os.getenv("DOCUMENTS_STORAGE_PATH")
    ACCESS_TOKEN_EXPIRE_MINUTES: str = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    ALGORITHM: str = os.getenv("ALGORITHM")

    def check_config(self):
        print("✅ Configuration chargée :")
        print(f"DATABASE_URL: {self.DATABASE_URL}")
        print(f"SECRET_KEY: {self.SECRET_KEY}")
        print(f"GMAIL_EMAIL: {self.GMAIL_EMAIL}")
        print(f"GMAIL_USERNAME: {self.GMAIL_USERNAME}")

settings = Settings()
settings.check_config()
