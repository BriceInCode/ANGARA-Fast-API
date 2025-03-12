from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class DocumentBase(BaseModel):
    demande_id: int = Field(..., description="Identifiant de la demande associée au document")
    file_path: str = Field(..., description="Chemin du fichier")
    file_type: str = Field(..., description="Type du fichier")
    file_size: int = Field(..., description="Taille du fichier en octets")
    checksum: str = Field(..., description="Checksum du fichier pour vérifier l'intégrité")

class DocumentCreate(DocumentBase):
    """
    Schéma pour la création d'un document.
    Les champs auto-générés (id, created_at, updated_at) sont gérés par SQLAlchemy.
    """
    pass

class DocumentRead(DocumentBase):
    id: int = Field(..., description="Identifiant unique du document")
    created_at: datetime = Field(..., description="Date de création du document")
    updated_at: datetime = Field(..., description="Date de dernière mise à jour du document")

    class Config:
        from_attributes = True
