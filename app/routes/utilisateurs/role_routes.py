from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.schemas.utilisateurs.role_schema import RoleCreate, RoleRead
from app.services.utilisateurs.role_service import RoleService

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)

@router.post("", summary="Créer un rôle", response_model=RoleRead)
def create_role(role_in: RoleCreate, db: Session = Depends(get_db)):
    response = RoleService.create_role(db, role_in)
    if response["code"] != 201:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response["data"]

@router.get("/{role_id}", summary="Obtenir un rôle par ID", response_model=RoleRead)
def get_role_by_id(role_id: int, db: Session = Depends(get_db)):
    response = RoleService.get_role_by_id(db, role_id)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response["data"]

@router.get("", summary="Obtenir tous les rôles", response_model=list[RoleRead])
def get_all_roles(db: Session = Depends(get_db)):
    response = RoleService.get_all_roles(db)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response["data"]

@router.put("/{role_id}/permissions", summary="Assigner des permissions à un rôle", response_model=RoleRead)
def assign_permissions_to_role(role_id: int, permission_ids: list[int], db: Session = Depends(get_db)):
    response = RoleService.assign_permissions_to_role(db, role_id, permission_ids)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response["data"]

@router.put("/{role_id}/permissions/remove", summary="Retirer des permissions d'un rôle", response_model=RoleRead)
def remove_permissions_from_role(role_id: int, permission_ids: list[int], db: Session = Depends(get_db)):
    response = RoleService.remove_permissions_from_role(db, role_id, permission_ids)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response["data"]

@router.delete("/{role_id}", summary="Supprimer un rôle")
def delete_role(role_id: int, db: Session = Depends(get_db)):
    response = RoleService.delete_role(db, role_id)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return {"message": response["message"]}
