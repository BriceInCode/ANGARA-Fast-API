from enum import Enum as PyEnum

class StatusEnum(PyEnum):
    EN_COURS = "En cours"
    VALIDE = "Validée"
    REJETE = "Rejetée"
    TRANSFERE = "Transférée"
