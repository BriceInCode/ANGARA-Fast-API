from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.database import Base

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    is_active = Column(Boolean, default=False)  # Une seule session active à la fois
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relation avec Client (Un client peut avoir plusieurs sessions)
    client = relationship("Client", back_populates="sessions")

    # Relation avec OTP (Une session a un seul OTP)
    otp = relationship("OTP", back_populates="session", uselist=False, cascade="all, delete-orphan")

    # Contrainte pour garantir qu'une seule session est active à la fois pour un client donné
    __table_args__ = (
        UniqueConstraint('client_id', 'is_active', name='unique_active_session_per_client'),
    )
