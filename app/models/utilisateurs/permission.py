from sqlalchemy import Column, Integer, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.configs.database import Base
from app.configs.enumerations.Persmissions import PermissionEnum

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(SQLAlchemyEnum(PermissionEnum), nullable=False)  
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    roles = relationship("Role", secondary="role_permissions", back_populates="permissions")
    utilisateurs = relationship("Utilisateur", secondary="user_permissions", back_populates="permissions")

    def __repr__(self):
        return f"<Permission {self.nom}>"
