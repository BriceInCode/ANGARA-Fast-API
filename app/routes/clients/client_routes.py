from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.schemas.clients.client_schema import ClientCreate
from app.services.clients.client_services import ClientService

router = APIRouter(
    prefix="/clients",
    tags=["Clients"]
)

@router.post("", summary="Créer un client", description="Crée un nouveau client ou retourne un client existant.")
def create_client(client_in: ClientCreate, db: Session = Depends(get_db)):
    service = ClientService(db)
    response = service.create_client(client_in)
    if response["code"] != 201:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response

@router.get("/{client_id}", summary="Obtenir un client par ID", description="Retourne un client via son identifiant unique.")
def get_client_by_id(client_id: int, db: Session = Depends(get_db)):
    service = ClientService(db)
    response = service.get_client_by_id(client_id)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response

@router.get("/email/{email}", summary="Obtenir un client par email", description="Retourne un client via son email.")
def get_client_by_email(email: str, db: Session = Depends(get_db)):
    service = ClientService(db)
    response = service.get_client_by_email(email)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response

@router.get("/phone/{phone}", summary="Obtenir un client par téléphone", description="Retourne un client via son numéro de téléphone.")
def get_client_by_phone(phone: str, db: Session = Depends(get_db)):
    service = ClientService(db)
    response = service.get_client_by_phone(phone)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response
