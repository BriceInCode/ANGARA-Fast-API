from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.configs.enumerations.Comptes import ComptesEnum
from app.schemas.utilisateurs.utilisateur_schema import UtilisateurCreate, UtilisateurRead
from app.services.utilisateurs.utilisateur_service import UtilisateurService

router = APIRouter(prefix="/utilisateurs", tags=["Utilisateurs"])

@router.post("/", response_model=UtilisateurRead, summary="Créer un utilisateur", description="Créer un nouvel utilisateur et envoyer un email de bienvenue")
def create_utilisateur(utilisateur_data: UtilisateurCreate = Body(..., example={
    "nom": "Doe",
    "prenom": "John",
    "email": "john.doe@example.com",
    "role_id": 1,
    "organisation_id": 1,
    "status": ComptesEnum.ACTIF
}), db: Session = Depends(get_db)):
    result = UtilisateurService.create_utilisateur(db, utilisateur_data)
    if result["code"] != 201:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result["data"]

@router.get("/{param}", response_model=UtilisateurRead, summary="Obtenir un utilisateur", description="Obtenir un utilisateur par ID ou par email")
def get_utilisateur(param: str, db: Session = Depends(get_db)):
    result = UtilisateurService.get_utilisateur(db, param)
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result["data"]

@router.get("/", response_model=list[UtilisateurRead], summary="Obtenir tous les utilisateurs", description="Récupérer la liste de tous les utilisateurs")
def get_all_utilisateurs(db: Session = Depends(get_db)):
    result = UtilisateurService.get_all_utilisateurs(db)
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result["data"]

@router.get("/role/{role}", response_model=list[UtilisateurRead], summary="Obtenir des utilisateurs par rôle", description="Récupérer les utilisateurs en fonction de leur rôle")
def get_utilisateurs_by_role(role: str, db: Session = Depends(get_db)):
    result = UtilisateurService.get_utilisateurs_by_role(db, role)
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result["data"]

@router.get("/organisation/{organisation}", response_model=list[UtilisateurRead], summary="Obtenir des utilisateurs par organisation", description="Récupérer les utilisateurs en fonction de leur organisation")
def get_utilisateurs_by_organisation(organisation: str, db: Session = Depends(get_db)):
    result = UtilisateurService.get_utilisateurs_by_organisation(db, organisation)
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result["data"]

@router.get("/centre/{centre}", response_model=list[UtilisateurRead], summary="Obtenir des utilisateurs par centre", description="Récupérer les utilisateurs en fonction de leur centre d'état civil")
def get_utilisateurs_by_centre(centre: str, db: Session = Depends(get_db)):
    result = UtilisateurService.get_utilisateurs_by_centre(db, centre)
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result["data"]

@router.put("/{utilisateur_id}", response_model=UtilisateurRead, summary="Mettre à jour un utilisateur", description="Mettre à jour les informations d'un utilisateur existant")
def update_utilisateur(utilisateur_id: int, updates: UtilisateurCreate = Body(..., example={
    "nom": "Doe",
    "prenom": "John",
    "email": "john.doe@example.com",
    "role_id": 1,
    "organisation_id": 1,
    "status": ComptesEnum.ACTIF
}), db: Session = Depends(get_db)):
    result = UtilisateurService.update_utilisateur(db, utilisateur_id, updates.dict())
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result["data"]

@router.delete("/{utilisateur_id}", summary="Supprimer un utilisateur", description="Supprimer un utilisateur existant")
def delete_utilisateur(utilisateur_id: int, db: Session = Depends(get_db)):
    result = UtilisateurService.delete_utilisateur(db, utilisateur_id)
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result

@router.put("/organisation/assign", summary="Affecter un utilisateur à une organisation", description="Assigner un utilisateur à une organisation en précisant l'utilisateur assignant et l'utilisateur affecté")
def assign_user_to_organisation(data: dict = Body(..., example={
    "assigner_id": 1,
    "utilisateur_id": 2,
    "organisation_id": 1
}), db: Session = Depends(get_db)):
    assigner_id = data.get("assigner_id")
    utilisateur_id = data.get("utilisateur_id")
    organisation_id = data.get("organisation_id")
    if not all([assigner_id, utilisateur_id, organisation_id]):
        raise HTTPException(status_code=400, detail="assigner_id, utilisateur_id et organisation_id sont requis")
    result = UtilisateurService.assign_user_to_organisation(db, assigner_id, utilisateur_id, organisation_id)
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result["data"]

@router.put("/centre/assign", summary="Affecter un utilisateur à un centre", description="Assigner un utilisateur à un centre en précisant l'utilisateur assignant et l'utilisateur affecté")
def assign_user_to_centre(data: dict = Body(..., example={
    "assigner_id": 1,
    "utilisateur_id": 2,
    "centre_id": 1
}), db: Session = Depends(get_db)):
    assigner_id = data.get("assigner_id")
    utilisateur_id = data.get("utilisateur_id")
    centre_id = data.get("centre_id")
    if not all([assigner_id, utilisateur_id, centre_id]):
        raise HTTPException(status_code=400, detail="assigner_id, utilisateur_id et centre_id sont requis")
    result = UtilisateurService.assign_user_to_centre(db, assigner_id, utilisateur_id, centre_id)
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result["data"]

@router.put("/permissions/assign", summary="Affecter des permissions à un utilisateur", description="Assigner des permissions à un utilisateur en précisant l'utilisateur assignant et les permissions à affecter")
def assign_permissions_to_user(data: dict = Body(..., example={
    "assigner_id": 1,
    "utilisateur_id": 2,
    "permissions": [1, 2, 3]
}), db: Session = Depends(get_db)):
    assigner_id = data.get("assigner_id")
    utilisateur_id = data.get("utilisateur_id")
    permissions = data.get("permissions")
    if not all([assigner_id, utilisateur_id, permissions]):
        raise HTTPException(status_code=400, detail="assigner_id, utilisateur_id et permissions sont requis")
    result = UtilisateurService.assign_permissions_to_user(db, assigner_id, utilisateur_id, permissions)
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result["data"]
