from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.schemas.utilisateurs.utilisateur_schema import UtilisateurRead
from app.services.utilisateurs.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentification"]
)

@router.post("/login", summary="Authentifier un utilisateur", description="Authentifie un utilisateur avec son email et mot de passe.")
def login_user(email: str, password: str, db: Session = Depends(get_db)):
    response = AuthService.authenticate_user(db, email, password)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response

@router.post("/logout", summary="Déconnexion d'un utilisateur", description="Déconnecte un utilisateur en invalidant son token.")
def logout_user(user_id: str, token: str, db: Session = Depends(get_db)):
    response = AuthService.logout_user(user_id, token)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response

@router.get("/check_token", summary="Vérifier si un token est valide", description="Vérifie si un token donné est dans la liste noire.")
def check_token(user_id: str, token: str, db: Session = Depends(get_db)):
    is_blacklisted = AuthService.is_token_blacklisted(user_id, token)
    return {"blacklisted": is_blacklisted}
