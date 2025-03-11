from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLAlchemyEnum, func
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.configs.database import Base
from app.configs.enumerations.Documents import DocumentEnum
from app.configs.enumerations.Raisons import RaisonEnum
from app.configs.enumerations.Sexe import SexeEnum
from app.configs.enumerations.Status import StatusEnum

class Demande(Base):
    __tablename__ = "demandes"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    numero_demande = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    type_document = Column(SQLAlchemyEnum(DocumentEnum), nullable=False)
    raison_demande = Column(SQLAlchemyEnum(RaisonEnum), nullable=False)
    reference_centre_civil = Column(String(255), nullable=False)
    prenom = Column(String(255), nullable=True)
    nom = Column(String(255), nullable=False)
    sexe = Column(SQLAlchemyEnum(SexeEnum), nullable=False)
    date_naissance = Column(DateTime, nullable=False)
    lieu_naissance = Column(String(255), nullable=False)
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
    
    date_creation = Column(DateTime, server_default=func.now(), nullable=False)
    date_modification = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    client = relationship("Client", back_populates="demandes")
    motif = relationship("Motif")
    valide_par = relationship("Utilisateur", foreign_keys=[valide_par_id])
    rejete_par = relationship("Utilisateur", foreign_keys=[rejete_par_id])
    agent = relationship("Utilisateur", foreign_keys=[agent_id])
    agent_site = relationship("Utilisateur", foreign_keys=[agent_site_id])

    def valider(self, utilisateur_id):
        self.status = StatusEnum.VALIDE
        self.valide_par_id = utilisateur_id
        self.date_validation = datetime.utcnow()

    def rejeter(self, utilisateur_id, motif_id):
        self.status = StatusEnum.REJETE
        self.rejete_par_id = utilisateur_id
        self.date_rejet = datetime.utcnow()
        self.motif_id = motif_id

    def prendre_en_charge(self, utilisateur_id):
        self.pris_en_charge_par_id = utilisateur_id
        self.date_prise_en_charge = datetime.utcnow()

    def assigner_agent(self, agent_id):
        self.agent_id = agent_id
        self.date_affectation_agent = datetime.utcnow()

    def reassigner_agent_site(self, agent_site_id):
        self.agent_site_id = agent_site_id
        self.date_affectation_agent_site = datetime.utcnow()

    def __repr__(self):
        return (
            f"<Demande {self.numero_demande} - {self.nom} {self.prenom} - "
            f"Status {self.status.value} - Agent {self.agent_id} - Agent site {self.agent_site_id}>"
        )
