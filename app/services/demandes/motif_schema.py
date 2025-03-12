from pydantic import BaseModel, Field
from datetime import datetime
from app.configs.enumerations.Motifs import MotifEnum

class MotifBase(BaseModel):
    motif: MotifEnum = Field(..., description="Motif de la demande")
    description: str = Field(..., description="Description détaillée du motif")

class MotifCreate(MotifBase):
    """ Schéma pour la création d'un motif. """
    pass

class MotifRead(MotifBase):
    id: int = Field(..., description="Identifiant unique du motif")
    created_at: datetime = Field(..., description="Date de création du motif")

    class Config:
        from_attributes = True
