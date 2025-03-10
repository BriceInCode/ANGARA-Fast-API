from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.documents.models import Document
from app.documents.schemas import DocumentCreate, DocumentRead

class DocumentService:
    def __init__(self, db: Session):
        self.db = db

    def create_document(self, document: DocumentCreate) -> DocumentRead:
        db_document = Document(**document.dict())
        self.db.add(db_document)
        self.db.commit()
        self.db.refresh(db_document)
        return DocumentRead.from_orm(db_document)

    def get_document(self, document_id: int) -> Optional[DocumentRead]:
        db_document = self.db.query(Document).filter(Document.id == document_id).first()
        if db_document:
            return DocumentRead.from_orm(db_document)
        return None

    def get_all_documents(self) -> List[DocumentRead]:
        db_documents = self.db.query(Document).all()
        return [DocumentRead.from_orm(document) for document in db_documents]

    def update_document(self, document_id: int, document: DocumentCreate) -> Optional[DocumentRead]:
        db_document = self.db.query(Document).filter(Document.id == document_id).first()
        if db_document:
            for key, value in document.dict().items():
                setattr(db_document, key, value)
            db_document.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(db_document)
            return DocumentRead.from_orm(db_document)
        return None

    def delete_document(self, document_id: int) -> bool:
        db_document = self.db.query(Document).filter(Document.id == document_id).first()
        if db_document:
            self.db.delete(db_document)
            self.db.commit()
            return True
        return False
