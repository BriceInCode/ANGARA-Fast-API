from enum import Enum as PyEnum

class DocumentEnum(PyEnum):
    ACTE_NAISSANCE = "Acte de naissance"
    ACTE_MARIAGE = "Acte de mariage"
    ACTE_DECES = "Acte de décès"
    CERTIFICAT_NATIONALITE = "Certificat de nationalité"
    CASIER_JUDICIAIRE = "Extrait du casier judiciaire"
    PLUMITIF = "Extrait du plumitif"
