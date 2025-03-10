# app/client/services/session_service.py
import jwt
from sqlalchemy.orm import Session
from app.client.models.session import Session as SessionModel
from app.client.schemas.session import SessionCreate
from datetime import datetime, timedelta
from typing import List, Optional
from app.client.services.otp_service import OTPService
from app.config.settings import settings

ALGORITHM = "HS256"

class SessionService:
    def __init__(self, db: Session):
        self.db = db

    def create_session(self, session_data: SessionCreate) -> dict:
        """
        Crée une nouvelle session pour le client.
        Si une session active existe et n'est pas expirée, elle est retournée.
        Si la session active est expirée, elle est marquée comme inactive puis une nouvelle session est créée.
        """
        now = datetime.utcnow()

        # Récupérer la première session active du client
        active_session = self.db.query(SessionModel).filter(
            SessionModel.client_id == session_data.client_id,
            SessionModel.is_active.is_(True)
        ).first()

        if active_session:
            # Si la session active est expirée, on la marque comme inactive
            if active_session.expires_at < now:
                active_session.is_active = False
                active_session.expires_at = now - timedelta(seconds=10)
                self.db.commit()
                self.db.refresh(active_session)
            else:
                return {
                    "code": 200,
                    "message": "Une session active existe déjà",
                    "data": active_session
                }

        # Désactiver toutes les sessions actives du client (pour être certain)
        self.deactivate_all_sessions(session_data.client_id)

        # Créer une nouvelle session active
        new_session = SessionModel(client_id=session_data.client_id, is_active=False)
        self.db.add(new_session)
        self.db.commit()
        self.db.refresh(new_session)

        # Créer l'OTP associé à cette session (envoi immédiat s'il y a email)
        OTPService(self.db).create_otp(new_session.id)

        return {
            "code": 200,
            "message": "Nouvelle session créée avec succès",
            "data": new_session
        }

    def deactivate_all_sessions(self, client_id: int) -> dict:
        self.db.query(SessionModel).filter(
            SessionModel.client_id == client_id,
            SessionModel.is_active.is_(True)
        ).update({
            SessionModel.is_active: False,
            SessionModel.expires_at: datetime.utcnow() - timedelta(seconds=2)
        }, synchronize_session=False)
        self.db.commit()
        return {
            "code": 200,
            "message": "Toutes les sessions ont été désactivées",
            "data": None
        }

    def get_session_by_id(self, session_id: int) -> dict:
        session = self.db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if session:
            return {
                "code": 200,
                "message": "Session trouvée",
                "data": session
            }
        return {
            "code": 404,
            "message": "Session non trouvée",
            "data": None
        }

    def get_all_sessions(self) -> dict:
        sessions = self.db.query(SessionModel).all()
        return {
            "code": 200,
            "message": "Sessions récupérées avec succès",
            "data": sessions
        }

    def delete_session(self, session_id: int) -> dict:
        db_session = self.db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if db_session:
            self.db.delete(db_session)
            self.db.commit()
            return {
                "code": 200,
                "message": "Session supprimée avec succès",
                "data": db_session
            }
        return {
            "code": 404,
            "message": "Session non trouvée",
            "data": None
        }

    def generate_token(self, email: str, expires_at: datetime) -> str:
        """Génère un token JWT basé sur l'email et la date d'expiration."""
        payload = {"email": email, "exp": expires_at}
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)
    
    def activate_session(self, session_id: int, otp_code: str) -> dict:
        """
        Active la session identifiée après validation de l'OTP.
        Si l'OTP fourni correspond à celui enregistré et n'est pas expiré,
        désactive les autres sessions et active celle-ci, puis génère un token.
        """
        now = datetime.utcnow()
        session_result = self.get_session_by_id(session_id)
        db_session = session_result.get("data")
        if not db_session:
            return {
                "code": 404,
                "message": "Session non trouvée",
                "data": None
            }

        # Valider l'OTP via le service OTP
        otp_service = OTPService(self.db)
        otp_validation = otp_service.validate_otp(session_id, otp_code)
        if otp_validation.get("code") != 200:
            return {
                "code": 400,
                "message": "OTP invalide ou expiré",
                "data": None
            }

        # OTP validé : désactiver toutes les sessions actives du client
        self.deactivate_all_sessions(db_session.client_id)

        # Activer la session et mettre à jour la base
        db_session.is_active = True
        self.db.commit()
        self.db.refresh(db_session)

        # Générer le token si l'email est disponible
        token = None
        if db_session.client and db_session.client.email:
            token = self.generate_token(db_session.client.email, db_session.expires_at)

        return {
            "code": 200,
            "message": "Session activée avec succès",
            "data": {"session": db_session, "token": token}
        }
