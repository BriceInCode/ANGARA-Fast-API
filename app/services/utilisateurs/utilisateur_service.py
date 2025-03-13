import random
import string
from datetime import datetime
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

from app.configs.enumerations.Comptes import ComptesEnum
from app.configs.utils.email_service import EmailService
from app.models.organisations.centre_etat_civil import CentreEtatCivil
from app.models.organisations.organisations import Organisation
from app.models.utilisateurs.permission import Permission
from app.models.utilisateurs.role import Role
from app.models.utilisateurs.utilisateur import Utilisateur
from app.schemas.utilisateurs.utilisateur_schema import UtilisateurCreate, UtilisateurRead

# Initialisation de CryptContext pour le hachage du mot de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UtilisateurService:
    def __init__(self, db: Session):
        self.db = db
        self.email_service = EmailService()

    @staticmethod
    def generate_password(length=10):
        """Génère un mot de passe aléatoire"""
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))

    @staticmethod
    def hash_password(password: str):
        """Hash le mot de passe généré"""
        return pwd_context.hash(password)

    def send_welcome_email(self, email, role_nom, mot_de_passe):
        """Envoie un email de bienvenue avec le mot de passe et le rôle"""
        current_hour = datetime.now().hour
        salutation = "Bonjour" if current_hour < 18 else "Bonsoir"
        subject = "Compte utilisateur créé"
        body = (
            f"Nous vous informons qu'un compte utilisateur vous a été créé en tant que {role_nom}.\n\n"
            f"Votre mot de passe est le suivant : {mot_de_passe}\n\n"
        )
        return self.email_service.send_email(email, subject, body)

    def create_utilisateur(self, utilisateur_data: UtilisateurCreate):
        try:
            # Vérifier si l'email est déjà utilisé
            if self.db.query(Utilisateur).filter(Utilisateur.email == utilisateur_data.email).first():
                return {"code": 409, "message": "L'email est déjà utilisé.", "data": None}

            # Vérifier l'existence du rôle et de l'organisation
            role = self.db.query(Role).filter(Role.id == utilisateur_data.role_id).first()
            if not role:
                return {"code": 404, "message": "Rôle non trouvé", "data": None}

            organisation = self.db.query(Organisation).filter(Organisation.id == utilisateur_data.organisation_id).first()
            if not organisation:
                return {"code": 404, "message": "Organisation non trouvée", "data": None}

            # Générer un mot de passe aléatoire et le hacher
            mot_de_passe = self.generate_password()
            hashed_password = self.hash_password(mot_de_passe)

            # S'assurer que le statut est ACTIF par défaut
            utilisateur_data.status = ComptesEnum.ACTIF
            new_utilisateur = Utilisateur(**utilisateur_data.dict(), mot_de_passe=hashed_password)
            self.db.add(new_utilisateur)
            self.db.commit()
            self.db.refresh(new_utilisateur)

            # Remplacer RoleEnum par son équivalent lisible
            role_nom = role.nom.value  # Utiliser le nom du rôle dans la base de données (en supposant qu'il est déjà défini)

            # Envoyer l'email de bienvenue
            success = self.send_welcome_email(utilisateur_data.email, role_nom, mot_de_passe)
            message = "Utilisateur créé avec succès, email envoyé" if success else "Utilisateur créé avec succès, mais l'email n'a pas pu être envoyé"
            return {"code": 201, "message": message, "data": UtilisateurRead.from_orm(new_utilisateur)}
        
        except IntegrityError as e:
            self.db.rollback()
            return {"code": 500, "message": f"Erreur d'intégrité lors de la création de l'utilisateur: {str(e)}", "data": None}
        except Exception as e:
            self.db.rollback()
            return {"code": 500, "message": f"Erreur inattendue: {str(e)}", "data": None}
        
        
    @classmethod
    def get_utilisateur(cls, db: Session, param: str):
        utilisateur = None

        if param.isdigit():
            utilisateur = db.query(Utilisateur).filter(Utilisateur.id == int(param)).first()
        else:
            utilisateur = db.query(Utilisateur).filter(Utilisateur.email == param).first()
        if utilisateur:
            return {"code": 200, "message": "Utilisateur trouvé", "data": UtilisateurRead.from_orm(utilisateur)}
        return {"code": 404, "message": "Utilisateur non trouvé", "data": None}


    def get_all_utilisateurs(self):
        utilisateurs = self.db.query(Utilisateur).all()
        return {"code": 200, "message": "Liste des utilisateurs récupérée", "data": [UtilisateurRead.from_orm(u) for u in utilisateurs]}

    @staticmethod
    def get_utilisateurs_by_role(db: Session, role: str):
        # Tenter de convertir `role` en entier pour vérifier si c'est un ID
        try:
            role_id = int(role)  # Si `role` est un ID, cela va passer
            role_obj = db.query(Role).filter(Role.id == role_id).first()
        except ValueError:
            # Si la conversion échoue, c'est probablement un nom de rôle
            role_obj = db.query(Role).filter(Role.nom == role).first()
        
        if role_obj:
            utilisateurs = db.query(Utilisateur).filter(Utilisateur.role_id == role_obj.id).all()
            return {"code": 200, "message": "Utilisateurs trouvés", "data": utilisateurs}
        
        return {"code": 404, "message": "Role non trouvé", "data": None}

    @staticmethod
    def get_utilisateurs_by_organisation(db: Session, organisation: str):
        """
        Retourne les utilisateurs par organisation.
        Le paramètre peut être l'ID (int), le nom ou la référence (str).
        """
        # Vérification si l'organisation est un ID (entier)
        try:
            organisation_id = int(organisation)  # Tentative de conversion en entier
            utilisateurs = db.query(Utilisateur).filter(Utilisateur.organisation_id == organisation_id).all()
        except ValueError:  # Si l'organisation n'est pas un entier, on recherche par nom ou référence
            # Recherche de l'organisation par nom ou référence
            org_obj = db.query(Organisation).filter(
                (Organisation.nom == organisation) | (Organisation.reference == organisation)
            ).first()

            if org_obj:
                utilisateurs = db.query(Utilisateur).filter(Utilisateur.organisation_id == org_obj.id).all()
            else:
                return {"code": 404, "message": "Organisation non trouvée", "data": None}

        # Si des utilisateurs ont été trouvés, on les retourne, sinon un message d'erreur
        if utilisateurs:
            return {"code": 200, "message": "Utilisateurs trouvés", "data": [UtilisateurRead.from_orm(u) for u in utilisateurs]}
        return {"code": 404, "message": "Aucun utilisateur trouvé pour cette organisation", "data": None}

    @staticmethod
    def get_utilisateurs_by_centre(db: Session, centre):
        """
        Retourne les utilisateurs par centre d'état civil.
        Le paramètre peut être l'ID (int) ou une valeur de référence, nom, email ou téléphone (str).
        """
        if isinstance(centre, int):
            # Recherche par ID du centre
            utilisateurs = db.query(Utilisateur).filter(Utilisateur.centre_id == centre).all()
        else:
            # Recherche par référence, nom, email ou téléphone
            centre_obj = db.query(CentreEtatCivil).filter(
                (CentreEtatCivil.id == centre) |
                (CentreEtatCivil.reference == centre) |
                (CentreEtatCivil.nom == centre) |
                (CentreEtatCivil.email == centre) |
                (CentreEtatCivil.telephone == centre)
            ).first()

            if centre_obj:
                # Recherche des utilisateurs pour ce centre
                utilisateurs = db.query(Utilisateur).filter(Utilisateur.centre_id == centre_obj.id).all()
            else:
                return {"code": 404, "message": "Centre d'état civil non trouvé", "data": None}

        if utilisateurs:
            # Retourne les utilisateurs trouvés sous forme de données lisibles
            return {"code": 200, "message": "Utilisateurs trouvés", "data": [UtilisateurRead.from_orm(u) for u in utilisateurs]}
        
        return {"code": 404, "message": "Aucun utilisateur trouvé pour ce centre d'état civil", "data": None}



    @staticmethod
    def update_utilisateur(db: Session, utilisateur_id: int, updates: dict):
        # Utilisation de db sans self
        utilisateur = db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
        if not utilisateur:
            return {"code": 404, "message": "Utilisateur non trouvé", "data": None}
        
        try:
            if 'role_id' in updates:
                role = db.query(Role).filter(Role.id == updates['role_id']).first()
                if not role:
                    return {"code": 404, "message": "Rôle non trouvé", "data": None}
                utilisateur.role_id = updates['role_id']
            
            if 'organisation_id' in updates:
                organisation = db.query(Organisation).filter(Organisation.id == updates['organisation_id']).first()
                if not organisation:
                    return {"code": 404, "message": "Organisation non trouvée", "data": None}
                utilisateur.organisation_id = updates['organisation_id']

            for key, value in updates.items():
                if key not in ['role_id', 'organisation_id', 'centre_id']:
                    setattr(utilisateur, key, value)

            db.commit()
            db.refresh(utilisateur)
            return {"code": 200, "message": "Utilisateur mis à jour", "data": UtilisateurRead.from_orm(utilisateur)}
        
        except IntegrityError as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur d'intégrité lors de la mise à jour: {str(e)}", "data": None}
        
        except Exception as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur inattendue: {str(e)}", "data": None}
    @staticmethod
    def delete_utilisateur(db: Session, utilisateur_id: int):
        utilisateur = db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
        if not utilisateur:
            return {"code": 404, "message": "Utilisateur non trouvé", "data": None}
        try:
            db.delete(utilisateur)
            db.commit()
            return {"code": 200, "message": "Utilisateur supprimé", "data": None}
        except IntegrityError as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur lors de la suppression de l'utilisateur: {str(e)}", "data": None}
        except Exception as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur inattendue: {str(e)}", "data": None}

    @staticmethod
    def assign_user_to_organisation(db: Session, assigner_id: int, utilisateur_id: int, organisation_id: int):
        # Recherche de l'utilisateur assignant
        assigner = db.query(Utilisateur).filter(Utilisateur.id == assigner_id).first()
        if not assigner:
            return {"code": 404, "message": "Utilisateur assignant non trouvé", "data": None}

        # Recherche de l'utilisateur à affecter
        utilisateur = db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
        if not utilisateur:
            return {"code": 404, "message": "Utilisateur à affecter non trouvé", "data": None}

        # Recherche de l'organisation
        organisation = db.query(Organisation).filter(Organisation.id == organisation_id).first()
        if not organisation:
            return {"code": 404, "message": "Organisation non trouvée", "data": None}

        # Mise à jour de l'utilisateur
        utilisateur.organisation_id = organisation.id
        utilisateur.organisation_affecte_par_id = assigner.id
        utilisateur.date_affectation_organisation = datetime.now()
        
        # Enregistrement dans la base de données
        db.commit()
        db.refresh(utilisateur)

        return {"code": 200, "message": "Utilisateur affecté à l'organisation", "data": UtilisateurRead.from_orm(utilisateur)}

    @staticmethod
    def assign_user_to_centre(db: Session, assigner_id: int, utilisateur_id: int, centre_id: int):
        # Trouver l'utilisateur qui effectue l'assignation
        assigner = db.query(Utilisateur).filter(Utilisateur.id == assigner_id).first()
        if not assigner:
            return {"code": 404, "message": f"L'utilisateur assignant avec l'ID {assigner_id} n'a pas été trouvé dans votre organisation. Veuillez vérifier les informations fournies.", "data": None}
        # Trouver l'utilisateur à assigner
        utilisateur = db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
        if not utilisateur:
            return {"code": 404, "message": f"L'utilisateur à affecter avec l'ID {utilisateur_id} n'a pas été trouvé dans votre organisation. Merci de vérifier son identité.", "data": None}
        # Trouver le centre
        centre = db.query(CentreEtatCivil).filter(CentreEtatCivil.id == centre_id).first()
        if not centre:
            return {"code": 404, "message": f"Le centre d'état civil avec l'ID {centre_id} n'existe pas dans la base de données de votre organisation. Veuillez vérifier les informations du centre.", "data": None}
        # Effectuer l'assignation
        utilisateur.centre_id = centre_id
        db.commit()
        # Retourner directement l'entité utilisateur après l'assignation
        return {"code": 200, "message": f"L'utilisateur {utilisateur.nom} a été affecté avec succès au centre {centre.nom}.", "data": UtilisateurRead.from_orm(utilisateur)}

    @staticmethod
    def assign_permissions_to_user(db: Session, assigner_id: int, utilisateur_id: int, permissions: list):
        assigner = db.query(Utilisateur).filter(Utilisateur.id == assigner_id).first()
        if not assigner:
            return {"code": 404, "message": "Utilisateur assignant non trouvé", "data": None}
        
        utilisateur = db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
        if not utilisateur:
            return {"code": 404, "message": "Utilisateur à affecter non trouvé", "data": None}

        for perm_id in permissions:
            permission = db.query(Permission).filter(Permission.id == perm_id).first()
            if permission:
                if permission not in utilisateur.permissions:
                    utilisateur.permissions.append(permission)
            else:
                return {"code": 404, "message": f"Permission avec l'ID {perm_id} non trouvée", "data": None}

        try:
            db.commit()
            db.refresh(utilisateur)
            return {"code": 200, "message": f"Permissions assignées à {utilisateur.nom} {utilisateur.prenom}", "data": utilisateur}
        except IntegrityError as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur d'intégrité lors de l'assignation des permissions: {str(e)}", "data": None}
        except Exception as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur inattendue lors de l'assignation des permissions: {str(e)}", "data": None}
    
    @staticmethod
    def change_role(db: Session, utilisateur_id: int, new_role_id: int):
        """
        Change le rôle d'un utilisateur.
        Vérifie que l'utilisateur et le nouveau rôle existent, met à jour et retourne l'utilisateur modifié.
        """
        utilisateur = db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
        if not utilisateur:
            return {"code": 404, "message": "Utilisateur non trouvé", "data": None}
        
        role = db.query(Role).filter(Role.id == new_role_id).first()
        if not role:
            return {"code": 404, "message": "Rôle non trouvé", "data": None}

        utilisateur.role_id = new_role_id
        try:
            db.commit()
            db.refresh(utilisateur)
            return {"code": 200, "message": "Rôle mis à jour avec succès", "data": UtilisateurRead.from_orm(utilisateur)}
        except IntegrityError as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur d'intégrité lors de la mise à jour du rôle: {str(e)}", "data": None}
        except Exception as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur inattendue: {str(e)}", "data": None}

    def remove_utilisateur_from_centre(self, utilisateur_id: int):
        utilisateur = self.db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
        if not utilisateur:
            return {"code": 404, "message": "Utilisateur non trouvé", "data": None}
        try:
            # Retirer l'utilisateur de son centre
            utilisateur.centre_id = None
            self.db.commit()
            self.db.refresh(utilisateur)
            # Convertir en dict et supprimer la clé non sérialisable
            utilisateur_data = utilisateur.__dict__.copy()
            utilisateur_data.pop('_sa_instance_state', None)
            return {"code": 200, "message": "Utilisateur retiré de son centre d'état civil", "data": utilisateur_data}
        except Exception as e:
            self.db.rollback()
            return {"code": 500, "message": f"Erreur lors du retrait de l'utilisateur de son centre d'état civil: {str(e)}", "data": None}
