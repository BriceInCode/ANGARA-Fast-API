from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.configs.enumerations.Documents import DocumentEnum
from app.configs.enumerations.Raisons import RaisonEnum
from app.configs.enumerations.Sexe import SexeEnum
from app.configs.enumerations.Status import StatusEnum

class DemandeBase(BaseModel):
    client_id: int = Field(..., description="Identifiant du client ayant fait la demande")
    type_document: DocumentEnum = Field(..., description="Type de document demandé")
    raison_demande: RaisonEnum = Field(..., description="Raison de la demande")
    reference_centre_civil: str = Field(..., description="Référence du centre civil")
    prenom: Optional[str] = Field(None, description="Prénom du demandeur")
    nom: str = Field(..., description="Nom du demandeur")
    sexe: SexeEnum = Field(..., description="Sexe du demandeur")
    date_naissance: datetime = Field(..., description="Date de naissance du demandeur")
    lieu_naissance: str = Field(..., description="Lieu de naissance du demandeur")
    numero_acte_naissance: str = Field(..., description="Numéro de l'acte de naissance")
    date_creation_acte: datetime = Field(..., description="Date de création de l'acte de naissance")
    declare_par: str = Field(..., description="Nom du déclarant")
    autorise_par: Optional[str] = Field(None, description="Nom de l'autorité ayant autorisé la déclaration")
    nom_pere: str = Field(..., description="Nom du père")
    date_naissance_pere: Optional[datetime] = Field(None, description="Date de naissance du père")
    lieu_naissance_pere: Optional[str] = Field(None, description="Lieu de naissance du père")
    profession_pere: Optional[str] = Field(None, description="Profession du père")
    nom_mere: str = Field(..., description="Nom de la mère")
    date_naissance_mere: Optional[datetime] = Field(None, description="Date de naissance de la mère")
    lieu_naissance_mere: Optional[str] = Field(None, description="Lieu de naissance de la mère")
    profession_mere: Optional[str] = Field(None, description="Profession de la mère")
    status: StatusEnum = Field(StatusEnum.EN_COURS, description="Statut de la demande")
    motif_id: Optional[int] = Field(None, description="Identifiant du motif en cas de rejet")

class DemandeCreate(DemandeBase):
    """
    Schéma pour la création d'une demande.
    Les champs auto-générés (numéro_demande, dates, etc.) sont gérés par SQLAlchemy.
    """
    pass

class DemandeRead(DemandeBase):
    id: int = Field(..., description="Identifiant unique de la demande")
    numero_demande: str = Field(..., description="Numéro unique de la demande")
    valide_par_id: Optional[int] = Field(None, description="Identifiant de l'utilisateur ayant validé la demande")
    date_validation: Optional[datetime] = Field(None, description="Date de validation de la demande")
    rejete_par_id: Optional[int] = Field(None, description="Identifiant de l'utilisateur ayant rejeté la demande")
    date_rejet: Optional[datetime] = Field(None, description="Date de rejet de la demande")
    agent_id: Optional[int] = Field(None, description="Identifiant de l'agent assigné à la demande")
    date_affectation_agent: Optional[datetime] = Field(None, description="Date d'affectation de l'agent")
    agent_site_id: Optional[int] = Field(None, description="Identifiant de l'agent du site assigné")
    date_affectation_agent_site: Optional[datetime] = Field(None, description="Date d'affectation de l'agent du site")
    date_creation: datetime = Field(..., description="Date de création de la demande")
    date_modification: datetime = Field(..., description="Date de dernière modification de la demande")

    class Config:
        from_attributes = True
