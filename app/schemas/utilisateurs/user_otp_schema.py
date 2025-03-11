from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class UserOTPBase(BaseModel):
    utilisateur_id: int = Field(..., description="Identifiant de l'utilisateur associé à l'OTP")

class UserOTPCreate(UserOTPBase):
    """
    Schéma utilisé lors de la création d'un OTP pour un utilisateur.
    Le code OTP ainsi que les dates de création et d'expiration sont générés par le modèle.
    """
    pass

class UserOTPRead(UserOTPBase):
    id: int = Field(..., description="Identifiant unique de l'OTP")
    otp_code: str = Field(..., description="Code OTP généré")
    created_at: datetime = Field(..., description="Date de création de l'OTP")
    expires_at: datetime = Field(..., description="Date d'expiration de l'OTP")

    class Config:
        from_attributes = True
