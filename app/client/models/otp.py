# app/client/models/otp.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from app.config.database import Base
import random

class OTP(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False, unique=True)
    otp_code = Column(String(5), nullable=False)  # Le code est généré dans le service
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)

    # Relation avec Session (une session a un seul OTP)
    session = relationship("Session", back_populates="otp")