from pydantic import BaseModel, Field, root_validator
from datetime import datetime, date
from typing import Optional
from app.documents.models.types.gender import GenderType
from app.documents.models.types.documents import DocumentsType
from app.documents.models.types.raisons import RaisonsType
from app.documents.models.types.status import StatusType
from app.documents.schemas.document import DocumentRead  # Importer le schéma du document

class DemandeBase(BaseModel):
    session_id: int = Field(..., gt=0, description="ID de la session associée")
    request_number: Optional[str] = Field(None, min_length=15, max_length=22, description="Numéro unique de la demande (15 à 22 caractères)")
    document_type: DocumentsType = Field(..., description="Type de document demandé")
    request_reason: RaisonsType = Field(..., description="Raison de la demande")
    civil_center_reference: str = Field(..., max_length=255, description="Référence du centre civil")
    birth_act_number: str = Field(..., max_length=255, description="Numéro de l'acte de naissance")
    birth_act_creation_date: date = Field(..., description="Date de création de l'acte de naissance")
    declaration_by: str = Field(..., max_length=255, description="Nom du déclarant")
    authorized_by: Optional[str] = Field(None, max_length=255, description="Nom de l'autorisé (optionnel)")

    first_name: Optional[str] = Field(None, min_length=2, max_length=255, description="Nom")
    last_name: str = Field(..., min_length=2, max_length=255, description="Prénom") 
    gender: GenderType = Field(..., description="Sexe de la personne")
    birth_date: date = Field(..., description="Date de naissance")
    birth_place: str = Field(..., min_length=2, max_length=255, description="Lieu de naissance")

    father_name: str = Field(..., min_length=2, max_length=255, description="Nom du père")
    father_birth_date: Optional[date] = Field(None, description="Date de naissance du père")
    father_birth_place: Optional[str] = Field(None, min_length=2, max_length=255, description="Lieu de naissance du père")
    father_profession: Optional[str] = Field(None, min_length=2, max_length=255, description="Profession du père")

    mother_name: str = Field(..., min_length=2, max_length=255, description="Nom de la mère")
    mother_birth_date: Optional[date] = Field(None, description="Date de naissance de la mère")
    mother_birth_place: Optional[str] = Field(None, min_length=2, max_length=255, description="Lieu de naissance de la mère")
    mother_profession: Optional[str] = Field(None, min_length=2, max_length=255, description="Profession de la mère")

    status: StatusType = Field(default=StatusType.EN_COURS, description="Statut de la demande (par défaut: en_cours)")

    @root_validator(skip_on_failure=True)
    def validate_birth_act(cls, values):
        birth_act_number = values.get("birth_act_number")
        birth_act_creation_date = values.get("birth_act_creation_date")
        if bool(birth_act_number) != bool(birth_act_creation_date):
            raise ValueError("Le numéro et la date de création de l'acte de naissance doivent être renseignés ensemble.")
        return values

class DemandeCreate(DemandeBase):
    pass

class DemandeRead(DemandeBase):
    id: int = Field(..., description="Identifiant unique de la demande")
    created_at: datetime = Field(..., description="Date de création de la demande")
    updated_at: datetime = Field(..., description="Date de mise à jour de la demande")
    document: Optional[DocumentRead]  # Correction ici : utiliser DocumentRead et non DemandeBase

    class Config:
        from_attributes = True

DemandeRead.update_forward_refs()
