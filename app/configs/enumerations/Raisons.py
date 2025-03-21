from enum import Enum as PyEnum

class RaisonEnum(PyEnum):
    PERTE_DOCUMENT = "Perte du document"
    VOL_DOCUMENT = "Vol du document"
    DETERIORATION_DOCUMENT = "Détérioration du document"
    RECTIFICATION_ERREUR = "Rectification d’une erreur sur le document"
    CHANGEMENT_ETAT_CIVIL = "Changement d’état civil"
    UTILISATION_ETRANGER = "Utilisation du document à l’étranger"
    DEMANDE_DUPLICATA = "Demande d’un duplicata"
    EXIGENCE_ADMINISTRATIVE = "Exigence d’une administration ou d’un organisme"
    REGULARISATION_SITUATION = "Régularisation d’une situation légale"
    DEMANDE_PERSONNELLE = "Demande personnelle"
    DOSSIER_SCOLAIRE = "Constitution d’un dossier scolaire"
    EMPLOI_RECRUTEMENT = "Dossier pour un emploi ou un recrutement"
    DEMANDE_VISA = "Demande de visa ou d’immigration"
    SUCCESSION_HERITAGE = "Procédure de succession ou d’héritage"
    MARIAGE = "Constitution d’un dossier de mariage"
    CREATION_ENTREPRISE = "Formalités pour la création d’entreprise"
    DOSSIER_BANCAIRE = "Exigences d’une banque pour ouverture de compte"
