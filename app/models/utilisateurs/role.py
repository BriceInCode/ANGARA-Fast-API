from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy import Enum as SQLAlchemyEnum
from app.configs.enumerations.Roles import RoleEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.configs.database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(SQLAlchemyEnum(RoleEnum), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    permissions = relationship("Permission", secondary="role_permissions", back_populates="roles", cascade="all, delete")
    utilisateurs = relationship("Utilisateur", back_populates="role", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Role {self.nom}>"
