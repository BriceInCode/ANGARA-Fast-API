# app/client/models/client.py
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=True)
    phone = Column(String(20), unique=True, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Un client peut avoir plusieurs sessions
    sessions = relationship("Session", back_populates="client", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('email', 'phone', name='unique_email_phone'),
        CheckConstraint('email IS NOT NULL OR phone IS NOT NULL', name='check_email_or_phone')
    )
