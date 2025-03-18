from pydantic import BaseModel, Field
from datetime import datetime
from app.configs.enumerations.Documents import DocumentEnum
from app.configs.enumerations.Raisons import RaisonEnum
from app.configs.enumerations.Sexe import SexeEnum
from app.configs.enumerations.Status import StatusEnum

# -----------------------------------------------------
# Schémas de base communs aux demandes
# -----------------------------------------------------
class DemandeBase(BaseModel):
    client_id: int = Field(..., description="Identifiant du client")
    type_document: DocumentEnum = Field(..., description="Type de document demandé")
    raison_demande: RaisonEnum = Field(..., description="Raison de la demande")

class DemandeCreateBase(DemandeBase):
    """Schéma de base pour la création d'une demande.
    Les champs tels que numero_demande, date_creation et date_modification sont générés automatiquement."""
    pass

class DemandeReadBase(DemandeBase):
    id: int = Field(..., description="Identifiant unique de la demande")
    numero_demande: str = Field(..., description="Numéro unique de la demande")
    status: StatusEnum = Field(..., description="Statut de la demande")
    date_creation: datetime = Field(..., description="Date de création de la demande")
    date_modification: datetime = Field(..., description="Date de modification de la demande")

    class Config:
        orm_mode = True
        from_attributes = True

# -----------------------------------------------------
# Demande d’acte de naissance
# -----------------------------------------------------
class DemandeActeNaissanceCreate(DemandeCreateBase):
    prenom: str = Field(..., description="Prénom de l'enfant")
    nom: str = Field(..., description="Nom de l'enfant")
    sexe: SexeEnum = Field(..., description="Sexe de l'enfant")
    date_naissance: datetime = Field(..., description="Date de naissance de l'enfant")
    lieu_naissance: str = Field(..., description="Lieu de naissance de l'enfant")
    
    reference_centre_civil: str = Field(..., description="Référence du centre civil")
    numero_acte_naissance: str = Field(..., description="Numéro de l'acte de naissance")
    date_creation_acte: datetime = Field(..., description="Date de création de l'acte")
    declare_par: str = Field(..., description="Personne ayant déclaré la naissance")
    autorise_par: str = Field(None, description="Personne ayant autorisé l'acte")
    
    nom_pere: str = Field(..., description="Nom du père")
    date_naissance_pere: datetime = Field(..., description="Date de naissance du père")
    lieu_naissance_pere: str = Field(..., description="Lieu de naissance du père")
    profession_pere: str = Field(..., description="Profession du père")
    nom_mere: str = Field(..., description="Nom de la mère")
    date_naissance_mere: datetime = Field(..., description="Date de naissance de la mère")
    lieu_naissance_mere: str = Field(..., description="Lieu de naissance de la mère")
    profession_mere: str = Field(..., description="Profession de la mère")

class DemandeActeNaissanceRead(DemandeReadBase):
    prenom: str = Field(..., description="Prénom de l'enfant")
    nom: str = Field(..., description="Nom de l'enfant")
    sexe: SexeEnum = Field(..., description="Sexe de l'enfant")
    date_naissance: datetime = Field(..., description="Date de naissance de l'enfant")
    lieu_naissance: str = Field(..., description="Lieu de naissance de l'enfant")
    
    reference_centre_civil: str = Field(..., description="Référence du centre civil")
    numero_acte_naissance: str = Field(..., description="Numéro de l'acte de naissance")
    date_creation_acte: datetime = Field(..., description="Date de création de l'acte")
    declare_par: str = Field(..., description="Personne ayant déclaré la naissance")
    autorise_par: str = Field(None, description="Personne ayant autorisé l'acte")
    
    nom_pere: str = Field(..., description="Nom du père")
    date_naissance_pere: datetime = Field(..., description="Date de naissance du père")
    lieu_naissance_pere: str = Field(..., description="Lieu de naissance du père")
    profession_pere: str = Field(..., description="Profession du père")
    nom_mere: str = Field(..., description="Nom de la mère")
    date_naissance_mere: datetime = Field(..., description="Date de naissance de la mère")
    lieu_naissance_mere: str = Field(..., description="Lieu de naissance de la mère")
    profession_mere: str = Field(..., description="Profession de la mère")

    class Config:
        from_attributes = True

# -----------------------------------------------------
# Demande d’acte de mariage
# -----------------------------------------------------
class DemandeActeMariageCreate(DemandeCreateBase):
    epoux_nom: str = Field(..., description="Nom de l'époux")
    epoux_prenom: str = Field(None, description="Prénom de l'époux")
    epouse_nom: str = Field(..., description="Nom de l'épouse")
    epouse_prenom: str = Field(None, description="Prénom de l'épouse")
    
    date_mariage: datetime = Field(..., description="Date du mariage")
    lieu_mariage: str = Field(..., description="Lieu du mariage")
    nom_officiant: str = Field(..., description="Nom de l'officiant")
    temoin1: str = Field(None, description="Nom du premier témoin")
    temoin2: str = Field(None, description="Nom du deuxième témoin")

class DemandeActeMariageRead(DemandeReadBase):
    epoux_nom: str = Field(..., description="Nom de l'époux")
    epoux_prenom: str = Field(None, description="Prénom de l'époux")
    epouse_nom: str = Field(..., description="Nom de l'épouse")
    epouse_prenom: str = Field(None, description="Prénom de l'épouse")
    
    date_mariage: datetime = Field(..., description="Date du mariage")
    lieu_mariage: str = Field(..., description="Lieu du mariage")
    nom_officiant: str = Field(..., description="Nom de l'officiant")
    temoin1: str = Field(None, description="Nom du premier témoin")
    temoin2: str = Field(None, description="Nom du deuxième témoin")

    class Config:
        from_attributes = True

# -----------------------------------------------------
# Demande d’acte de décès
# -----------------------------------------------------
class DemandeActeDecesCreate(DemandeCreateBase):
    nom: str = Field(..., description="Nom du défunt")
    prenom: str = Field(None, description="Prénom du défunt")
    sexe: SexeEnum = Field(..., description="Sexe du défunt")
    date_naissance: datetime = Field(..., description="Date de naissance du défunt")
    lieu_naissance: str = Field(..., description="Lieu de naissance du défunt")
    
    numero_acte_deces: str = Field(..., description="Numéro de l'acte de décès")
    date_deces: datetime = Field(..., description="Date du décès")
    lieu_deces: str = Field(..., description="Lieu du décès")
    cause_deces: str = Field(None, description="Cause du décès")
    declare_par_deces: str = Field(..., description="Personne déclarant le décès")
    date_creation_acte_deces: datetime = Field(..., description="Date de création de l'acte de décès")

class DemandeActeDecesRead(DemandeReadBase):
    nom: str = Field(..., description="Nom du défunt")
    prenom: str = Field(None, description="Prénom du défunt")
    sexe: SexeEnum = Field(..., description="Sexe du défunt")
    date_naissance: datetime = Field(..., description="Date de naissance du défunt")
    lieu_naissance: str = Field(..., description="Lieu de naissance du défunt")
    
    numero_acte_deces: str = Field(..., description="Numéro de l'acte de décès")
    date_deces: datetime = Field(..., description="Date du décès")
    lieu_deces: str = Field(..., description="Lieu du décès")
    cause_deces: str = Field(None, description="Cause du décès")
    declare_par_deces: str = Field(..., description="Personne déclarant le décès")
    date_creation_acte_deces: datetime = Field(..., description="Date de création de l'acte de décès")

    class Config:
        from_attributes = True

# -----------------------------------------------------
# Demande de certificat de nationalité
# -----------------------------------------------------
class DemandeCertificatNationaliteCreate(DemandeCreateBase):
    nationalite: str = Field("CAMEROUNAISE", description="Nationalité (par défaut Camerounaise)")
    numero_certificat_nationalite: str = Field(..., description="Numéro du certificat de nationalité")
    date_certification: datetime = Field(..., description="Date de certification")
    lieu_certification: str = Field(..., description="Lieu de certification")

class DemandeCertificatNationaliteRead(DemandeReadBase):
    nationalite: str = Field("CAMEROUNAISE", description="Nationalité (par défaut Camerounaise)")
    numero_certificat_nationalite: str = Field(..., description="Numéro du certificat de nationalité")
    date_certification: datetime = Field(..., description="Date de certification")
    lieu_certification: str = Field(..., description="Lieu de certification")

    class Config:
        from_attributes = True

# -----------------------------------------------------
# Demande d’extrait du casier judiciaire
# -----------------------------------------------------
class DemandeCasierJudiciaireCreate(DemandeCreateBase):
    numero_extrait_casier: str = Field(..., description="Numéro de l'extrait du casier judiciaire")
    date_extrait: datetime = Field(..., description="Date de délivrance de l'extrait")
    resultat: str = Field(None, description="Résultat de l'extrait")

class DemandeCasierJudiciaireRead(DemandeReadBase):
    numero_extrait_casier: str = Field(..., description="Numéro de l'extrait du casier judiciaire")
    date_extrait: datetime = Field(..., description="Date de délivrance de l'extrait")
    resultat: str = Field(None, description="Résultat de l'extrait")

    class Config:
        from_attributes = True

# -----------------------------------------------------
# Demande d’extrait du plumitif
# -----------------------------------------------------
class DemandePlumitifCreate(DemandeCreateBase):
    etat_civil: str = Field(..., description="État civil")
    numero_plumitif: str = Field(..., description="Numéro du plumitif")
    date_maj: datetime = Field(..., description="Date de mise à jour")

class DemandePlumitifRead(DemandeReadBase):
    etat_civil: str = Field(..., description="État civil")
    numero_plumitif: str = Field(..., description="Numéro du plumitif")
    date_maj: datetime = Field(..., description="Date de mise à jour")

    class Config:
        from_attributes = True
