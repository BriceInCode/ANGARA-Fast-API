from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.services.clients.otp_services import OTPService

router = APIRouter(
    prefix="/otp",
    tags=["OTP"]
)

@router.post("/{session_id}", summary="Créer un OTP pour une session", description="Génère un OTP pour une session client.")
def create_otp_for_session(session_id: int, db: Session = Depends(get_db)):
    service = OTPService(db)
    response = service.create_otp_for_session(session_id)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response

@router.get("/{session_id}", summary="Obtenir un OTP par session", description="Retourne un OTP pour une session donnée.")
def get_otp_by_session_id(session_id: int, db: Session = Depends(get_db)):
    service = OTPService(db)
    response = service.get_otp_by_session_id(session_id)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response

@router.post("/{session_id}/validate", summary="Valider un OTP", description="Vérifie si un OTP est valide pour une session.")
def validate_otp(session_id: int, otp_code: str, db: Session = Depends(get_db)):
    service = OTPService(db)
    response = service.validate_otp(session_id, otp_code)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response
