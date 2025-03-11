from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

class CentreEtatCivilBase(BaseModel):
    reference: str = Field(..., description="Référence unique du centre d'état civil")
    nom: str = Field(..., description="Nom du centre d'état civil")
    adresse: Optional[str] = Field(None, description="Adresse du centre d'état civil")
    email: Optional[EmailStr] = Field(None, description="Email du centre d'état civil")
    telephone: Optional[str] = Field(None, description="Numéro de téléphone du centre d'état civil")

class CentreEtatCivilCreate(CentreEtatCivilBase):
    """
    Schéma utilisé lors de la création d'un centre d'état civil.
    Les champs générés automatiquement (id, created_at, updated_at) sont gérés par la base de données.
    """
    pass

class CentreEtatCivilRead(CentreEtatCivilBase):
    id: int = Field(..., description="Identifiant unique du centre d'état civil")
    created_at: datetime = Field(..., description="Date de création du centre d'état civil")
    updated_at: datetime = Field(..., description="Date de dernière mise à jour du centre d'état civil")

    class Config:
        from_attributes = True
