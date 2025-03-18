from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict, Any
from app.configs.enumerations.Motifs import MotifEnum
from app.models.demandes.motif import Motif
from app.schemas.demandes.motif_schema import MotifCreate

class MotifService:
    @staticmethod
    def create_motif(db: Session, motif_data: MotifCreate) -> Dict[str, Any]:
        """Crée un nouveau motif."""
        try:
            # Vérifier si le statut est valide
            if motif_data.motif not in MotifEnum.__members__:
                return {"code": 400, "message": "Le motif renseigné n'existe pas encore dans notre système.", "data": None}

            motif = Motif(**motif_data.dict())
            db.add(motif)
            db.commit()
            db.refresh(motif)
            return {"code": 201, "message": "Motif créé avec succès", "data": motif}
        except SQLAlchemyError as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur lors de la création du motif: {str(e)}", "data": None}

    @staticmethod
    def get_motif_by_id(db: Session, motif_id: int) -> Dict[str, Any]:
        """Récupère un motif par son ID."""
        try:
            motif = db.query(Motif).filter(Motif.id == motif_id).first()
            if motif:
                return {"code": 200, "message": "Motif trouvé", "data": motif}
            return {"code": 404, "message": "Motif introuvable", "data": None}
        except SQLAlchemyError as e:
            return {"code": 500, "message": f"Erreur lors de la récupération du motif: {str(e)}", "data": None}

    @staticmethod
    def get_all_motifs(db: Session) -> Dict[str, Any]:
        """Récupère tous les motifs."""
        try:
            motifs = db.query(Motif).all()
            return {"code": 200, "message": "Liste des motifs récupérée", "data": motifs}
        except SQLAlchemyError as e:
            return {"code": 500, "message": f"Erreur lors de la récupération des motifs: {str(e)}", "data": None}

    @staticmethod
    def delete_motif(db: Session, motif_id: int) -> Dict[str, Any]:
        """Supprime un motif par son ID."""
        try:
            motif = db.query(Motif).filter(Motif.id == motif_id).first()
            if motif:
                db.delete(motif)
                db.commit()
                return {"code": 200, "message": "Motif supprimé avec succès", "data": motif}
            return {"code": 404, "message": "Motif introuvable", "data": None}
        except SQLAlchemyError as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur lors de la suppression du motif: {str(e)}", "data": None}
