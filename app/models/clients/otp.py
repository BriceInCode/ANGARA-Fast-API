from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import random
from app.configs.database import Base

class OTP(Base):
    __tablename__ = "clients_otps"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("clients_sessions.id", ondelete="CASCADE"), nullable=False, unique=True)
    otp_code = Column(String(5), nullable=False, default=lambda: str(random.randint(10000, 99999)))
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=10), index=True)
    session = relationship("Session", back_populates="otp")
