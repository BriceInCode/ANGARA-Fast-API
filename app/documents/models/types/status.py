# app/documents/models/types/status.py
from enum import Enum

class StatusType(str, Enum):
    EN_COURS = "en_cours"
    VALIDE = "validée"
    REFUSE = "refusée"
