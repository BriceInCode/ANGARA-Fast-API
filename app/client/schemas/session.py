from pydantic import BaseModel, Field
from datetime import datetime

class SessionBase(BaseModel):
    is_active: bool = Field(False, description="Indique si la session est active")

class SessionCreate(SessionBase):
    client_id: int = Field(..., description="Identifiant unique du client associé à la session")

class SessionRead(SessionBase):
    id: int = Field(..., description="Identifiant unique de la session")
    client_id: int = Field(..., description="Identifiant unique du client associé à la session")
    created_at: datetime = Field(..., description="Date de création de la session")

    class Config:
        orm_mode = True
