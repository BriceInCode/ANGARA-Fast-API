from pydantic import BaseModel, Field, root_validator
from datetime import datetime
from typing import Optional

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}

class DocumentBase(BaseModel):
    request_id: int = Field(..., gt=0, description="ID de la demande associée")
    file_path: str = Field(..., max_length=255, description="Chemin du fichier")
    file_type: str = Field(..., max_length=100, description="Type du fichier (ex: pdf, png, jpg, jpeg, etc.)")
    file_size: int = Field(..., gt=0, description="Taille du fichier en octets")
    checksum: str = Field(..., max_length=255, description="Checksum SHA-256 du fichier")

    @root_validator(skip_on_failure=True)
    def validate_file_extension(cls, values):
        file_path = values.get("file_path")
        if file_path:
            extension = file_path.split(".")[-1].lower()
            if extension not in ALLOWED_EXTENSIONS:
                raise ValueError(f"L'extension du fichier {extension} n'est pas autorisée.")
        return values

class DocumentCreate(DocumentBase):
    pass

class DocumentRead(DocumentBase):
    id: int = Field(..., description="Identifiant unique du document")
    created_at: datetime = Field(..., description="Date de création du document")
    updated_at: datetime = Field(..., description="Date de mise à jour du document")

    class Config:
        from_attributes = True
