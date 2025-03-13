from enum import Enum as PyEnum

class RoleEnum(str , PyEnum):
    SUPER_ADMINISTRATEUR = "Super Administrateur"
    ADMINISTRATEUR = "Administrateur"
    AGENT = "Agent"
    OPERATEUR_SUR_SITE = "Opérateur sur site"
