from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.utilisateurs.role import Role
from app.schemas.utilisateurs.role_schema import RoleCreate, RoleRead
from app.models.utilisateurs.permission import Permission

class RoleService:
    @staticmethod
    def create_role(db: Session, role_data: RoleCreate):
        try:
            # Vérifier si le rôle existe déjà
            existing = db.query(Role).filter(Role.nom == role_data.nom).first()
            if existing:
                return {"code": 409, "message": "Le rôle existe déjà.", "data": None}
            
            # Créer et ajouter le nouveau rôle
            new_role = Role(**role_data.dict())
            db.add(new_role)
            db.commit()
            db.refresh(new_role)
            
            return {"code": 201, "message": "Rôle créé avec succès", "data": RoleRead.from_orm(new_role)}
        except IntegrityError as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur d'intégrité lors de la création du rôle: {str(e)}", "data": None}
        except Exception as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur inattendue: {str(e)}", "data": None}

    @staticmethod
    def get_role_by_id(db: Session, role_id: int):
        role = db.query(Role).filter(Role.id == role_id).first()
        if role:
            return {"code": 200, "message": "Rôle trouvé", "data": RoleRead.from_orm(role)}
        return {"code": 404, "message": "Rôle non trouvé", "data": None}

    @staticmethod
    def get_all_roles(db: Session):
        roles = db.query(Role).all()
        return {"code": 200, "message": "Liste des rôles récupérée", "data": [RoleRead.from_orm(r) for r in roles]}

    @staticmethod
    def assign_permissions_to_role(db: Session, role_id: int, permission_ids: list):
        """Assigne une liste de permissions à un rôle, en vérifiant qu'elles existent et en évitant les doublons."""
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            return {"code": 404, "message": "Rôle non trouvé", "data": None}

        # Vérifier que toutes les permissions existent
        existing_permissions = db.query(Permission).filter(Permission.id.in_(permission_ids)).all()
        existing_permission_ids = {p.id for p in existing_permissions}

        # Permissions manquantes
        missing_permission_ids = set(permission_ids) - existing_permission_ids
        if missing_permission_ids:
            return {"code": 400, "message": f"Les permissions suivantes n'existent pas: {', '.join(map(str, missing_permission_ids))}", "data": None}

        try:
            # Mettre à jour les permissions du rôle, en supprimant les anciennes et en ajoutant les nouvelles sans doublons
            current_permissions_ids = {p.id for p in role.permissions}
            new_permissions_to_add = [p for p in existing_permissions if p.id not in current_permissions_ids]
            
            # Mettre à jour les permissions du rôle
            role.permissions = new_permissions_to_add
            db.commit()
            db.refresh(role)

            return {"code": 200, "message": "Permissions assignées avec succès", "data": RoleRead.from_orm(role)}
        except IntegrityError as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur d'intégrité lors de l'assignation: {str(e)}", "data": None}
        except Exception as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur inattendue: {str(e)}", "data": None}
        
    @staticmethod
    def remove_permissions_from_role(db: Session, role_id: int, permission_ids: list):
        """Retire une ou plusieurs permissions d'un rôle, en vérifiant qu'elles existent avant de les retirer."""
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            return {"code": 404, "message": "Rôle non trouvé", "data": None}

        # Vérifier que toutes les permissions existent
        existing_permissions = db.query(Permission).filter(Permission.id.in_(permission_ids)).all()
        existing_permission_ids = {p.id for p in existing_permissions}

        # Permissions qui n'existent pas
        non_existing_permission_ids = set(permission_ids) - existing_permission_ids
        if non_existing_permission_ids:
            return {"code": 400, "message": f"Les permissions suivantes n'existent pas: {', '.join(map(str, non_existing_permission_ids))}", "data": None}

        try:
            # Retirer les permissions du rôle
            current_permission_ids = {p.id for p in role.permissions}
            permissions_to_remove = [p for p in role.permissions if p.id in permission_ids]

            # Mettre à jour les permissions du rôle en retirant les permissions demandées
            role.permissions = [p for p in role.permissions if p.id not in permission_ids]
            db.commit()
            db.refresh(role)

            return {"code": 200, "message": "Permissions retirées avec succès", "data": RoleRead.from_orm(role)}
        except IntegrityError as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur d'intégrité lors de la suppression des permissions: {str(e)}", "data": None}
        except Exception as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur inattendue: {str(e)}", "data": None}

    @staticmethod
    def delete_role(db: Session, role_id: int):
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            return {"code": 404, "message": "Rôle non trouvé", "data": None}
        
        try:
            db.delete(role)
            db.commit()
            return {"code": 200, "message": "Rôle supprimé avec succès", "data": None}
        except IntegrityError as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur lors de la suppression du rôle: {str(e)}", "data": None}
        except Exception as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur inattendue: {str(e)}", "data": None}
