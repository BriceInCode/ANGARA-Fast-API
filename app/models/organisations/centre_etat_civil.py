from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.configs.database import Base

class CentreEtatCivil(Base):
    __tablename__ = "centres_etat_civil"

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String(255), nullable=False, unique=True)
    nom = Column(String(255), nullable=False, unique=True)
    adresse = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True, unique=True)
    telephone = Column(String(20), nullable=True, unique=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relation avec les utilisateurs
    utilisateurs = relationship("Utilisateur", back_populates="centre")

    def __repr__(self):
        return f"<CentreEtatCivil {self.nom} - {self.adresse}>"
