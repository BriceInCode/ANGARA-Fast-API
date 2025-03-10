# app/models/gender.py
from enum import Enum

class GenderType(str, Enum):
    MASCULIN = "MASCULIN"
    FEMININ = "FEMININ"
