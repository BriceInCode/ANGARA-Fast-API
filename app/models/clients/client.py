from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint, CheckConstraint
from datetime import datetime
from app.configs.database import Base
from sqlalchemy.orm import relationship
from app.models.demandes.demandes import Demande

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=True)
    phone = Column(String(20), unique=True, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relation avec Session
    sessions = relationship("Session", back_populates="client", cascade="all, delete-orphan")
    
    # Relation avec Demande (un client peut avoir plusieurs demandes)
    demandes = relationship("Demande", back_populates="client", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('email', 'phone', name='unique_email_phone'),
        CheckConstraint('email IS NOT NULL OR phone IS NOT NULL', name='check_email_or_phone')
    )

    def __repr__(self):
        return f"<Client {self.email if self.email else self.phone}>"
