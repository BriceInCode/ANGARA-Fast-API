from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.schemas.organisations.centre_etat_civil_schema import CentreEtatCivilCreate
from app.services.organisations.centre_etat_civil_service import CentreEtatCivilService

router = APIRouter(
    prefix="/centres-etat-civil",
    tags=["Centres d'État Civil"]
)

@router.post("", summary="Créer un centre d'état civil", description="Ajoute un nouveau centre d'état civil.")
def create_centre(centre_in: CentreEtatCivilCreate, db: Session = Depends(get_db)):
    response = CentreEtatCivilService.create_centre(db, centre_in)
    if response["code"] != 201:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response

@router.get("/{centre_id}", summary="Obtenir un centre par ID", description="Récupère un centre d'état civil via son identifiant unique.")
def get_centre_by_id(centre_id: int, db: Session = Depends(get_db)):
    response = CentreEtatCivilService.get_centre_by_id(db, centre_id)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response

@router.get("", summary="Obtenir tous les centres", description="Retourne la liste de tous les centres d'état civil.")
def get_all_centres(db: Session = Depends(get_db)):
    return CentreEtatCivilService.get_all_centres(db)

@router.put("/{centre_id}", summary="Mettre à jour un centre", description="Met à jour les informations d'un centre d'état civil existant.")
def update_centre(centre_id: int, updates: dict, db: Session = Depends(get_db)):
    response = CentreEtatCivilService.update_centre(db, centre_id, updates)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response

@router.delete("/{centre_id}", summary="Supprimer un centre", description="Supprime un centre d'état civil via son identifiant.")
def delete_centre(centre_id: int, db: Session = Depends(get_db)):
    response = CentreEtatCivilService.delete_centre(db, centre_id)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response

@router.get("/{identifier}/utilisateurs", summary="Obtenir les utilisateurs d'un centre", description="Retourne la liste des utilisateurs associés à un centre via son ID, référence, nom, email ou téléphone.")
def get_users_by_centre(identifier: str, db: Session = Depends(get_db)):
    response = CentreEtatCivilService.get_users_by_centre(db, identifier)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response
