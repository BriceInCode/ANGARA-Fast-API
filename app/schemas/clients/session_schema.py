from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class SessionBase(BaseModel):
    client_id: int = Field(..., description="Identifiant du client associé à la session")
    is_active: bool = Field(False, description="Statut actif de la session")

class SessionCreate(SessionBase):
    pass

class SessionRead(SessionBase):
    id: int = Field(..., description="Identifiant unique de la session")
    created_at: datetime = Field(..., description="Date de création de la session")
    expires_at: datetime = Field(..., description="Date d'expiration de la session")

    class Config:
        from_attributes = True
