from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.schemas.clients.session_schema import SessionCreate
from app.services.clients.session_services import SessionService

router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"]
)

@router.post("", summary="Créer une session", description="Crée une nouvelle session pour un client.")
def create_session(session_in: SessionCreate, db: Session = Depends(get_db)):
    service = SessionService(db)
    response = service.create_session(session_in)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response

@router.post("/{session_id}/activate", summary="Activer une session", description="Active une session avec un OTP.")
def activate_session(session_id: int, otp_code: str, db: Session = Depends(get_db)):
    service = SessionService(db)
    response = service.activate_session(session_id, otp_code)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response

@router.get("/{session_id}", summary="Obtenir une session", description="Retourne une session via son identifiant.")
def get_session_by_id(session_id: int, db: Session = Depends(get_db)):
    service = SessionService(db)
    response = service.get_session_by_id(session_id)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response

@router.get("/client/{client_id}", summary="Obtenir les sessions d'un client", description="Retourne toutes les sessions d'un client.")
def get_sessions_by_client(client_id: int, db: Session = Depends(get_db)):
    service = SessionService(db)
    response = service.get_sessions_by_client(client_id)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response
