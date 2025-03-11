from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLAlchemyEnum, func
from sqlalchemy.orm import relationship
from datetime import datetime

from app.configs.database import Base
from app.configs.enumerations.Comptes import ComptesEnum
from app.models.utilisateurs.role import user_permissions

class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    mot_de_passe = Column(String, nullable=False)
    status = Column(SQLAlchemyEnum(ComptesEnum), nullable=False, default=ComptesEnum.INACTIF)
    date_creation = Column(DateTime, server_default=func.now(), nullable=False)
    date_modification = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    organisation_id = Column(Integer, ForeignKey("organisations.id", ondelete="CASCADE"), nullable=False)
    
    role = relationship("Role", back_populates="utilisateurs")
    organisation = relationship("Organisation", back_populates="utilisateurs")
    permissions = relationship("Permission", secondary=user_permissions, back_populates="utilisateurs")

    centre_id = Column(Integer, ForeignKey("centres_etat_civil.id", ondelete="SET NULL"), nullable=True)
    centre = relationship("CentreEtatCivil", back_populates="utilisateurs")

    affecte_par_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="SET NULL"), nullable=True)
    date_affectation = Column(DateTime, nullable=True)

    affecteur = relationship("Utilisateur", remote_side=[id], backref="utilisateurs_affectes")

    def affecter_centre(self, centre_id, utilisateur_id):
        self.centre_id = centre_id
        self.affecte_par_id = utilisateur_id
        self.date_affectation = datetime.utcnow()

    def __repr__(self):
        return f"<Utilisateur {self.email} - Centre {self.centre_id} - Status {self.status.value}>"