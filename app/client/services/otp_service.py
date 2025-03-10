from sqlalchemy.orm import Session
from app.client.models.otp import OTP
from app.client.models.session import Session as SessionModel
from datetime import datetime, timedelta
import random
from typing import Optional
from app.config.utils.email_service import EmailService

class OTPService:
    def __init__(self, db: Session):
        self.db = db
        self.email_service = EmailService()  # Instanciation du service d'email

    def get_user_email_by_session(self, session_id: int) -> Optional[str]:
        """ Récupère l'email de l'utilisateur à partir de l'ID de la session."""
        session_obj = self.db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if session_obj and session_obj.client:
            return session_obj.client.email
        return None

    def create_otp(self, session_id: int) -> dict:
        """  Crée un OTP pour la session donnée et, s'il existe, envoie l'OTP par email.  """
        # Récupérer l'email de l'utilisateur à partir de la session
        receiver_email = self.get_user_email_by_session(session_id)

        # Générer et sauvegarder l'OTP
        otp_code = str(random.randint(10000, 99999))
        expires_at = datetime.utcnow() + timedelta(minutes=68)
        new_otp = OTP(session_id=session_id, otp_code=otp_code, expires_at=expires_at)
        self.db.add(new_otp)
        self.db.commit()
        self.db.refresh(new_otp)

        # Si une adresse email est disponible, envoyer l'OTP par email
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

        return {
            "code": 200,
            "message": message,
            "data": new_otp
        }
        
    def validate_otp(self, session_id: int, otp_code: str) -> dict:
        """
        Valide l'OTP pour la session donnée.
        Vérifie que le code en base correspond au code fourni et que la date d'expiration est > à la date actuelle.
        """
        otp_obj = self.db.query(OTP).filter(OTP.session_id == session_id).first()
        if otp_obj is None:
            return {
                "code": 404,
                "message": "OTP non trouvé pour cette session",
                "data": None
            }
        if otp_obj.otp_code != otp_code:
            return {
                "code": 400,
                "message": "OTP invalide",
                "data": None
            }
        if otp_obj.expires_at <= datetime.utcnow():
            return {
                "code": 400,
                "message": "OTP expiré",
                "data": None
            }
        return {
            "code": 200,
            "message": "OTP validé",
            "data": otp_obj
        }
