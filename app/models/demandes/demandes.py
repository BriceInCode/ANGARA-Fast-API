from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLAlchemyEnum, func
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.configs.database import Base
from app.configs.enumerations.Documents import DocumentEnum
from app.configs.enumerations.Raisons import RaisonEnum
from app.configs.enumerations.Sexe import SexeEnum
from app.configs.enumerations.Status import StatusEnum

from app.models.demandes.motif import Motif

# Mixins pour les champs communs
class TimestampMixin:
    date_creation = Column(DateTime, server_default=func.now(), nullable=False)
    date_modification = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

class PersonMixin:
    prenom = Column(String(255), nullable=True)
    nom = Column(String(255), nullable=False)
    sexe = Column(SQLAlchemyEnum(SexeEnum), nullable=False)
    date_naissance = Column(DateTime, nullable=False)
    lieu_naissance = Column(String(255), nullable=False)

# Classe de base pour toutes les demandes
class Demande(Base, TimestampMixin):
    __tablename__ = "demandes"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    numero_demande = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    type_document = Column(SQLAlchemyEnum(DocumentEnum), nullable=False)
    raison_demande = Column(SQLAlchemyEnum(RaisonEnum), nullable=False)
    reference_centre_civil = Column(String(255), nullable=False)
    
    # Champs administratifs communs
    status = Column(SQLAlchemyEnum(StatusEnum), nullable=False, default=StatusEnum.EN_COURS)
    motif_id = Column(Integer, ForeignKey("motifs_demandes.id", ondelete="SET NULL"), nullable=True)
    
    valide_par_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="SET NULL"), nullable=True)
    date_validation = Column(DateTime, nullable=True)
    rejete_par_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="SET NULL"), nullable=True)
    date_rejet = Column(DateTime, nullable=True)
    agent_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="SET NULL"), nullable=True)
    date_affectation_agent = Column(DateTime, nullable=True)
    agent_site_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="SET NULL"), nullable=True)
    date_affectation_agent_site = Column(DateTime, nullable=True)
    
    # Relations
    client = relationship("Client", back_populates="demandes")
    motif = relationship("Motif")
    valide_par = relationship("Utilisateur", foreign_keys=[valide_par_id])
    rejete_par = relationship("Utilisateur", foreign_keys=[rejete_par_id])
    agent = relationship("Utilisateur", foreign_keys=[agent_id])
    agent_site = relationship("Utilisateur", foreign_keys=[agent_site_id])
    
    __mapper_args__ = {
        "polymorphic_on": type_document,
        "polymorphic_identity": "demande"
    }
    
    def __repr__(self):
        return f"<Demande {self.numero_demande} - Type: {self.type_document.value} - Status: {self.status.value}>"

# 1. Acte de Naissance (hérite de PersonMixin pour éviter la redondance)
class ActeNaissance(Demande, PersonMixin):
    __tablename__ = "acte_naissance"
    id = Column(Integer, ForeignKey("demandes.id", ondelete="CASCADE"), primary_key=True)
    
    numero_acte_naissance = Column(String(255), nullable=False)
    date_creation_acte = Column(DateTime, nullable=False)
    declare_par = Column(String(255), nullable=False)
    autorise_par = Column(String(255), nullable=True)
    nom_pere = Column(String(255), nullable=False)
    date_naissance_pere = Column(DateTime, nullable=True)
    lieu_naissance_pere = Column(String(255), nullable=True)
    profession_pere = Column(String(255), nullable=True)
    nom_mere = Column(String(255), nullable=False)
    date_naissance_mere = Column(DateTime, nullable=True)
    lieu_naissance_mere = Column(String(255), nullable=True)
    profession_mere = Column(String(255), nullable=True)
    
    __mapper_args__ = {
         "polymorphic_identity": DocumentEnum.ACTE_NAISSANCE.value,
    }

# 2. Acte de Mariage (les champs étant spécifiques, pas de mixin ici)
class ActeMariage(Demande):
    __tablename__ = "acte_mariage"
    id = Column(Integer, ForeignKey("demandes.id", ondelete="CASCADE"), primary_key=True)
    
    prenom_epoux = Column(String(255), nullable=False)
    nom_epoux = Column(String(255), nullable=False)
    sexe_epoux = Column(SQLAlchemyEnum(SexeEnum), nullable=False)
    date_naissance_epoux = Column(DateTime, nullable=False)
    lieu_naissance_epoux = Column(String(255), nullable=False)
    profession_epoux = Column(String(255), nullable=True)
    
    prenom_epouse = Column(String(255), nullable=False)
    nom_epouse = Column(String(255), nullable=False)
    sexe_epouse = Column(SQLAlchemyEnum(SexeEnum), nullable=False)
    date_naissance_epouse = Column(DateTime, nullable=False)
    lieu_naissance_epouse = Column(String(255), nullable=False)
    profession_epouse = Column(String(255), nullable=True)
    
    date_mariage = Column(DateTime, nullable=False)
    lieu_mariage = Column(String(255), nullable=False)
    nom_officiant = Column(String(255), nullable=False)
    temoin1 = Column(String(255), nullable=True)
    temoin2 = Column(String(255), nullable=True)
    
    __mapper_args__ = {
         "polymorphic_identity": DocumentEnum.ACTE_MARIAGE.value,
    }

# 3. Acte de Décès (les champs sont préfixés, donc pas de mixin)
class ActeDeces(Demande):
    __tablename__ = "acte_deces"
    id = Column(Integer, ForeignKey("demandes.id", ondelete="CASCADE"), primary_key=True)
    
    prenom_decede = Column(String(255), nullable=False)
    nom_decede = Column(String(255), nullable=False)
    sexe_decede = Column(SQLAlchemyEnum(SexeEnum), nullable=False)
    date_naissance_decede = Column(DateTime, nullable=False)
    lieu_naissance_decede = Column(String(255), nullable=False)
    
    numero_acte_deces = Column(String(255), nullable=False)
    date_deces = Column(DateTime, nullable=False)
    lieu_deces = Column(String(255), nullable=False)
    cause_deces = Column(String(255), nullable=True)
    declare_par_deces = Column(String(255), nullable=False)
    date_creation_acte_deces = Column(DateTime, nullable=False)
    
    __mapper_args__ = {
         "polymorphic_identity": DocumentEnum.ACTE_DECES.value,
    }

# 4. Certificat de Nationalité (hérite également de PersonMixin)
class CertificatNationalite(Demande, PersonMixin):
    __tablename__ = "certificat_nationalite"
    id = Column(Integer, ForeignKey("demandes.id", ondelete="CASCADE"), primary_key=True)
    
    nationalite = Column(String(255), nullable=False, default="CAMEROUNAISE")
    numero_certificat_nationalite = Column(String(255), nullable=False)
    date_certification = Column(DateTime, nullable=False)
    lieu_certification = Column(String(255), nullable=False)
    nom_pere = Column(String(255), nullable=False)
    nom_mere = Column(String(255), nullable=False)
    
    __mapper_args__ = {
         "polymorphic_identity": DocumentEnum.CERTIFICAT_NATIONALITE.value,
    }

# 5. Extrait du Casier Judiciaire (hérite de PersonMixin)
class ExtraitCasierJudiciaire(Demande, PersonMixin):
    __tablename__ = "casier_judiciaire"
    id = Column(Integer, ForeignKey("demandes.id", ondelete="CASCADE"), primary_key=True)
    
    nationalite = Column(String(255), nullable=True)
    numero_extrait_casier = Column(String(255), nullable=False)
    date_extrait = Column(DateTime, nullable=False)
    resultat = Column(String(255), nullable=True)
    
    __mapper_args__ = {
         "polymorphic_identity": DocumentEnum.CASIER_JUDICIAIRE.value,
    }

# 6. Extrait du Plumitif (hérite de PersonMixin)
class ExtraitPlumitif(Demande, PersonMixin):
    __tablename__ = "plumitif"
    id = Column(Integer, ForeignKey("demandes.id", ondelete="CASCADE"), primary_key=True)
    
    nationalite = Column(String(255), nullable=True)
    etat_civil = Column(String(255), nullable=False)
    numero_acte_naissance = Column(String(255), nullable=True)
    numero_acte_mariage = Column(String(255), nullable=True)
    numero_acte_deces = Column(String(255), nullable=True)
    numero_plumitif = Column(String(255), nullable=False)
    date_maj = Column(DateTime, nullable=False)
    
    __mapper_args__ = {
         "polymorphic_identity": DocumentEnum.PLUMITIF.value,
    }
