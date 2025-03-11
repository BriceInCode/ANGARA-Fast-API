from pydantic import BaseModel, EmailStr, Field, root_validator
from datetime import datetime
from typing import Optional

class ClientBase(BaseModel):
    email: Optional[EmailStr] = Field(None, description="Adresse email du client")
    phone: Optional[str] = Field(None, description="Numéro de téléphone du client")

    @root_validator(skip_on_failure=True)
    def check_email_or_phone(cls, values):
        if not values.get('email') and not values.get('phone'):
            raise ValueError('Au moins un des champs email ou téléphone doit être fourni')
        return values

class ClientCreate(ClientBase):
    pass

class ClientRead(ClientBase):
    id: int = Field(..., description="Identifiant unique du client")
    created_at: datetime = Field(..., description="Date de création du client")

    class Config:
        from_attributes = True
