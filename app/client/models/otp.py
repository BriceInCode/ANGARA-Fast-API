from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import random
from app.config.database import Base

class OTP(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False, unique=True)  # Un OTP par session
    otp_code = Column(String(5), nullable=False, default=lambda: str(random.randint(10000, 99999)))
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=5))  # Expiration après 5 min

    # Relation avec Session (Une session a un seul OTP)
    session = relationship("Session", back_populates="otp")
