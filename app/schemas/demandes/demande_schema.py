from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.configs.enumerations.Documents import DocumentEnum
from app.configs.enumerations.Raisons import RaisonEnum
from app.configs.enumerations.Sexe import SexeEnum
from app.configs.enumerations.Status import StatusEnum

# Schéma commun aux informations administratives
class DemandeAdminBase(BaseModel):
    client_id: int = Field(..., description="Identifiant du client")
    type_document: DocumentEnum = Field(..., description="Type de document demandé")
    raison_demande: RaisonEnum = Field(..., description="Raison de la demande")
    reference_centre_civil: str = Field(..., description="Référence du centre civil")
    status: StatusEnum = Field(StatusEnum.EN_COURS, description="Statut de la demande")
    motif_id: Optional[int] = Field(None, description="Identifiant du motif en cas de rejet")

# Schéma pour les informations d'administration en lecture
class DemandeAdminRead(BaseModel):
    id: int = Field(..., description="Identifiant unique de la demande")
    numero_demande: str = Field(..., description="Numéro unique de la demande")
    valide_par_id: Optional[int] = Field(None, description="Identifiant de l'utilisateur ayant validé")
    date_validation: Optional[datetime] = Field(None, description="Date de validation")
    rejete_par_id: Optional[int] = Field(None, description="Identifiant de l'utilisateur ayant rejeté")
    date_rejet: Optional[datetime] = Field(None, description="Date de rejet")
    agent_id: Optional[int] = Field(None, description="Identifiant de l'agent assigné")
    date_affectation_agent: Optional[datetime] = Field(None, description="Date d'affectation de l'agent")
    agent_site_id: Optional[int] = Field(None, description="Identifiant de l'agent du site assigné")
    date_affectation_agent_site: Optional[datetime] = Field(None, description="Date d'affectation de l'agent du site")
    date_creation: datetime = Field(..., description="Date de création de la demande")
    date_modification: datetime = Field(..., description="Date de dernière modification de la demande")

    class Config:
        orm_mode = True

# Schéma pour les informations personnelles communes
class PersonSchema(BaseModel):
    prenom: Optional[str] = Field(None, description="Prénom")
    nom: str = Field(..., description="Nom")
    sexe: SexeEnum = Field(..., description="Sexe")
    date_naissance: datetime = Field(..., description="Date de naissance")
    lieu_naissance: str = Field(..., description="Lieu de naissance")

# ================================
# 1. Acte de Naissance
class ActeNaissanceBase(DemandeAdminBase, PersonSchema):
    numero_acte_naissance: str = Field(..., description="Numéro de l'acte de naissance")
    date_creation_acte: datetime = Field(..., description="Date de création de l'acte")
    declare_par: str = Field(..., description="Nom du déclarant")
    autorise_par: Optional[str] = Field(None, description="Autorisation")
    nom_pere: str = Field(..., description="Nom du père")
    date_naissance_pere: Optional[datetime] = Field(None, description="Date de naissance du père")
    lieu_naissance_pere: Optional[str] = Field(None, description="Lieu de naissance du père")
    profession_pere: Optional[str] = Field(None, description="Profession du père")
    nom_mere: str = Field(..., description="Nom de la mère")
    date_naissance_mere: Optional[datetime] = Field(None, description="Date de naissance de la mère")
    lieu_naissance_mere: Optional[str] = Field(None, description="Lieu de naissance de la mère")
    profession_mere: Optional[str] = Field(None, description="Profession de la mère")

class ActeNaissanceCreate(ActeNaissanceBase):
    pass

class ActeNaissanceRead(ActeNaissanceBase, DemandeAdminRead):
    pass

# ================================
# 2. Acte de Mariage
class ActeMariageBase(DemandeAdminBase):
    prenom_epoux: str = Field(..., description="Prénom de l'époux")
    nom_epoux: str = Field(..., description="Nom de l'époux")
    sexe_epoux: SexeEnum = Field(..., description="Sexe de l'époux")
    date_naissance_epoux: datetime = Field(..., description="Date de naissance de l'époux")
    lieu_naissance_epoux: str = Field(..., description="Lieu de naissance de l'époux")
    profession_epoux: Optional[str] = Field(None, description="Profession de l'époux")
    
    prenom_epouse: str = Field(..., description="Prénom de l'épouse")
    nom_epouse: str = Field(..., description="Nom de l'épouse")
    sexe_epouse: SexeEnum = Field(..., description="Sexe de l'épouse")
    date_naissance_epouse: datetime = Field(..., description="Date de naissance de l'épouse")
    lieu_naissance_epouse: str = Field(..., description="Lieu de naissance de l'épouse")
    profession_epouse: Optional[str] = Field(None, description="Profession de l'épouse")
    
    date_mariage: datetime = Field(..., description="Date du mariage")
    lieu_mariage: str = Field(..., description="Lieu du mariage")
    nom_officiant: str = Field(..., description="Nom de l'officiant")
    temoin1: Optional[str] = Field(None, description="Nom du premier témoin")
    temoin2: Optional[str] = Field(None, description="Nom du second témoin")

class ActeMariageCreate(ActeMariageBase):
    pass

class ActeMariageRead(ActeMariageBase, DemandeAdminRead):
    pass

# ================================
# 3. Acte de Décès
class ActeDecesBase(DemandeAdminBase):
    prenom_decede: str = Field(..., description="Prénom du défunt")
    nom_decede: str = Field(..., description="Nom du défunt")
    sexe_decede: SexeEnum = Field(..., description="Sexe du défunt")
    date_naissance_decede: datetime = Field(..., description="Date de naissance du défunt")
    lieu_naissance_decede: str = Field(..., description="Lieu de naissance du défunt")
    numero_acte_deces: str = Field(..., description="Numéro de l'acte de décès")
    date_deces: datetime = Field(..., description="Date du décès")
    lieu_deces: str = Field(..., description="Lieu du décès")
    cause_deces: Optional[str] = Field(None, description="Cause du décès")
    declare_par_deces: str = Field(..., description="Nom du déclarant")
    date_creation_acte_deces: datetime = Field(..., description="Date de création de l'acte")

class ActeDecesCreate(ActeDecesBase):
    pass

class ActeDecesRead(ActeDecesBase, DemandeAdminRead):
    pass

# ================================
# 4. Certificat de Nationalité
class CertificatNationaliteBase(DemandeAdminBase, PersonSchema):
    nationalite: str = Field("CAMEROUNAISE", description="Nationalité")
    numero_certificat_nationalite: str = Field(..., description="Numéro du certificat")
    date_certification: datetime = Field(..., description="Date de certification")
    lieu_certification: str = Field(..., description="Lieu de certification")
    nom_pere: str = Field(..., description="Nom du père")
    nom_mere: str = Field(..., description="Nom de la mère")

class CertificatNationaliteCreate(CertificatNationaliteBase):
    pass

class CertificatNationaliteRead(CertificatNationaliteBase, DemandeAdminRead):
    pass

# ================================
# 5. Extrait du Casier Judiciaire
class ExtraitCasierJudiciaireBase(DemandeAdminBase, PersonSchema):
    nationalite: Optional[str] = Field(None, description="Nationalité")
    numero_extrait_casier: str = Field(..., description="Numéro de l'extrait")
    date_extrait: datetime = Field(..., description="Date de l'extrait")
    resultat: Optional[str] = Field(None, description="Résultat")

class ExtraitCasierJudiciaireCreate(ExtraitCasierJudiciaireBase):
    pass

class ExtraitCasierJudiciaireRead(ExtraitCasierJudiciaireBase, DemandeAdminRead):
    pass

# ================================
# 6. Extrait du Plumitif
class ExtraitPlumitifBase(DemandeAdminBase, PersonSchema):
    nationalite: Optional[str] = Field(None, description="Nationalité")
    etat_civil: str = Field(..., description="État civil")
    numero_acte_naissance: Optional[str] = Field(None, description="Numéro de l'acte de naissance")
    numero_acte_mariage: Optional[str] = Field(None, description="Numéro de l'acte de mariage")
    numero_acte_deces: Optional[str] = Field(None, description="Numéro de l'acte de décès")
    numero_plumitif: str = Field(..., description="Numéro du plumitif")
    date_maj: datetime = Field(..., description="Date de mise à jour")

class ExtraitPlumitifCreate(ExtraitPlumitifBase):
    pass

class ExtraitPlumitifRead(ExtraitPlumitifBase, DemandeAdminRead):
    pass
