from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.utilisateurs.otp import USER_OTP
from app.schemas.utilisateurs.user_otp_schema import UserOTPCreate, UserOTPRead
from datetime import datetime

class OTPService:
    @staticmethod
    def create_otp(db: Session, otp_data: UserOTPCreate):
        try:
            new_otp = USER_OTP(**otp_data.dict())
            db.add(new_otp)
            db.commit()
            db.refresh(new_otp)
            return {"code": 201, "message": "OTP créé avec succès", "data": UserOTPRead.from_orm(new_otp)}
        except IntegrityError as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur d'intégrité lors de la création de l'OTP: {str(e)}", "data": None}
        except Exception as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur inattendue lors de la création de l'OTP: {str(e)}", "data": None}

    @staticmethod
    def get_otp_by_id(db: Session, otp_id: int):
        otp = db.query(USER_OTP).filter(USER_OTP.id == otp_id).first()
        if otp:
            return {"code": 200, "message": "OTP trouvé", "data": UserOTPRead.from_orm(otp)}
        return {"code": 404, "message": "OTP non trouvé", "data": None}

    @staticmethod
    def delete_otp(db: Session, otp_id: int):
        otp = db.query(USER_OTP).filter(USER_OTP.id == otp_id).first()
        if not otp:
            return {"code": 404, "message": "OTP non trouvé", "data": None}
        try:
            db.delete(otp)
            db.commit()
            return {"code": 200, "message": "OTP supprimé avec succès", "data": None}
        except IntegrityError as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur lors de la suppression de l'OTP: {str(e)}", "data": None}
        except Exception as e:
            db.rollback()
            return {"code": 500, "message": f"Erreur inattendue: {str(e)}", "data": None}
