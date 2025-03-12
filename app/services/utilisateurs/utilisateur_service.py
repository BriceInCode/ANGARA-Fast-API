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
        return ''.join(random.choice(characters) for i in range(length))

    @staticmethod
    def hash_password(password: str):
        """Hash le mot de passe généré"""
        return pwd_context.hash(password)

    @staticmethod
    def send_welcome_email(email: str, role_name: str, mot_de_passe: str):
        """Envoie un email de bienvenue avec le mot de passe et le rôle"""
        # Déterminer si c'est le matin ou le soir
        current_hour = datetime.now().hour
        salutation = "Bonjour" if current_hour < 18 else "Bonsoir"
        
        # Construire le contenu du message
        subject = "Compte utilisateur créé"
        body = (
            f"{salutation} Ms/Mme/Mlle...,\n\n"
            f"Nous vous informons qu'un compte utilisateur vous a été créé en tant que {role_name}.\n\n"
            f"Votre mot de passe est le suivant : {mot_de_passe}\n\n"
            "Veuillez le garder en sécurité et le changer dès que possible. \n\n\n"
            "ANGARA AUTHENTIC. \n\n "
        )
        return EmailService().send_email(email, subject, body)

    @staticmethod
    def create_utilisateur(db: Session, utilisateur_data: UtilisateurCreate):
        try:
            # Vérifier si l'email est déjà utilisé
            if db.query(Utilisateur).filter(Utilisateur.email == utilisateur_data.email).first():
                return {"code": 409, "message": "L'email est déjà utilisé.", "data": None}

            # Vérifier si le rôle et l'organisation existent
            role = db.query(Role).filter(Role.id == utilisateur_data.role_id).first()
            if not role:
                return {"code": 404, "message": "Rôle non trouvé", "data": None}

            organisation = db.query(Organisation).filter(Organisation.id == utilisateur_data.organisation_id).first()
            if not organisation:
                return {"code": 404, "message": "Organisation non trouvée", "data": None}

            # Générer un mot de passe aléatoire pour l'utilisateur
            mot_de_passe = UtilisateurService.generate_password()

            # Hacher le mot de passe avant de l'affecter à l'utilisateur
            hashed_password = UtilisateurService.hash_password(mot_de_passe)

            # Créer l'utilisateur, en s'assurant que le statut est ACTIF par défaut
            utilisateur_data.status = ComptesEnum.ACTIF  # S'assurer que le statut est ACTIF si non spécifié
            new_utilisateur = Utilisateur(**utilisateur_data.dict(), mot_de_passe=hashed_password)
            db.add(new_utilisateur)
            db.commit()
            db.refresh(new_utilisateur)

            # Envoyer l'email de bienvenue avec le mot de passe et le rôle
            success = UtilisateurService.send_welcome_email(utilisateur_data.email, role.nom, mot_de_passe)
            message = "Utilisateur créé avec succès, email envoyé" if success else "Utilisateur créé avec succès, mais l'email n'a pas pu être envoyé"

            return {"code": 201, "message": message, "data": UtilisateurRead.from_orm(new_utilisateur)}
        except IntegrityError as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur d'intégrité lors de la création de l'utilisateur: {str(e)}", "data": None}
        except Exception as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur inattendue: {str(e)}", "data": None}

    @staticmethod
    def get_utilisateur(db: Session, param: str):
        # Vérifier si le paramètre est un ID (un entier) ou un email
        utilisateur = None
        if param.isdigit():  # Si le paramètre est un ID (c'est-à-dire un nombre entier)
            utilisateur = db.query(Utilisateur).filter(Utilisateur.id == int(param)).first()
        else:  # Si le paramètre est un email (string)
            utilisateur = db.query(Utilisateur).filter(Utilisateur.email == param).first()

        if utilisateur:
            return {"code": 200, "message": "Utilisateur trouvé", "data": UtilisateurRead.from_orm(utilisateur)}
        return {"code": 404, "message": "Utilisateur non trouvé", "data": None}


    @staticmethod
    def get_all_utilisateurs(db: Session):
        utilisateurs = db.query(Utilisateur).all()
        return {"code": 200, "message": "Liste des utilisateurs récupérée", "data": [UtilisateurRead.from_orm(u) for u in utilisateurs]}

    @staticmethod
    def get_utilisateurs_by_role(db: Session, role: str):
        # Vérifier si le paramètre est un entier (id du rôle) ou une chaîne (nom du rôle)
        if isinstance(role, int):
            # Si le paramètre est un entier, c'est l'ID du rôle
            utilisateurs = db.query(Utilisateur).filter(Utilisateur.role_id == role).all()
        else:
            # Si le paramètre est une chaîne, c'est le nom du rôle
            role_obj = db.query(Role).filter(Role.id == role).first()
            if role_obj:
                utilisateurs = db.query(Utilisateur).filter(Utilisateur.role_id == role_obj.id).all()
            else:
                return {"code": 404, "message": "Rôle non trouvé", "data": None}
        
        if utilisateurs:
            return {"code": 200, "message": "Utilisateurs trouvés", "data": [UtilisateurRead.from_orm(utilisateur) for utilisateur in utilisateurs]}
        return {"code": 404, "message": "Aucun utilisateur trouvé pour ce rôle", "data": None}

    @staticmethod
    def get_utilisateurs_by_organisation(db: Session, organisation: str):
        # Vérifier si le paramètre est un entier (id de l'organisation), une chaîne (nom ou référence)
        if isinstance(organisation, int):
            # Si le paramètre est un entier, c'est l'ID de l'organisation
            utilisateurs = db.query(Utilisateur).filter(Utilisateur.organisation_id == organisation).all()
        else:
            # Si le paramètre est une chaîne, il peut être soit le nom, soit la référence de l'organisation
            organisation_obj = db.query(Organisation).filter(
                (Organisation.nom == organisation) | (Organisation.reference == organisation)
            ).first()

            if organisation_obj:
                utilisateurs = db.query(Utilisateur).filter(Utilisateur.organisation_id == organisation_obj.id).all()
            else:
                return {"code": 404, "message": "Organisation non trouvée", "data": None}
        
        if utilisateurs:
            return {"code": 200, "message": "Utilisateurs trouvés", "data": [UtilisateurRead.from_orm(utilisateur) for utilisateur in utilisateurs]}
        return {"code": 404, "message": "Aucun utilisateur trouvé pour cette organisation", "data": None}

    @staticmethod
    def get_utilisateurs_by_centre(db: Session, centre: str):
        # Vérifier si le paramètre est un entier (id du centre), ou une chaîne (référence, nom, email, téléphone)
        if isinstance(centre, int):
            # Si le paramètre est un entier, c'est l'ID du centre
            utilisateurs = db.query(Utilisateur).filter(Utilisateur.centre_id == centre).all()
        else:
            # Si le paramètre est une chaîne, il peut être la référence, le nom, l'email ou le téléphone du centre
            centre_obj = db.query(CentreEtatCivil).filter(
                (CentreEtatCivil.id == centre) |  # Recherche par ID
                (CentreEtatCivil.reference == centre) | 
                (CentreEtatCivil.nom == centre) | 
                (CentreEtatCivil.email == centre) | 
                (CentreEtatCivil.telephone == centre)
            ).first()

            if centre_obj:
                utilisateurs = db.query(Utilisateur).filter(Utilisateur.centre_id == centre_obj.id).all()
            else:
                return {"code": 404, "message": "Centre d'état civil non trouvé", "data": None}
        
        if utilisateurs:
            return {"code": 200, "message": "Utilisateurs trouvés", "data": [UtilisateurRead.from_orm(utilisateur) for utilisateur in utilisateurs]}
        return {"code": 404, "message": "Aucun utilisateur trouvé pour ce centre d'état civil", "data": None}


    @staticmethod
    def update_utilisateur(db: Session, utilisateur_id: int, updates: dict):
        utilisateur = db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
        if not utilisateur:
            return {"code": 404, "message": "Utilisateur non trouvé", "data": None}
        
        try:
            # Vérifier si le rôle et l'organisation existent
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
            
            # Si un centre d'état civil est renseigné, vérifier s'il existe
            if 'centre_id' in updates:
                centre = db.query(CentreEtatCivil).filter(CentreEtatCivil.id == updates['centre_id']).first()
                if not centre:
                    return {"code": 404, "message": "Centre d'état civil non trouvé", "data": None}
                utilisateur.centre_id = updates['centre_id']
            
            # Appliquer les autres mises à jour
            for key, value in updates.items():
                if key not in ['role_id', 'organisation_id', 'centre_id']:  # Ces champs sont déjà traités
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
        """Affecter un utilisateur à une organisation, en prenant en compte l'utilisateur assignant et l'utilisateur affecté"""
        
        # Vérifier si l'utilisateur qui effectue l'affectation existe
        assigner = db.query(Utilisateur).filter(Utilisateur.id == assigner_id).first()
        if not assigner:
            return {"code": 404, "message": "Utilisateur assignant non trouvé", "data": None}
        
        # Vérifier si l'utilisateur à affecter existe
        utilisateur = db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
        if not utilisateur:
            return {"code": 404, "message": "Utilisateur à affecter non trouvé", "data": None}
        
        # Vérifier si l'organisation existe
        organisation = db.query(Organisation).filter(Organisation.id == organisation_id).first()
        if not organisation:
            return {"code": 404, "message": "Organisation non trouvée", "data": None}
        
        # Affecter l'organisation à l'utilisateur
        utilisateur.organisation_id = organisation.id
        utilisateur.organisation_affecte_par_id = assigner.id  # Enregistrer l'utilisateur assignant
        utilisateur.date_affectation_organisation = datetime.now()  # Enregistrer la date d'affectation
        db.commit()
        db.refresh(utilisateur)

        return {"code": 200, "message": "Utilisateur affecté à l'organisation", "data": UtilisateurRead.from_orm(utilisateur)}


    @staticmethod
    def assign_user_to_centre(db: Session, assigner_id: int, utilisateur_id: int, centre_id: int):
        """Affecter un utilisateur à un centre, en prenant en compte l'utilisateur assignant et l'utilisateur affecté"""
        
        # Vérifier si l'utilisateur qui effectue l'affectation existe
        assigner = db.query(Utilisateur).filter(Utilisateur.id == assigner_id).first()
        if not assigner:
            return {"code": 404, "message": "Utilisateur assignant non trouvé", "data": None}
        
        # Vérifier si l'utilisateur à affecter existe
        utilisateur = db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
        if not utilisateur:
            return {"code": 404, "message": "Utilisateur à affecter non trouvé", "data": None}
        
        # Vérifier si le centre existe
        centre = db.query(CentreEtatCivil).filter(CentreEtatCivil.id == centre_id).first()
        if not centre:
            return {"code": 404, "message": "Centre non trouvé", "data": None}
        
        # Affecter le centre à l'utilisateur
        utilisateur.centre_id = centre.id
        utilisateur.centre_affecte_par_id = assigner.id  # Enregistrer l'utilisateur assignant
        utilisateur.date_affectation_centre = datetime.now()  # Enregistrer la date d'affectation
        db.commit()
        db.refresh(utilisateur)

        return {"code": 200, "message": "Utilisateur affecté au centre", "data": UtilisateurRead.from_orm(utilisateur)}

    @staticmethod
    def assign_permissions_to_user(db: Session, assigner_id: int, utilisateur_id: int, permissions: list):
        """
        Assigner des permissions à un utilisateur.
        
        :param db: Session SQLAlchemy
        :param assigner_id: ID de l'utilisateur qui effectue l'assignation
        :param utilisateur_id: ID de l'utilisateur auquel on assigne les permissions
        :param permissions: Liste des permissions à attribuer
        :return: Dictionnaire avec code de statut et message
        """
        
        # Vérifier si l'utilisateur assignant existe
        assigner = db.query(Utilisateur).filter(Utilisateur.id == assigner_id).first()
        if not assigner:
            return {"code": 404, "message": "Utilisateur assignant non trouvé", "data": None}

        # Vérifier si l'utilisateur à affecter existe
        utilisateur = db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
        if not utilisateur:
            return {"code": 404, "message": "Utilisateur à affecter non trouvé", "data": None}

        # Vérifier si l'utilisateur assignant a les droits nécessaires
        # if assigner.role.nom not in ['SUPER_ADMINISTRATEUR', 'ADMINISTRATEUR']:
        #     return {"code": 403, "message": "L'utilisateur assignant n'a pas les droits nécessaires pour assigner des permissions", "data": None}

        # Vérifier si les permissions existent et ajouter
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