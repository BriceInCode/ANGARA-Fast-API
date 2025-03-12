from datetime import datetime
import uuid
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.organisations.organisations import Organisation
from app.models.utilisateurs.utilisateur import Utilisateur
from app.schemas.organisations.organisation_schema import OrganisationCreate, OrganisationRead
from app.schemas.utilisateurs.utilisateur_schema import UtilisateurRead


def generate_reference() -> str:
    """Génère une référence unique pour une organisation."""
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")  # Correction de datetime.datetime → datetime
    unique_id = uuid.uuid4().hex[:6]  # Prend les 6 premiers caractères de l'UUID
    return f"ANGARA-AUTHENTIC-ORG-{timestamp}-{unique_id}"


class OrganisationService:
    @staticmethod
    def create_organisation(db: Session, organisation_data: OrganisationCreate):
        """Crée une nouvelle organisation en s'assurant que le nom et la référence sont uniques."""
        try:
            # Vérifier si un nom identique existe déjà
            if db.query(Organisation).filter(Organisation.nom == organisation_data.nom).scalar():
                return {"code": 409, "message": "Le nom de l'organisation est déjà attribué.", "data": None}

            # Générer une nouvelle référence (ignore celle fournie par l'utilisateur)
            reference = generate_reference()

            # Vérifier si la référence est unique
            while db.query(Organisation).filter(Organisation.reference == reference).scalar():
                reference = generate_reference()  # Générer une nouvelle référence en cas de duplication

            # Supprimer "reference" du dictionnaire (même si l'utilisateur l'a renseignée)
            organisation_dict = organisation_data.dict()
            organisation_dict.pop("reference", None)

            # Création de l'organisation
            new_organisation = Organisation(**organisation_dict, reference=reference)
            db.add(new_organisation)
            db.commit()
            db.refresh(new_organisation)

            return {"code": 201, "message": "Organisation créée avec succès", "data": OrganisationRead.from_orm(new_organisation)}

        except IntegrityError:
            db.rollback()
            return {"code": 500, "message": "Erreur d'intégrité lors de la création de l'organisation.", "data": None}
        except Exception as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur inattendue: {str(e)}", "data": None}

    @staticmethod
    def get_organisation_by_id(db: Session, organisation_id: int):
        """Récupère une organisation par son ID."""
        organisation = db.query(Organisation).filter(Organisation.id == organisation_id).scalar()
        if not organisation:
            return {"code": 404, "message": "Organisation non trouvée.", "data": None}
        return {"code": 200, "message": "Organisation trouvée", "data": OrganisationRead.from_orm(organisation)}

    @staticmethod
    def get_all_organisations(db: Session):
        """Récupère la liste de toutes les organisations."""
        organisations = db.query(Organisation).all()
        return {"code": 200, "message": "Liste des organisations récupérée avec succès", "data": [OrganisationRead.from_orm(org) for org in organisations]}

    @staticmethod
    def update_organisation(db: Session, organisation_id: int, updates: dict):
        """Met à jour une organisation tout en excluant certains champs sensibles."""
        organisation = db.query(Organisation).filter(Organisation.id == organisation_id).scalar()
        if not organisation:
            return {"code": 404, "message": "Organisation non trouvée.", "data": None}

        # Liste des champs à NE PAS modifier
        exclusions = {"id", "reference", "date_creation"}

        for key, value in updates.items():
            if key not in exclusions:
                setattr(organisation, key, value)

        db.commit()
        db.refresh(organisation)
        return {"code": 200, "message": "Organisation mise à jour avec succès", "data": OrganisationRead.from_orm(organisation)}

    @staticmethod
    def delete_organisation(db: Session, organisation_id: int):
        """Supprime une organisation si elle existe."""
        organisation = db.query(Organisation).filter(Organisation.id == organisation_id).scalar()
        if not organisation:
            return {"code": 404, "message": "Organisation non trouvée.", "data": None}

        db.delete(organisation)
        db.commit()
        return {"code": 200, "message": "Organisation supprimée avec succès", "data": None}

    @staticmethod
    def get_organisation_users(db: Session, identifier: str):
        """Récupère les utilisateurs d'une organisation à partir de son ID, son nom ou sa référence."""
        organisation = db.query(Organisation).filter(
            (Organisation.id == identifier) | (Organisation.nom == identifier) | (Organisation.reference == identifier)
        ).scalar()

        if not organisation:
            return {"code": 404, "message": "Organisation non trouvée.", "data": None}

        users = db.query(Utilisateur).filter(Utilisateur.organisation_id == organisation.id).all()
        return {"code": 200, "message": "Utilisateurs récupérés avec succès", "data": [UtilisateurRead.from_orm(user) for user in users]}
