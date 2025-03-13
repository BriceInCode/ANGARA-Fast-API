from enum import Enum as PyEnum

class PermissionEnum(PyEnum):
    # Permissions liées aux utilisateurs
    CREER_UTILISATEUR = "Créer un utilisateur"
    LIRE_UTILISATEUR = "Consulter un utilisateur"
    MODIFIER_UTILISATEUR = "Modifier un utilisateur"
    SUPPRIMER_UTILISATEUR = "Supprimer un utilisateur"
    ACTIVER_DESACTIVER_UTILISATEUR = "Activer/Désactiver un utilisateur"
    REINITIALISER_MOT_DE_PASSE = "Réinitialiser le mot de passe d'un utilisateur"
    
    # Permissions liées aux rôles et permissions
    CREER_ROLE = "Créer un rôle"
    LIRE_ROLE = "Consulter un rôle"
    MODIFIER_ROLE = "Modifier un rôle"
    SUPPRIMER_ROLE = "Supprimer un rôle"
    ASSIGNER_PERMISSION = "Assigner des permissions à un rôle"
    
    # Permissions liées aux demandes
    CREER_DEMANDE = "Créer une demande"
    LIRE_DEMANDE = "Consulter une demande"
    MODIFIER_DEMANDE = "Modifier une demande"
    SUPPRIMER_DEMANDE = "Supprimer une demande"
    VALIDER_DEMANDE = "Valider une demande"
    REJETER_DEMANDE = "Rejeter une demande"
    TRANSFERER_DEMANDE = "Transférer une demande"
    AFFECTER_AGENT = "Affecter un agent à une demande"
    REASSIGNER_AGENT = "Réassigner un agent"
    
    # Permissions liées aux documents
    CREER_DOCUMENT = "Créer un document"
    LIRE_DOCUMENT = "Consulter un document"
    MODIFIER_DOCUMENT = "Modifier un document"
    SUPPRIMER_DOCUMENT = "Supprimer un document"
    AUTHENTIFIER_DOCUMENT = "Authentifier un document"
    CERTIFIER_DOCUMENT = "Certifier un document"
    
    # Permissions liées aux clients
    CREER_CLIENT = "Créer un client"
    LIRE_CLIENT = "Consulter un client"
    MODIFIER_CLIENT = "Modifier un client"
    SUPPRIMER_CLIENT = "Supprimer un client"
    
    # Permissions liées aux motifs de rejet
    CREER_MOTIF = "Créer un motif de rejet"
    LIRE_MOTIF = "Consulter un motif de rejet"
    MODIFIER_MOTIF = "Modifier un motif de rejet"
    SUPPRIMER_MOTIF = "Supprimer un motif de rejet"
    
    # Permissions liées aux statistiques et audits
    CONSULTER_STATISTIQUES = "Consulter les statistiques"
    GENERER_RAPPORT = "Générer un rapport"
    CONSULTER_HISTORIQUE_ACTIONS = "Consulter l'historique des actions"
    
    # Permissions liées aux organisations
    CREER_ORGANISATION = "Créer une organisation"
    LIRE_ORGANISATION = "Consulter une organisation"
    MODIFIER_ORGANISATION = "Modifier une organisation"
    SUPPRIMER_ORGANISATION = "Supprimer une organisation"

    # Permissions générales
    EXPORTER_DONNEES = "Exporter des données"
    IMPORTER_DONNEES = "Importer des données"
    GESTION_PARAMETRES = "Gérer les paramètres du système"

    # Permissions liées à la gestion des clients
    GESTION_CLIENTS = "Gérer les clients"
    VIEW_CLIENTS = "Voir la liste des clients"
    CREATE_CLIENT = "Créer un client"
    EDIT_CLIENT = "Modifier un client"
    DELETE_CLIENT = "Supprimer un client"
    VIEW_CLIENT_DETAILS = "Voir les détails d'un client"

    # Permissions liées à la gestion des sessions
    GESTION_SESSIONS = "Gérer les sessions"
    VIEW_SESSIONS = "Voir la liste des sessions"
    CREATE_SESSION = "Créer une session"
    ACTIVATE_SESSION = "Activer une session"
    EDIT_SESSION = "Modifier une session"
    DELETE_SESSION = "Supprimer une session"
    VIEW_SESSION_DETAILS = "Voir les détails d'une session"

    # Permissions liées à la gestion des OTP
    GESTION_OTP = "Gérer les OTP"
    VIEW_OTPS = "Voir la liste des OTP"
    CREATE_OTP = "Créer un OTP"
    VALIDATE_OTP = "Valider un OTP"
    DELETE_OTP = "Supprimer un OTP"
    VIEW_OTP_DETAILS = "Voir les détails d'un OTP"
    
    # Permissions liées aux centres d'état civil
    GESTION_CENTRE_ETAT_CIVIL = "Gérer les centres d'état civil"
    CREER_CENTRE_ETAT_CIVIL = "Créer un centre d'état civil"
    VOIR_CENTRE_ETAT_CIVIL = "Voir un centre d'état civil"
    MODIFIER_CENTRE_ETAT_CIVIL = "Modifier un centre d'état civil"
    SUPPRIMER_CENTRE_ETAT_CIVIL = "Supprimer un centre d'état civil"
    CONSULTER_UTILISATEURS_CENTRE = "Consulter les utilisateurs d'un centre d'état civil"

    # Permissions liées aux organisations
    GESTION_ORGANISATIONS = "Gérer les organisations"
    VOIR_ORGANISATION = "Voir une organisation"
    CONSULTER_UTILISATEURS_ORGANISATION = "Consulter les utilisateurs d'une organisation"
