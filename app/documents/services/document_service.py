import os
import shutil
import hashlib
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import UploadFile
from app.documents.models.document import Document
from app.documents.schemas import DocumentRead
from app.config.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {"pdf", "jpg", "png", "jpeg"}
MAX_FILE_SIZE_MB = 10
BASE_DOCUMENTS_STORAGE_PATH = settings.DOCUMENTS_STORAGE_PATH

class DocumentService:
    def __init__(self, db: Session):
        self.db = db

    def _get_document_path(self, document_type: str) -> str:
        today_date = datetime.utcnow().strftime("%Y-%m-%d")
        folder_name = f"{today_date}"
        folder_path = os.path.join(BASE_DOCUMENTS_STORAGE_PATH + "/" + document_type.upper(), folder_name)
        os.makedirs(folder_path, exist_ok=True)
        return folder_path

    def _validate_file(self, file: UploadFile) -> dict:
        # Validation du fichier (format et taille)
        file_extension = file.filename.split(".")[-1].lower()
        file.file.seek(0)
        file_size_mb = len(file.file.read()) / (1024 * 1024)
        file.file.seek(0)

        if file_extension not in ALLOWED_EXTENSIONS:
            return {"code": 400, "message": "Format non autorisé.", "data": None}

        if file_size_mb > MAX_FILE_SIZE_MB:
            return {"code": 400, "message": "Fichier trop volumineux.", "data": None}

        return {"code": 200, "message": "Fichier valide", "data": None}

    def _calculate_file_hash(self, file_path: str) -> str:
        # Calcul du hash du fichier pour éviter les doublons
        sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    sha256.update(chunk)
        except Exception as e:
            logger.error(f"Erreur hash: {e}")
            return ""
        return sha256.hexdigest()

    def create_document(self, demande_id: int, document_type: str, file: UploadFile) -> dict:
        file_validation = self._validate_file(file)
        if file_validation["code"] != 200:
            return file_validation

        try:
            # Récupère le chemin de stockage du document
            document_path = self._get_document_path(document_type)
            file_extension = file.filename.split('.')[-1].lower()
            filename = f"{demande_id}_{int(datetime.utcnow().timestamp())}.{file_extension}"
            file_path = os.path.join(document_path, filename)

            # Sauvegarde du fichier sur le disque
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Calcul du hash du fichier pour le stockage
            file_hash = self._calculate_file_hash(file_path)
            file_size = os.path.getsize(file_path)
            now = datetime.utcnow()

            # Vérification si un document existe déjà pour cette demande
            db_document = self.db.query(Document).filter(Document.demande_id == demande_id).first()

            if db_document:
                # Si un document existe déjà, suppression de l'ancien fichier et du document dans la base de données
                if os.path.exists(db_document.file_path):
                    os.remove(db_document.file_path)  # Suppression du fichier du disque
                self.db.delete(db_document)  # Suppression du document dans la base de données
                self.db.commit()
                logger.info(f"Ancien document supprimé pour la demande {demande_id}.")
                message = "Document mis à jour avec succès."

            else:
                message = "Document téléchargé avec succès."

            # Création ou mise à jour du document dans la base de données
            db_document = Document(
                demande_id=demande_id,
                file_path=file_path,
                file_type=file_extension,
                file_size=file_size,
                checksum=file_hash,
                created_at=now,
                updated_at=now,
            )
            self.db.add(db_document)
            self.db.commit()
            self.db.refresh(db_document)

            return {"code": 200, "message": message, "data": DocumentRead.from_orm(db_document)}

        except SQLAlchemyError as e:
            self.db.rollback()  # Annule la transaction en cas d'erreur
            logger.error(f"Erreur SQL: {e}")
            return {"code": 500, "message": "Erreur BDD.", "data": str(e)}

        except Exception as e:
            logger.error(f"Erreur inattendue: {e}")
            return {"code": 500, "message": "Erreur inattendue.", "data": str(e)}
