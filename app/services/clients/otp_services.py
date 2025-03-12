import random
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.configs.utils.email_service import EmailService
from app.models.clients.session import Session as SessionModel
from app.models.clients.otp import OTP

class OTPService:
    def __init__(self, db: Session):
        self.db = db
        self.email_service = EmailService()
        
    def get_user_email_by_session(self, session_id: int) -> Optional[str]:
        session_obj = self.db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if session_obj and session_obj.client:
            return session_obj.client.email
        return None

    def create_otp_for_session(self, session_id: int) -> Dict[str, Any]:
        try:
            receiver_email = self.get_user_email_by_session(session_id)
            print(f"Email: {receiver_email}")

            otps = self.db.query(OTP).filter(OTP.session_id == session_id).all()
            current_time = datetime.utcnow()
            expiration_time = current_time - timedelta(seconds=20)
            for otp in otps:
                otp.expires_at = expiration_time
            self.db.commit()

            otp_code = str(random.randint(10000, 99999))
            new_otp = OTP(session_id=session_id, otp_code=otp_code, expires_at=current_time + timedelta(minutes=70))
            self.db.add(new_otp)
            self.db.commit()
            self.db.refresh(new_otp)
            
            if receiver_email:
                subject = "Votre code OTP"
                body = (
                    f"Bonjour,\n\n"
                    f"Votre code OTP est : {new_otp.otp_code}\n\n"
                    "Il expirera bientôt."
                )
                success = self.email_service.send_email(receiver_email, subject, body)
                message = "OTP généré et email envoyé avec succès" if success else "OTP généré mais échec de l'envoi de l'email"
            else:
                message = "OTP généré, aucun email trouvé pour l'envoi"
            
            return {"code": 200, "message": message, "data": new_otp}
        except Exception as e:
            self.db.rollback()
            return {"code": 500, "message": f"Erreur lors de la création de l'OTP: {str(e)}.", "data": None}

    def get_otp_by_session_id(self, session_id: int) -> Dict[str, Any]:
        try:
            otp = self.db.query(OTP).filter(OTP.session_id == session_id).first()
            if otp:
                return {"code": 200, "message": "OTP récupéré avec succès.", "data": otp}
            else:
                return {"code": 404, "message": "OTP non trouvé.", "data": None}
        except Exception as e:
            return {"code": 500, "message": f"Erreur lors de la récupération de l'OTP: {str(e)}.", "data": None}

    def validate_otp(self, session_id: int, otp_code: str) -> Dict[str, Any]:
        try:
            result = self.get_otp_by_session_id(session_id)
            otp = result.get("data")
            if not otp:
                return {"code": 404, "message": "OTP non trouvé.", "data": None}
            if otp.otp_code == otp_code and otp.expires_at > datetime.utcnow():
                return {"code": 200, "message": "OTP valide.", "data": otp}
            else:
                return {"code": 400, "message": "OTP invalide ou expiré.", "data": None}
        except Exception as e:
            return {"code": 500, "message": f"Erreur lors de la validation de l'OTP: {str(e)}.", "data": None}
