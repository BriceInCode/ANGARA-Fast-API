from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.documents.models import Demande
from app.documents.schemas import DemandeCreate, DemandeRead

class DemandeService:
    def __init__(self, db: Session):
        self.db = db

    def create_demande(self, demande: DemandeCreate) -> DemandeRead:
        db_demande = Demande(**demande.dict())
        self.db.add(db_demande)
        self.db.commit()
        self.db.refresh(db_demande)
        return DemandeRead.from_orm(db_demande)

    def get_demande(self, demande_id: int) -> Optional[DemandeRead]:
        db_demande = self.db.query(Demande).filter(Demande.id == demande_id).first()
        if db_demande:
            return DemandeRead.from_orm(db_demande)
        return None

    def get_all_demandes(self) -> List[DemandeRead]:
        db_demandes = self.db.query(Demande).all()
        return [DemandeRead.from_orm(demande) for demande in db_demandes]

    def update_demande(self, demande_id: int, demande: DemandeCreate) -> Optional[DemandeRead]:
        db_demande = self.db.query(Demande).filter(Demande.id == demande_id).first()
        if db_demande:
            for key, value in demande.dict().items():
                setattr(db_demande, key, value)
            db_demande.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(db_demande)
            return DemandeRead.from_orm(db_demande)
        return None

    def delete_demande(self, demande_id: int) -> bool:
        db_demande = self.db.query(Demande).filter(Demande.id == demande_id).first()
        if db_demande:
            self.db.delete(db_demande)
            self.db.commit()
            return True
        return False
