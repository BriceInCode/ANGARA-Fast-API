from sqlalchemy import Column, Integer, Text, DateTime, func, Enum as SQLAlchemyEnum
from app.configs.database import Base
from app.configs.enumerations.Motifs import MotifEnum

class Motif(Base):
    __tablename__ = "motifs_demandes"

    id = Column(Integer, primary_key=True, index=True)
    motif = Column(SQLAlchemyEnum(MotifEnum), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<Motif {self.id} - {self.motif.value}>"
