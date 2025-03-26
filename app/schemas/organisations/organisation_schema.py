from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.configs.enumerations.Organisations import OrganisationEnum

class OrganisationBase(BaseModel):
    nom: OrganisationEnum = Field(..., description="Nom de l'organisation")
    reference: str = Field(..., description="Référence unique de l'organisation")

class OrganisationCreate(OrganisationBase):
    """
    Schéma utilisé lors de la création d'une organisation.
    Les champs générés automatiquement (id, created_at, updated_at) sont gérés par la base de données.
    """
    pass

class OrganisationRead(OrganisationBase):
    id: int = Field(..., description="Identifiant unique de l'organisation")
    cle_publique: datetime = Field(..., description="Clé d'api publique de l'organisation")
    created_at: datetime = Field(..., description="Date de création de l'organisation")
    updated_at: datetime = Field(..., description="Date de dernière mise à jour de l'organisation")

    class Config:
        from_attributes = True
