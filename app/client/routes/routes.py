# app/api/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.client.schemas.client import ClientCreate
from app.client.schemas.session import SessionCreate
from app.client.services.client_service import ClientService
from app.client.services.session_service import SessionService
from app.config.utils.dependencies import verify_token  
router = APIRouter()

# --------------------------------------------------
# Routes "libres" (sans token)
# --------------------------------------------------

@router.post("/clients", tags=["Free"], summary="Créer un client et une session associée")
def create_client_and_session(client_data: ClientCreate, db: Session = Depends(get_db)):
    service = ClientService(db)
    result = service.create_client_and_session(client_data)
    return result

@router.put("/clients/{client_id}/session/{session_id}/activate", tags=["Free"], summary="Activer la session d'un client")
def activate_client_session(client_id: int, session_id: int, otp_code: str, db: Session = Depends(get_db)):
    """
    Active la session pour le client en validant le code OTP fourni.
    Endpoint libre.
    """
    service = ClientService(db)
    result = service.activate_client_session(client_id, session_id, otp_code)
    if result.get("code") != 200:
        raise HTTPException(status_code=result.get("code"), detail=result.get("message"))
    return result

# --------------------------------------------------
# Routes sécurisées (token requis)
# --------------------------------------------------

# Endpoints Clients
@router.get("/clients/{client_id}", tags=["Clients"], summary="Récupérer un client par son ID")
def get_client_by_id(client_id: int, token: dict = Depends(verify_token), db: Session = Depends(get_db)):
    service = ClientService(db)
    result = service.get_client_by_id(client_id)
    if result.get("code") != 200:
        raise HTTPException(status_code=result.get("code"), detail=result.get("message"))
    return result

@router.get("/clients/email/{email}", tags=["Clients"], summary="Récupérer un client par son e-mail")
def get_client_by_email(email: str, token: dict = Depends(verify_token), db: Session = Depends(get_db)):
    service = ClientService(db)
    result = service.get_client_by_email(email)
    if result.get("code") != 200:
        raise HTTPException(status_code=result.get("code"), detail=result.get("message"))
    return result

@router.get("/clients/phone/{phone}", tags=["Clients"], summary="Récupérer un client par son numéro de téléphone")
def get_client_by_phone(phone: str, token: dict = Depends(verify_token), db: Session = Depends(get_db)):
    service = ClientService(db)
    result = service.get_client_by_phone(phone)
    if result.get("code") != 200:
        raise HTTPException(status_code=result.get("code"), detail=result.get("message"))
    return result

@router.get("/clients", tags=["Clients"], summary="Récupérer tous les clients")
def get_all_clients(token: dict = Depends(verify_token), db: Session = Depends(get_db)):
    service = ClientService(db)
    result = service.get_all_clients()
    return result

@router.get("/clients/{client_id}/sessions", tags=["Sessions-Clients"], summary="Récupérer toutes les sessions d'un client (actives/inactives)")
def get_sessions_by_client(client_id: int, token: dict = Depends(verify_token), db: Session = Depends(get_db)):
    """
    Récupère toutes les sessions d'un client donné, séparées en sessions actives et inactives.
    """
    service = SessionService(db)
    result = service.get_sessions_by_client(client_id)
    return result

@router.delete("/clients/{client_id}", tags=["Clients"], summary="Supprimer un client")
def delete_client(client_id: int, token: dict = Depends(verify_token), db: Session = Depends(get_db)):
    service = ClientService(db)
    result = service.delete_client(client_id)
    if result.get("code") != 200:
        raise HTTPException(status_code=result.get("code"), detail=result.get("message"))
    return result

# Endpoints Sessions
@router.get("/sessions/{session_id}", tags=["Sessions-Clients"], summary="Récupérer une session par son ID")
def get_session_by_id(session_id: int, token: dict = Depends(verify_token), db: Session = Depends(get_db)):
    service = SessionService(db)
    result = service.get_session_by_id(session_id)
    if result.get("code") != 200:
        raise HTTPException(status_code=result.get("code"), detail=result.get("message"))
    return result

@router.get("/sessions", tags=["Sessions-Clients"], summary="Récupérer toutes les sessions")
def get_all_sessions(token: dict = Depends(verify_token), db: Session = Depends(get_db)):
    service = SessionService(db)
    result = service.get_all_sessions()
    return result

@router.delete("/sessions/{session_id}", tags=["Sessions-Clients"], summary="Supprimer une session")
def delete_session(session_id: int, token: dict = Depends(verify_token), db: Session = Depends(get_db)):
    service = SessionService(db)
    result = service.delete_session(session_id)
    if result.get("code") != 200:
        raise HTTPException(status_code=result.get("code"), detail=result.get("message"))
    return result
