# app/documents/models/request.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.database import Base
from app.documents.models.types.gender import GenderType
from app.documents.models.types.documents import DocumentsType
from app.documents.models.types.raisons import RaisonsType
from app.documents.models.types.status import StatusType

class Demande(Base):
    __tablename__ = "demandes"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("clients_sessions.id", ondelete="CASCADE"), nullable=False)
    request_number = Column(String(22), unique=True, nullable=False)

    document_type = Column(SAEnum(DocumentsType), nullable=False)
    request_reason = Column(SAEnum(RaisonsType), nullable=False)
    civil_center_reference = Column(String(255), nullable=False)
    birth_act_number = Column(String(255), nullable=False)
    birth_act_creation_date = Column(DateTime, nullable=False)
    declaration_by = Column(String(255), nullable=False)
    authorized_by = Column(String(255), nullable=True)

    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=False)
    gender = Column(SAEnum(GenderType), nullable=False)
    birth_date = Column(DateTime, nullable=False)
    birth_place = Column(String(255), nullable=False)

    father_name = Column(String(255), nullable=False)
    father_birth_date = Column(DateTime, nullable=True)
    father_birth_place = Column(String(255), nullable=True)
    father_profession = Column(String(255), nullable=True)

    mother_name = Column(String(255), nullable=False)
    mother_birth_date = Column(DateTime, nullable=True)
    mother_birth_place = Column(String(255), nullable=True)
    mother_profession = Column(String(255), nullable=True)

    status = Column(SAEnum(StatusType), nullable=False, default=StatusType.EN_COURS)

    # Relations
    session = relationship("Session", back_populates="demandes")
    document = relationship("Document", back_populates="demande", uselist=False, cascade="all, delete-orphan")
