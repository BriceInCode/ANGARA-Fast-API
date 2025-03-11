from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional, List
from app.configs.enumerations.Comptes import ComptesEnum
from role_schema import RoleRead
from organisation_schema import OrganisationRead
from centre_etat_civil_schema import CentreEtatCivilRead
from permission_schema import PermissionRead

class UtilisateurBase(BaseModel):
    nom: str = Field(..., description="Nom de l'utilisateur")
    prenom: str = Field(..., description="Prénom de l'utilisateur")
    email: EmailStr = Field(..., description="Adresse email de l'utilisateur")
    mot_de_passe: str = Field(..., description="Mot de passe de l'utilisateur")
    status: ComptesEnum = Field(default=ComptesEnum.INACTIF, description="Statut du compte utilisateur")

class UtilisateurCreate(UtilisateurBase):
    role_id: int = Field(..., description="Identifiant du rôle associé à l'utilisateur")
    organisation_id: int = Field(..., description="Identifiant de l'organisation associée")
    centre_id: Optional[int] = Field(None, description="Identifiant du centre d'état civil associé à l'utilisateur")

class UtilisateurRead(BaseModel):
    id: int = Field(..., description="Identifiant unique de l'utilisateur")
    nom: str = Field(..., description="Nom de l'utilisateur")
    prenom: str = Field(..., description="Prénom de l'utilisateur")
    email: EmailStr = Field(..., description="Adresse email de l'utilisateur")
    status: ComptesEnum = Field(..., description="Statut du compte utilisateur")
    date_creation: datetime = Field(..., description="Date de création du compte")
    date_modification: datetime = Field(..., description="Date de dernière mise à jour du compte")
    role: RoleRead = Field(..., description="Rôle associé à l'utilisateur")
    organisation: OrganisationRead = Field(..., description="Organisation associée à l'utilisateur")
    centre: Optional[CentreEtatCivilRead] = Field(None, description="Centre d'état civil associé à l'utilisateur")
    permissions: Optional[List[PermissionRead]] = Field(
        None, description="Liste des permissions attribuées à l'utilisateur"
    )

    class Config:
        from_attributes = True
