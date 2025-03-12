from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.organisations.centre_etat_civil import CentreEtatCivil
from app.models.utilisateurs.utilisateur import Utilisateur
from app.schemas.organisations.centre_etat_civil_schema import CentreEtatCivilCreate, CentreEtatCivilRead
from app.schemas.utilisateurs.utilisateur_schema import UtilisateurRead

class CentreEtatCivilService:
    @staticmethod
    def create_centre(db: Session, centre_data: CentreEtatCivilCreate):
        try:
            existing_reference = db.query(CentreEtatCivil).filter(CentreEtatCivil.reference == centre_data.reference).first()
            if existing_reference:
                return {"code": 409, "message": "La référence fournie est déjà utilisée.", "data": None}

            existing_nom = db.query(CentreEtatCivil).filter(CentreEtatCivil.nom == centre_data.nom).first()
            if existing_nom:
                return {"code": 409, "message": "Le nom du centre est déjà attribué à un autre centre.", "data": None}

            existing_email = db.query(CentreEtatCivil).filter(CentreEtatCivil.email == centre_data.email).first()
            if existing_email:
                return {"code": 409, "message": "L'email fourni est déjà associé à un autre centre.", "data": None}

            existing_telephone = db.query(CentreEtatCivil).filter(CentreEtatCivil.telephone == centre_data.telephone).first()
            if existing_telephone:
                return {"code": 409, "message": "Le numéro de téléphone est déjà utilisé par un autre centre.", "data": None}

            new_centre = CentreEtatCivil(**centre_data.dict())
            db.add(new_centre)
            db.commit()
            db.refresh(new_centre)
            return {"code": 201, "message": "Centre créé avec succès", "data": CentreEtatCivilRead.from_orm(new_centre)}

        except IntegrityError:
            db.rollback()
            return {"code": 500, "message": "Erreur d'intégrité lors de la création du centre.", "data": None}

    @staticmethod
    def get_centre_by_id(db: Session, centre_id: int):
        centre = db.query(CentreEtatCivil).filter(CentreEtatCivil.id == centre_id).first()
        return {"code": 200, "message": "Centre trouvé", "data": CentreEtatCivilRead.from_orm(centre)} if centre else {"code": 404, "message": "Centre d'état civil non trouvé.", "data": None}

    @staticmethod
    def get_all_centres(db: Session):
        return {"code": 200, "message": "Liste des centres récupérée avec succès", "data": db.query(CentreEtatCivil).all()}

    @staticmethod
    def update_centre(db: Session, centre_id: int, updates: dict):
        centre = db.query(CentreEtatCivil).filter(CentreEtatCivil.id == centre_id).first()
        if not centre:
            return {"code": 404, "message": "Centre d'état civil non trouvé.", "data": None}
        for key, value in updates.items():
            setattr(centre, key, value)
        db.commit()
        db.refresh(centre)
        return {"code": 200, "message": "Centre mis à jour avec succès", "data": CentreEtatCivilRead.from_orm(centre)}

    @staticmethod
    def delete_centre(db: Session, centre_id: int):
        centre = db.query(CentreEtatCivil).filter(CentreEtatCivil.id == centre_id).first()
        if not centre:
            return {"code": 404, "message": "Centre d'état civil non trouvé.", "data": None}
        db.delete(centre)
        db.commit()
        return {"code": 200, "message": "Centre supprimé avec succès", "data": None}

    @staticmethod
    def get_users_by_centre(db: Session, identifier: str):
        centre = db.query(CentreEtatCivil).filter(
            (CentreEtatCivil.reference == identifier) |
            (CentreEtatCivil.nom == identifier) |
            (CentreEtatCivil.email == identifier) |
            (CentreEtatCivil.id == identifier) |
            (CentreEtatCivil.telephone == identifier)
        ).first()

        if not centre:
            return {"code": 404, "message": "Centre d'état civil non trouvé.", "data": None}

        users = db.query(Utilisateur).filter(Utilisateur.centre_id == centre.id).all()
        return {"code": 200, "message": "Utilisateurs récupérés avec succès", "data": [UtilisateurRead.from_orm(user) for user in users]}
