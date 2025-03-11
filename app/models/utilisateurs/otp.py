from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import random
from app.configs.database import Base

class USER_OTP(Base):
    __tablename__ = "utilisateurs_otp"

    id = Column(Integer, primary_key=True, index=True)
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False)
    otp_code = Column(String(5), nullable=False, default=lambda: str(random.randint(10000, 99999)))
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(hours=5), index=True)

    utilisateur = relationship("Utilisateur", back_populates="otps")

    def is_active(self):
        """Vérifie si l'OTP est encore valide."""
        return datetime.utcnow() < self.expires_at

    def __repr__(self):
        return f"<USER_OTP {self.otp_code} (Actif: {self.is_active()}) pour Utilisateur {self.utilisateur_id}>"
