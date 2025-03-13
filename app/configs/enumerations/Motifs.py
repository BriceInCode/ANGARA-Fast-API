from enum import Enum as PyEnum

class MotifEnum(PyEnum):
    # 📌 Motifs liés aux documents
    DOCUMENT_INCOMPLET = "Le dossier soumis est incomplet"
    DOCUMENT_NON_VALIDE = "Le document présenté est périmé ou invalide"
    DOCUMENT_NON_LISIBLE = "Le document est illisible ou endommagé"
    DOCUMENT_NON_AUTHENTIQUE = "Le document semble falsifié ou contrefait"
    DOCUMENT_NON_CONFORME = "Le document ne respecte pas les exigences officielles"
    DOCUMENT_MANQUANT = "Un ou plusieurs documents obligatoires sont absents"
    DOCUMENT_NON_TRADUIT = "Le document n'est pas traduit dans la langue requise"

    # 📌 Motifs liés aux informations fournies
    INFORMATIONS_INCORRECTES = "Les informations fournies ne correspondent pas aux registres officiels"
    DONNEES_INCOHERENTES = "Des incohérences existent entre plusieurs documents"
    IDENTITE_NON_VERIFIEE = "L'identité du demandeur ne peut pas être confirmée"
    INFORMATION_OBSOLETE = "Les informations fournies ne sont plus à jour"
    ADRESSE_NON_VALIDE = "L'adresse fournie n'existe pas ou est erronée"

    # 📌 Motifs administratifs
    DOSSIER_DUPLIQUE = "Une demande similaire a déjà été traitée"
    DOSSIER_NON_AUTORISE = "Le demandeur n’a pas les droits nécessaires pour cette demande"
    NON_RESPECT_DES_DELAIS = "La demande a été faite hors des délais réglementaires"
    ABSENCE_DE_PIECES_JUSTIFICATIVES = "Les pièces justificatives obligatoires ne sont pas fournies"
    DEMANDE_NON_RECEVABLE = "La demande ne remplit pas les conditions requises"
    QUOTA_DEPASSE = "Le nombre maximal de demandes autorisées a été atteint"

    # 📌 Motifs techniques
    ERREUR_ENREGISTREMENT = "Une erreur s’est produite lors du traitement du dossier"
    INCOHERENCE_BASE_DE_DONNEES = "L’information demandée ne correspond pas aux archives officielles"
    SERVICE_TEMPORAIREMENT_INDISPONIBLE = "Le service est momentanément indisponible"
    FORMULAIRE_INVALIDE = "Le formulaire soumis contient des erreurs"
    PROBLEME_CONNEXION = "Un problème de connexion empêche le traitement de la demande"
