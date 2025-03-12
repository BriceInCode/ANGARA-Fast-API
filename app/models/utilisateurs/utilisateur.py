from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from app.configs.database import Base
from app.configs.enumerations.Comptes import ComptesEnum

class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False)
    prenom = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    mot_de_passe = Column(String(255), nullable=False)
    status = Column(SQLAlchemyEnum(ComptesEnum), nullable=False, default=ComptesEnum.ACTIF)

    date_creation = Column(DateTime, server_default=func.now(), nullable=False)
    date_modification = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    organisation_id = Column(Integer, ForeignKey("organisations.id", ondelete="CASCADE"), nullable=False)

    role = relationship("Role", back_populates="utilisateurs")
    organisation = relationship("Organisation", back_populates="utilisateurs")
    permissions = relationship("Permission", secondary="user_permissions", back_populates="utilisateurs")

    centre_id = Column(Integer, ForeignKey("centres_etat_civil.id", ondelete="SET NULL"), nullable=True)
    centre = relationship("CentreEtatCivil", back_populates="utilisateurs")

    affecte_par_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="SET NULL"), nullable=True)
    date_affectation = Column(DateTime, nullable=True)

    # Explicitly specify foreign key in the relationship
    affecteur = relationship("Utilisateur", remote_side=[id], backref="utilisateurs_affectes", foreign_keys=[affecte_par_id])

    # Additional relationships
    organisation_affecte_par_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="SET NULL"), nullable=True)
    date_affectation_organisation = Column(DateTime, nullable=True)

    centre_affecte_par_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="SET NULL"), nullable=True)
    date_affectation_centre = Column(DateTime, nullable=True)

    def affecter_centre(self, centre_id, utilisateur_id):
        """Attribue un centre à un utilisateur et enregistre l'affectation"""
        self.centre_id = centre_id
        self.affecte_par_id = utilisateur_id
        self.date_affectation = func.now()
        self.centre_affecte_par_id = utilisateur_id
        self.date_affectation_centre = func.now()

    def affecter_organisation(self, organisation_id, utilisateur_id):
        """Attribue une organisation à un utilisateur et enregistre l'affectation"""
        self.organisation_id = organisation_id
        self.affecte_par_id = utilisateur_id
        self.date_affectation = func.now()
        self.organisation_affecte_par_id = utilisateur_id
        self.date_affectation_organisation = func.now()

    def __repr__(self):
        return f"<Utilisateur {self.email} - Centre {self.centre_id} - Organisation {self.organisation_id} - Status {self.status}>"
