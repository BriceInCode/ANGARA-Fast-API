from datetime import datetime, timedelta
from typing import Dict, Any
import jwt
from sqlalchemy.orm import Session
from app.configs.settings import settings
from app.models.clients.client import Client
from app.models.clients.session import Session as ClientSession
from app.schemas.clients.session_schema import SessionCreate
from app.services.clients.otp_services import OTPService

ALGORITHM = "HS256"

class SessionService:
    def __init__(self, db: Session):
        self.db = db
    
    def generate_token(self, email: str, expires_at: datetime) -> str:
        payload = {"email": email, "exp": expires_at}
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)

    def create_session(self, session_in: SessionCreate) -> Dict[str, Any]:
        try:
            client = self.db.query(Client).filter(Client.id == session_in.client_id).first()
            if not client:
                return {"code": 404, "message": "Client introuvable.", "data": None}

            active_session = (
                self.db.query(ClientSession)
                .filter(
                    ClientSession.client_id == session_in.client_id,
                    ClientSession.is_active == True,
                    ClientSession.expires_at > datetime.utcnow()
                )
                .first()
            )
            if active_session:
                return {"code": 200, "message": "Session active trouvée.", "data": {"client": client, "session": active_session}}

            current_time = datetime.utcnow()
            expiration_time = current_time - timedelta(seconds=20)
            self.db.query(ClientSession).filter(ClientSession.client_id == session_in.client_id).update({
                ClientSession.is_active: False,
                ClientSession.expires_at: expiration_time
            })
            self.db.commit()

            new_session = ClientSession(
                client_id=session_in.client_id,
                is_active=False,
                expires_at=current_time
            )
            self.db.add(new_session)
            self.db.commit()
            self.db.refresh(new_session)

            otp_response = OTPService(self.db).create_otp_for_session(new_session.id)
            if otp_response.get("code") != 200:
                self.db.delete(new_session)
                self.db.commit()
                return {"code": 500, "message": "Échec de la création de l'OTP, session annulée.", "data": None}

            user_identifier = client.email if client.email else client.phone
            token = self.generate_token(user_identifier, new_session.expires_at)
            return {"code": 200, "message": "Nouvelle session créée.", "data": {"client": client, "session": new_session, "token": token}}
        except Exception as e:
            self.db.rollback()
            return {"code": 500, "message": f"Erreur lors de la création de la session: {str(e)}.", "data": None}

    def get_session_by_id(self, session_id: int) -> Dict[str, Any]:
        try:
            session_instance = self.db.query(ClientSession).filter(ClientSession.id == session_id).first()
            if session_instance:
                return {"code": 200, "message": "Session récupérée avec succès.", "data": session_instance}
            else:
                return {"code": 404, "message": "Session non trouvée.", "data": None}
        except Exception as e:
            return {"code": 500, "message": f"Erreur lors de la récupération de la session: {str(e)}.", "data": None}

    def get_sessions_by_client(self, client_id: int) -> Dict[str, Any]:
        try:
            current_time = datetime.utcnow()
            sessions = self.db.query(ClientSession).filter(ClientSession.client_id == client_id).all()

            if not sessions:
                return {"code": 404, "message": "Aucune session trouvée pour ce client.", "data": None}

            sessions_grouped = {"actives": [], "expirées": [], "inactives": []}
            for session in sessions:
                if session.is_active and session.expires_at > current_time:
                    sessions_grouped["actives"].append(session)
                elif session.expires_at <= current_time:
                    sessions_grouped["expirées"].append(session)
                else:
                    sessions_grouped["inactives"].append(session)

            return {"code": 200, "message": "Sessions récupérées avec succès.", "data": sessions_grouped}
        except Exception as e:
            return {"code": 500, "message": f"Erreur lors de la récupération des sessions: {str(e)}.", "data": None}

    def activate_session(self, session_id: int, otp_code: str) -> Dict[str, Any]:
        try:
            session = self.db.query(ClientSession).filter(ClientSession.id == session_id).first()
            if not session:
                return {"code": 404, "message": "Session introuvable.", "data": None}

            otp_service = OTPService(self.db)
            otp_validation = otp_service.validate_otp(session_id, otp_code)
            if otp_validation.get("code") != 200:
                return {"code": 400, "message": "OTP invalide ou expiré.", "data": None}

            current_time = datetime.utcnow()
            if session.is_active and session.expires_at > current_time:
                return {"code": 200, "message": "Cette session est déjà active.", "data": session}

            self.db.query(ClientSession).filter(
                ClientSession.client_id == session.client_id,
                ClientSession.is_active == True
            ).update({ClientSession.is_active: False})
            
            session.is_active = True
            session.expires_at = current_time + timedelta(hours=2)
            self.db.commit()
            self.db.refresh(session)
            
            token = None
            if session.client:
                user_identifier = session.client.email if session.client.email else session.client.phone
                token = self.generate_token(user_identifier, session.expires_at)
            return {"code": 200, "message": "Session activée avec succès.", "data": {"session": session, "token": token}}
        except Exception as e:
            self.db.rollback()
            return {"code": 500, "message": f"Erreur lors de l'activation de la session: {str(e)}.", "data": None}
