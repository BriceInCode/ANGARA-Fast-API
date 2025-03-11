from typing import List, Optional, Dict, Union
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import exists
from app.documents.models.demande import Demande
from app.client.models.client import Client
from app.documents.models.types.status import StatusType
from app.documents.schemas import DemandeCreate, DemandeRead


class DemandeService:
    def __init__(self, db: Session):
        self.db = db

    def generate_unique_demande_number(self) -> str:
        """Génère un numéro unique de demande au format P0-YYYYMMDD-XXXXX"""
        today_str = datetime.utcnow().strftime("%Y%m%d")

        last_number = (
            self.db.query(Demande.request_number)
            .filter(Demande.request_number.like(f"P0-{today_str}-%"))
            .order_by(Demande.request_number.desc())
            .limit(1)
            .scalar()
        )

        next_number = int(last_number.split("-")[-1]) + 1 if last_number else 1
        return f"P0-{today_str}-{next_number:05d}"

    def is_valid_session(self, session_id: int) -> bool:
        """Vérifie si un client avec ce session_id existe"""
        return self.db.query(exists().where(Client.id == session_id)).scalar()

    def create_demande(self, demande: DemandeCreate) -> Dict[str, Union[int, str, Dict]]:
        """Crée une demande après validation du session_id et génération d'un numéro unique"""
        if not self.is_valid_session(demande.session_id):
            return {"code": 400, "message": "Session invalide. Veuillez vérifier votre identifiant.", "data": None}

        try:
            numero_demande = self.generate_unique_demande_number()

            db_demande = Demande(
                **demande.dict(exclude={"request_number"}),
                request_number=numero_demande,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            self.db.add(db_demande)
            self.db.commit()
            self.db.refresh(db_demande)

            return {
                "code": 201,
                "message": "Demande créée avec succès.",
                "data": DemandeRead.from_orm(db_demande)
            }

        except Exception as e:
            self.db.rollback()
            return {"code": 500, "message": f"Erreur lors de la création : {str(e)}", "data": None}

    def get_demande(self, demande_id: int) -> Dict[str, Union[int, str, Dict]]:
        """Récupère une demande par son ID"""
        demande = self.db.query(Demande).filter(Demande.id == demande_id).first()
        if not demande:
            return {"code": 404, "message": "Aucune demande trouvée.", "data": None}

        return {"code": 200, "message": "Demande récupérée avec succès.", "data": DemandeRead.from_orm(demande)}

    def get_all_demandes(self) -> Dict[str, Union[int, str, List[Dict]]]:
        """Récupère toutes les demandes"""
        demandes = self.db.query(Demande).all()
        return {
            "code": 200,
            "message": f"{len(demandes)} demande(s) trouvée(s).",
            "data": [DemandeRead.from_orm(demande) for demande in demandes]
        }

    def get_demandes_by_session_id(self, session_id: int) -> Dict[str, Union[int, str, List[Dict]]]:
        """Récupère toutes les demandes associées à un session_id donné"""
        if not self.is_valid_session(session_id):
            return {"code": 400, "message": "Session invalide. Aucun utilisateur trouvé.", "data": None}

        demandes = self.db.query(Demande).filter(Demande.session_id == session_id).all()
        return {
            "code": 200,
            "message": f"{len(demandes)} demande(s) trouvée(s) pour cette session.",
            "data": [DemandeRead.from_orm(demande) for demande in demandes]
        }

    def update_demande(self, demande_id: int, demande: DemandeCreate) -> Dict[str, Union[int, str, Dict]]:
        """Met à jour une demande après validation du session_id"""
        db_demande = self.db.query(Demande).filter(Demande.id == demande_id).first()
        if not db_demande:
            return {"code": 404, "message": "Aucune demande trouvée.", "data": None}

        if not self.is_valid_session(demande.session_id):
            return {"code": 400, "message": "Session invalide. Vérifiez votre identifiant.", "data": None}

        try:
            for key, value in demande.dict().items():
                setattr(db_demande, key, value)

            db_demande.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(db_demande)

            return {"code": 200, "message": "Demande mise à jour avec succès.", "data": DemandeRead.from_orm(db_demande)}

        except Exception as e:
            self.db.rollback()
            return {"code": 500, "message": f"Erreur lors de la mise à jour : {str(e)}", "data": None}

    def delete_demande(self, demande_id: int) -> Dict[str, Union[int, str, None]]:
        """Supprime une demande par son ID"""
        db_demande = self.db.query(Demande).filter(Demande.id == demande_id).first()
        if not db_demande:
            return {"code": 404, "message": "Aucune demande trouvée.", "data": None}

        try:
            self.db.delete(db_demande)
            self.db.commit()
            return {"code": 200, "message": "Demande supprimée avec succès.", "data": None}

        except Exception as e:
            self.db.rollback()
            return {"code": 500, "message": f"Erreur lors de la suppression : {str(e)}", "data": None}

    def update_demande_status(self, demande_id: int, new_status: StatusType) -> Dict[str, Union[int, str, Dict]]:
        """Met à jour le statut d'une demande"""
        db_demande = self.db.query(Demande).filter(Demande.id == demande_id).first()
        if not db_demande:
            return {"code": 404, "message": "Aucune demande trouvée.", "data": None}

        try:
            db_demande.status = new_status
            db_demande.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(db_demande)

            return {
                "code": 200,
                "message": f"Demande {new_status.value} avec succès.",
                "data": DemandeRead.from_orm(db_demande)
            }

        except Exception as e:
            self.db.rollback()
            return {"code": 500, "message": f"Erreur lors de la mise à jour du statut : {str(e)}", "data": None}

    def valider_demande(self, demande_id: int) -> Dict[str, Union[int, str, Dict]]:
        """Valide une demande"""
        return self.update_demande_status(demande_id, StatusType.VALIDE)

    def refuser_demande(self, demande_id: int) -> Dict[str, Union[int, str, Dict]]:
        """Refuse une demande"""
        return self.update_demande_status(demande_id, StatusType.REFUSE)

    def mettre_en_cours_demande(self, demande_id: int) -> Dict[str, Union[int, str, Dict]]:
        """Met une demande en cours de traitement"""
        return self.update_demande_status(demande_id, StatusType.EN_COURS)
