from pydantic import BaseModel, Field
from datetime import datetime

class OTPBase(BaseModel):
    otp_code: str = Field(..., description="Code OTP généré")

class OTPCreate(BaseModel):
    session_id: int = Field(..., description="Identifiant de la session associée à l'OTP")

class OTPRead(OTPBase):
    id: int = Field(..., description="Identifiant unique de l'OTP")
    session_id: int = Field(..., description="Identifiant de la session associée à l'OTP")
    created_at: datetime = Field(..., description="Date de création de l'OTP")
    expires_at: datetime = Field(..., description="Date d'expiration de l'OTP")

    class Config:
        from_attributes = True
