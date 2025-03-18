from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum as SQLAlchemyEnum,
    func
)
from sqlalchemy.orm import relationship
import uuid
from app.configs.database import Base
from app.configs.enumerations.Documents import DocumentEnum
from app.configs.enumerations.Raisons import RaisonEnum
from app.configs.enumerations.Sexe import SexeEnum
from app.configs.enumerations.Status import StatusEnum

# -------------------------------------------------------------------------
# Classe de base pour toutes les demandes (héritage polymorphe)
# -------------------------------------------------------------------------
class DemandeBase(Base):
    __tablename__ = "demandes"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    numero_demande = Column(String(36), unique=True, nullable=False)
    type_document = Column(SQLAlchemyEnum(DocumentEnum), nullable=False)
    raison_demande = Column(SQLAlchemyEnum(RaisonEnum), nullable=False)
    status = Column(SQLAlchemyEnum(StatusEnum), nullable=False, default=StatusEnum.EN_COURS)
    date_creation = Column(DateTime, server_default=func.now(), nullable=False)
    date_modification = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Champs administratifs communs
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
        'polymorphic_on': type_document,
        'polymorphic_identity': 'demande'
    }

# -------------------------------------------------------------------------
# Demande d’acte de naissance
# -------------------------------------------------------------------------
class DemandeActeNaissance(DemandeBase):
    __tablename__ = "demande_acte_naissance"
    
    id = Column(Integer, ForeignKey("demandes.id", ondelete="CASCADE"), primary_key=True)
    
    prenom = Column(String(255), nullable=False)
    nom = Column(String(255), nullable=False)
    sexe = Column(SQLAlchemyEnum(SexeEnum), nullable=False)
    date_naissance = Column(DateTime, nullable=False)
    lieu_naissance = Column(String(255), nullable=False)

    reference_centre_civil = Column(String(255), nullable=False)
    numero_acte_naissance = Column(String(255), nullable=False)
    date_creation_acte = Column(DateTime, nullable=False)
    declare_par = Column(String(255), nullable=False)
    autorise_par = Column(String(255), nullable=True)

    nom_pere = Column(String(255), nullable=False)
    date_naissance_pere = Column(DateTime, nullable=False)
    lieu_naissance_pere = Column(String(255), nullable=False)
    profession_pere = Column(String(255), nullable=False)
    nom_mere = Column(String(255), nullable=False)
    date_naissance_mere = Column(DateTime, nullable=False)
    lieu_naissance_mere = Column(String(255), nullable=False)
    profession_mere = Column(String(255), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': DocumentEnum.ACTE_NAISSANCE.value
    }

# -------------------------------------------------------------------------
# Demande d’acte de mariage
# -------------------------------------------------------------------------
class DemandeActeMariage(DemandeBase):
    __tablename__ = "demande_acte_mariage"
    
    id = Column(Integer, ForeignKey("demandes.id", ondelete="CASCADE"), primary_key=True)
    epoux_nom = Column(String(255), nullable=False)
    epoux_prenom = Column(String(255), nullable=True)
    epouse_nom = Column(String(255), nullable=False)
    epouse_prenom = Column(String(255), nullable=True)

    date_mariage = Column(DateTime, nullable=False)
    lieu_mariage = Column(String(255), nullable=False)
    nom_officiant = Column(String(255), nullable=False)
    temoin1 = Column(String(255), nullable=True)
    temoin2 = Column(String(255), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': DocumentEnum.ACTE_MARIAGE.value
    }

# -------------------------------------------------------------------------
# Demande d’acte de décès
# -------------------------------------------------------------------------
class DemandeActeDeces(DemandeBase):
    __tablename__ = "demande_acte_deces"
    
    id = Column(Integer, ForeignKey("demandes.id", ondelete="CASCADE"), primary_key=True)

    nom = Column(String(255), nullable=False)
    prenom = Column(String(255), nullable=True)
    sexe = Column(SQLAlchemyEnum(SexeEnum), nullable=False)
    date_naissance = Column(DateTime, nullable=False)
    lieu_naissance = Column(String(255), nullable=False)

    numero_acte_deces = Column(String(255), nullable=False)
    date_deces = Column(DateTime, nullable=False)
    lieu_deces = Column(String(255), nullable=False)
    cause_deces = Column(String(255), nullable=True)
    declare_par_deces = Column(String(255), nullable=False)
    date_creation_acte_deces = Column(DateTime, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': DocumentEnum.ACTE_DECES.value
    }

# -------------------------------------------------------------------------
# Demande de certificat de nationalité
# -------------------------------------------------------------------------
class DemandeCertificatNationalite(DemandeBase):
    __tablename__ = "demande_certificat_nationalite"
    
    id = Column(Integer, ForeignKey("demandes.id", ondelete="CASCADE"), primary_key=True)
    nationalite = Column(String(255), nullable=False, default="CAMEROUNAISE")
    numero_certificat_nationalite = Column(String(255), nullable=False)
    date_certification = Column(DateTime, nullable=False)
    lieu_certification = Column(String(255), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': DocumentEnum.CERTIFICAT_NATIONALITE.value
    }

# -------------------------------------------------------------------------
# Demande d’extrait du casier judiciaire
# -------------------------------------------------------------------------
class DemandeCasierJudiciaire(DemandeBase):
    __tablename__ = "demande_casier_judiciaire"
    
    id = Column(Integer, ForeignKey("demandes.id", ondelete="CASCADE"), primary_key=True)
    numero_extrait_casier = Column(String(255), nullable=False)
    date_extrait = Column(DateTime, nullable=False)
    resultat = Column(String(255), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': DocumentEnum.CASIER_JUDICIAIRE.value
    }

# -------------------------------------------------------------------------
# Demande d’extrait du plumitif
# -------------------------------------------------------------------------
class DemandePlumitif(DemandeBase):
    __tablename__ = "demande_plumitif"
    
    id = Column(Integer, ForeignKey("demandes.id", ondelete="CASCADE"), primary_key=True)
    etat_civil = Column(String(255), nullable=False)
    numero_plumitif = Column(String(255), nullable=False)
    date_maj = Column(DateTime, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': DocumentEnum.PLUMITIF.value
    }
