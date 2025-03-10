from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from app.config.database import Base

class Session(Base):
    __tablename__ = "clients_sessions"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(hours=2), index=True)

    # Relation avec Client (un client peut avoir plusieurs sessions)
    client = relationship("Client", back_populates="sessions")

    # Une session possède un seul OTP (cascade pour suppression)
    otp = relationship("OTP", back_populates="session", uselist=False, cascade="all, delete-orphan")

    # __table_args__ = (
    #     UniqueConstraint('client_id', 'is_active', name='unique_active_session_per_client'),
    # )
