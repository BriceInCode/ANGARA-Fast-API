from pydantic import BaseModel, Field
from datetime import datetime
from app.configs.enumerations.Persmissions import PermissionEnum

class PermissionBase(BaseModel):
    nom: PermissionEnum = Field(..., description="Nom de la permission")

    class Config:
        orm_mode = True  # This is necessary for compatibility with SQLAlchemy models

class PermissionCreate(PermissionBase):
    """
    Schéma utilisé lors de la création d'une permission.
    """
    pass

class PermissionRead(PermissionBase):
    id: int = Field(..., description="Identifiant unique de la permission")
    created_at: datetime = Field(..., description="Date de création de la permission")
    updated_at: datetime = Field(..., description="Date de dernière mise à jour de la permission")

    class Config:
        from_attributes = True

