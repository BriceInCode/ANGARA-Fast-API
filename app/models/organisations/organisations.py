import uuid
from sqlalchemy import Column, Integer, String, DateTime, func, Enum as SQLAlchemyEnum
from app.configs.enumerations.Organisations import OrganisationEnum
from sqlalchemy.orm import relationship
from app.configs.database import Base

class Organisation(Base):
    __tablename__ = "organisations"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(SQLAlchemyEnum(OrganisationEnum), nullable=False)
    reference = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    utilisateurs = relationship("Utilisateur", back_populates="organisation", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Organisation {self.reference}>"
