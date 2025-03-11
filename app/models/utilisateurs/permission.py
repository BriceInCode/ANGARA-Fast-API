from sqlalchemy import Column, Integer, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.configs.database import Base
from app.configs.enumerations.Persmissions import PermissionEnum
from app.models.utilisateurs.role import role_permissions, user_permissions

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(SQLAlchemyEnum(PermissionEnum), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")
    utilisateurs = relationship("Utilisateur", secondary=user_permissions, back_populates="permissions")

    def __repr__(self):
        return f"<Permission {self.nom}>"
