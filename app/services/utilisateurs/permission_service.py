from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.utilisateurs.permission import Permission
from app.schemas.utilisateurs.permission_schema import PermissionCreate, PermissionRead

class PermissionService:
    @staticmethod
    def create_permission(db: Session, permission_data: PermissionCreate):
        try:
            # Vérifie si une permission avec ce nom existe déjà
            existing = db.query(Permission).filter(Permission.nom == permission_data.nom).first()
            if existing:
                return {"code": 409, "message": "La permission existe déjà.", "data": None}
            new_permission = Permission(**permission_data.dict())
            db.add(new_permission)
            db.commit()
            db.refresh(new_permission)
            return {"code": 201, "message": "Permission créée avec succès", "data": PermissionRead.from_orm(new_permission)}
        except IntegrityError as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur d'intégrité lors de la création de la permission: {str(e)}", "data": None}
        except Exception as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur inattendue: {str(e)}", "data": None}

    @staticmethod
    def get_permission_by_id(db: Session, permission_id: int):
        permission = db.query(Permission).filter(Permission.id == permission_id).first()
        if permission:
            return {"code": 200, "message": "Permission trouvée", "data": PermissionRead.from_orm(permission)}
        return {"code": 404, "message": "Permission non trouvée", "data": None}

    @staticmethod
    def get_all_permissions(db: Session):
        permissions = db.query(Permission).all()
        return {"code": 200, "message": "Liste des permissions récupérée", "data": [PermissionRead.from_orm(p) for p in permissions]}

    @staticmethod
    def update_permission(db: Session, permission_id: int, updates: dict):
        permission = db.query(Permission).filter(Permission.id == permission_id).first()
        if not permission:
            return {"code": 404, "message": "Permission non trouvée", "data": None}
        try:
            for key, value in updates.items():
                setattr(permission, key, value)
            db.commit()
            db.refresh(permission)
            return {"code": 200, "message": "Permission mise à jour", "data": PermissionRead.from_orm(permission)}
        except IntegrityError as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur d'intégrité lors de la mise à jour: {str(e)}", "data": None}
        except Exception as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur inattendue: {str(e)}", "data": None}

    @staticmethod
    def delete_permission(db: Session, permission_id: int):
        permission = db.query(Permission).filter(Permission.id == permission_id).first()
        if not permission:
            return {"code": 404, "message": "Permission non trouvée", "data": None}
        try:
            db.delete(permission)
            db.commit()
            return {"code": 200, "message": "Permission supprimée avec succès", "data": None}
        except IntegrityError as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur lors de la suppression de la permission: {str(e)}", "data": None}
        except Exception as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur inattendue: {str(e)}", "data": None}
