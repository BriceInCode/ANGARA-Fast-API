from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from app.configs.enumerations.Persmissions import PermissionEnum
from app.configs.enumerations.Roles import RoleEnum
from app.schemas.utilisateurs.permission_schema import PermissionRead

class RoleBase(BaseModel):
    nom: RoleEnum = Field(..., description="Nom du rôle")
    permissions: list[PermissionEnum]

class RoleCreate(RoleBase):
    """
    Schéma utilisé lors de la création d'un rôle.
    """
    pass

class RoleRead(RoleBase):
    id: int = Field(..., description="Identifiant unique du rôle")
    created_at: datetime = Field(..., description="Date de création du rôle")
    updated_at: datetime = Field(..., description="Date de dernière mise à jour du rôle")
    permissions: Optional[List[PermissionRead]] = Field(
        None, description="Liste des permissions associées à ce rôle"
    )

    class Config:
        from_attributes = True
