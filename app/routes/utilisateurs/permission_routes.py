from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.schemas.utilisateurs.permission_schema import PermissionCreate, PermissionRead
from app.services.utilisateurs.permission_service import PermissionService

router = APIRouter(
    prefix="/permissions",
    tags=["Permissions"]
)

@router.post("", summary="Créer une permission", description="Crée une nouvelle permission.")
def create_permission(permission_data: PermissionCreate, db: Session = Depends(get_db)):
    response = PermissionService.create_permission(db, permission_data)
    if response["code"] != 201:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response

@router.get("/{permission_id}", summary="Obtenir une permission par ID", description="Retourne une permission via son identifiant unique.")
def get_permission_by_id(permission_id: int, db: Session = Depends(get_db)):
    response = PermissionService.get_permission_by_id(db, permission_id)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response

@router.get("", summary="Obtenir toutes les permissions", description="Retourne une liste de toutes les permissions.")
def get_all_permissions(db: Session = Depends(get_db)):
    response = PermissionService.get_all_permissions(db)
    return response

@router.put("/{permission_id}", summary="Mettre à jour une permission", description="Met à jour une permission existante.")
def update_permission(permission_id: int, updates: dict, db: Session = Depends(get_db)):
    response = PermissionService.update_permission(db, permission_id, updates)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response

@router.delete("/{permission_id}", summary="Supprimer une permission", description="Supprime une permission par son identifiant.")
def delete_permission(permission_id: int, db: Session = Depends(get_db)):
    response = PermissionService.delete_permission(db, permission_id)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response
