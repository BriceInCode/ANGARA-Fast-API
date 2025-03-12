from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.schemas.organisations.organisation_schema import OrganisationCreate
from app.services.organisations.organisation_service import OrganisationService

router = APIRouter(
    prefix="/organisations",
    tags=["Organisations"]
)

@router.post("", summary="Créer une organisation", description="Ajoute une nouvelle organisation.")
def create_organisation(organisation_in: OrganisationCreate, db: Session = Depends(get_db)):
    response = OrganisationService.create_organisation(db, organisation_in)
    if response["code"] != 201:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response

@router.get("/{organisation_id}", summary="Obtenir une organisation par ID", description="Récupère une organisation via son identifiant unique.")
def get_organisation_by_id(organisation_id: int, db: Session = Depends(get_db)):
    response = OrganisationService.get_organisation_by_id(db, organisation_id)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response

@router.get("", summary="Obtenir toutes les organisations", description="Retourne la liste de toutes les organisations.")
def get_all_organisations(db: Session = Depends(get_db)):
    return OrganisationService.get_all_organisations(db)

@router.put("/{organisation_id}", summary="Mettre à jour une organisation", description="Met à jour les informations d'une organisation existante.")
def update_organisation(organisation_id: int, updates: dict, db: Session = Depends(get_db)):
    response = OrganisationService.update_organisation(db, organisation_id, updates)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response

@router.delete("/{organisation_id}", summary="Supprimer une organisation", description="Supprime une organisation via son identifiant.")
def delete_organisation(organisation_id: int, db: Session = Depends(get_db)):
    response = OrganisationService.delete_organisation(db, organisation_id)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response

@router.get("/{identifier}/utilisateurs", summary="Obtenir les utilisateurs d'une organisation", description="Retourne la liste des utilisateurs associés à une organisation via son ID, référence ou nom.")
def get_organisation_users(identifier: str, db: Session = Depends(get_db)):
    response = OrganisationService.get_organisation_users(db, identifier)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response
