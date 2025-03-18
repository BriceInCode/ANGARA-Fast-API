from datetime import datetime
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Any, Dict, Optional, List

from app.models.demandes.demandes import (
    DemandeBase,
    DemandeActeNaissance,
    DemandeActeMariage,
    DemandeActeDeces,
    DemandeCertificatNationalite,
    DemandeCasierJudiciaire,
    DemandePlumitif,
)
from app.configs.enumerations.Documents import DocumentEnum
from app.configs.enumerations.Status import StatusEnum
from app.models.clients.client import Client
from app.configs.enumerations.Raisons import RaisonEnum
from app.configs.enumerations.Sexe import SexeEnum
from app.models.utilisateurs.utilisateur import Utilisateur
from app.schemas.demandes.demande_schema import DemandeActeNaissanceRead
from app.schemas.demandes.motif_schema import MotifCreate
from app.services.demandes.motif_service import MotifService

# =============================================================================
# Classe de base pour les services liés aux demandes
# =============================================================================
class BaseDemandeService:
    def __init__(self, db: Session):
        self.db = db

    def creer_demande(self, data: dict) -> Dict[str, Any]:
        """Méthode abstraite pour créer une demande."""
        raise NotImplementedError

    def modifier_demande(self, demande_id: int, data: dict) -> Dict[str, Any]:
        """Méthode abstraite pour modifier une demande."""
        raise NotImplementedError

    def _commit_and_refresh(self, demande: DemandeBase) -> None:
        """Commit et rafraîchissement de l'objet demande."""
        self.db.commit()
        self.db.refresh(DemandeBase)

    def _create_demande(self, model_class, data: dict, message: str) -> Dict[str, Any]:
        """Méthode générique de création d'une demande."""
        try:
            demande = model_class(**data)
            self.db.add(DemandeBase)
            self._commit_and_refresh(DemandeBase)
            return {"code": 201, "message": f"{message} créé avec succès", "data": demande}
        except SQLAlchemyError as e:
            self.db.rollback()
            return {"code": 500, "message": f"Erreur interne : {str(e)}", "data": None}

    def _modifier_demande(self, demande: DemandeBase, data: dict) -> Dict[str, Any]:
        """Méthode générique de modification d'une demande."""
        try:
            for key, value in data.items():
                setattr(DemandeBase, key, value)
            self._commit_and_refresh(DemandeBase)
            return {"code": 200, "message": "Demande modifiée avec succès", "data": demande}
        except SQLAlchemyError as e:
            self.db.rollback()
            return {"code": 500, "message": f"Erreur interne : {str(e)}", "data": None}

    def _get_demande(self, model_class, demande_id: int) -> Optional[DemandeBase]:
        """Récupère une demande par son ID pour un modèle donné."""
        return self.db.query(model_class).filter(model_class.id == demande_id).first()


# =============================================================================
# Services spécifiques pour chaque type de document
# =============================================================================
class ActeNaissanceService(BaseDemandeService):
    def creer_demande(self, data: dict) -> Dict[str, Any]:
        return self._create_demande(DemandeActeNaissance, data, "Acte de naissance")

    def modifier_demande(self, demande_id: int, data: dict) -> Dict[str, Any]:
        demande = self._get_demande(DemandeActeNaissance, demande_id)
        if not demande:
            return {"code": 404, "message": "Demande d'acte de naissance non trouvée", "data": None}
        return self._modifier_demande(DemandeBase, data)


class ActeMariageService(BaseDemandeService):
    def creer_demande(self, data: dict) -> Dict[str, Any]:
        return self._create_demande(DemandeActeNaissance, data, "Acte de mariage")

    def modifier_demande(self, demande_id: int, data: dict) -> Dict[str, Any]:
        demande = self._get_demande(DemandeActeNaissance, demande_id)
        if not demande:
            return {"code": 404, "message": "Demande d'acte de mariage non trouvée", "data": None}
        return self._modifier_demande(DemandeBase, data)


class ActeDecesService(BaseDemandeService):
    def creer_demande(self, data: dict) -> Dict[str, Any]:
        return self._create_demande(DemandeActeDeces, data, "Acte de décès")

    def modifier_demande(self, demande_id: int, data: dict) -> Dict[str, Any]:
        demande = self._get_demande(DemandeActeDeces, demande_id)
        if not demande:
            return {"code": 404, "message": "Demande d'acte de décès non trouvée", "data": None}
        return self._modifier_demande(DemandeBase, data)


class CertificatNationaliteService(BaseDemandeService):
    def creer_demande(self, data: dict) -> Dict[str, Any]:
        return self._create_demande(DemandeCertificatNationalite, data, "Certificat de nationalité")

    def modifier_demande(self, demande_id: int, data: dict) -> Dict[str, Any]:
        demande = self._get_demande(DemandeCertificatNationalite, demande_id)
        if not demande:
            return {"code": 404, "message": "Demande de certificat de nationalité non trouvée", "data": None}
        return self._modifier_demande(DemandeBase, data)


class ExtraitCasierJudiciaireService(BaseDemandeService):
    def creer_demande(self, data: dict) -> Dict[str, Any]:
        return self._create_demande(DemandeCasierJudiciaire, data, "Extrait du casier judiciaire")

    def modifier_demande(self, demande_id: int, data: dict) -> Dict[str, Any]:
        demande = self._get_demande(DemandeCasierJudiciaire, demande_id)
        if not demande:
            return {"code": 404, "message": "Demande d'extrait du casier judiciaire non trouvée", "data": None}
        return self._modifier_demande(DemandeBase, data)

class ExtraitPlumitifService(BaseDemandeService):
    def creer_demande(self, data: dict) -> Dict[str, Any]:
        return self._create_demande(DemandePlumitif, data, "Extrait plumitif")

    def modifier_demande(self, demande_id: int, data: dict) -> Dict[str, Any]:
        demande = self._get_demande(DemandePlumitif, demande_id)
        if not demande:
            return {"code": 404, "message": "Demande d'extrait plumitif non trouvée", "data": None}
        return self._modifier_demande(DemandeBase, data)


# =============================================================================
# Service principal pour gérer les demandes
# =============================================================================
class DemandeService:
    def __init__(self, db: Session):
        self.db = db
        self.services = {
            DocumentEnum.ACTE_NAISSANCE.value: ActeNaissanceService(db),
            DocumentEnum.ACTE_MARIAGE.value: ActeMariageService(db),
            DocumentEnum.ACTE_DECES.value: ActeDecesService(db),
            DocumentEnum.CERTIFICAT_NATIONALITE.value: CertificatNationaliteService(db),
            DocumentEnum.CASIER_JUDICIAIRE.value: ExtraitCasierJudiciaireService(db),
            DocumentEnum.PLUMITIF.value: ExtraitPlumitifService(db),
        }

    @staticmethod
    def validate_enum_value(value: str, enum_type: Any, error_message: str) -> Optional[Dict[str, Any]]:
        """Vérifie si la valeur appartient à l'énumération donnée."""
        if value not in enum_type.__members__:
            return {"code": 400, "message": error_message, "data": None}
        return None

    def validate_data(self, data: dict) -> Dict[str, Any]:
        """Valide le client et les valeurs d'énumération avant création d'une demande."""
        try:
            # Validation du client
            client = self.db.query(Client).filter(Client.id == data.get("client_id")).first()
            if not client:
                return {"code": 404, "message": "Client non trouvé", "data": None}

            # Validation des énumérations
            for value, enum_type, error_msg in [
                (data.get("type_document"), DocumentEnum, "Type de document invalide."),
                (data.get("raison_demande"), RaisonEnum, "Raison de demande invalide."),
                (data.get("sexe"), SexeEnum, "Genre non pris en charge."),
            ]:
                error = self.validate_enum_value(value, enum_type, error_msg)
                if error:
                    return error

            return {"code": 200, "message": "Validation réussie", "data": data}

        except SQLAlchemyError as e:
            return {"code": 500, "message": f"Erreur interne : {str(e)}", "data": None}

    def generate_unique_demande_number(self) -> str:
        """Génère un numéro unique au format P0-YYYYMMDD-XXXXX."""
        try:
            today_str = datetime.utcnow().strftime("%Y%m%d")
            last_number = (
                self.db.query(DemandeBase.numero_demande)
                .filter(DemandeBase.numero_demande.like(f"P0-{today_str}-%"))
                .order_by(DemandeBase.numero_demande.desc())
                .limit(1)
                .scalar()
            )
            next_number = int(last_number.split("-")[-1]) + 1 if last_number else 1
            return f"P0-{today_str}-{next_number:05d}"
        except SQLAlchemyError as e:
            raise RuntimeError(f"Erreur lors de la génération du numéro de demande : {str(e)}")

    def creer_demande(self, data: dict) -> Dict[str, Any]:
        """Crée une demande après validation et génération d'un numéro unique."""
        try:
            # Conversion des énumérations en chaînes (si nécessaire)
            for key, enum_class in [ ("type_document", DocumentEnum), ("raison_demande", RaisonEnum), ("status", StatusEnum) ]:
                if isinstance(data.get(key), enum_class):
                    data[key] = data[key].value

            # Validation du type de document
            type_document = data.get("type_document")
            if type_document not in [member.value for member in DocumentEnum]:
                return {"code": 400, "message": "Type de document invalide", "data": None}

            # Génération du numéro unique et attribution du statut par défaut
            data["numero_demande"] = self.generate_unique_demande_number()
            data["status"] = StatusEnum.EN_COURS.value

            # Validation spécifique pour l'acte de naissance
            if type_document == DocumentEnum.ACTE_NAISSANCE:
                # Ensure all required fields are present
                required_fields = [
                    "prenom", "nom", "sexe", "date_naissance", "lieu_naissance",
                    "reference_centre_civil", "numero_acte_naissance", "date_creation_acte",
                    "declare_par", "nom_pere", "date_naissance_pere", "lieu_naissance_pere",
                    "profession_pere", "nom_mere", "date_naissance_mere", "lieu_naissance_mere",
                    "profession_mere"
                ]
                for field in required_fields:
                    if field not in data:
                        return {"code": 400, "message": f"Champ requis manquant: {field}", "data": None}

                try:
                    # Utilisation du schéma Pydantic pour valider les données
                    acte_naissance_data = DemandeActeNaissanceRead(**data)
                except ValidationError as e:
                    return { "code": 400, "message": f"Erreur de validation pour un acte de naissance: {e}", "data": None }

            # Sélection du service dédié en fonction du type de document
            service = self.services.get(type_document)
            if not service:
                return {"code": 400, "message": "Type de document invalide", "data": None}

            return service.creer_demande(data)

        except SQLAlchemyError as e:
            self.db.rollback()
            return {"code": 500, "message": f"Erreur interne : {str(e)}", "data": None}


    def _execute_query(self, query, error_message: str) -> Dict[str, Any]:
        """Exécute une requête et gère la réponse en cas d'absence de résultat."""
        try:
            results = query.all()
            if not results:
                return {"code": 404, "message": error_message, "data": None}
            return {"code": 200, "message": "Demandes récupérées avec succès", "data": results}
        except SQLAlchemyError as e:
            return {"code": 500, "message": f"Erreur interne : {str(e)}", "data": None}

    def recuperer_demandes_par_client(self, client_id: int) -> Dict[str, Any]:
        """Récupère toutes les demandes associées à un client."""
        try:
            if not self.db.query(Client).filter(Client.id == client_id).first():
                return {"code": 404, "message": "Client non trouvé", "data": None}
            return self._execute_query(
                self.db.query(DemandeBase).filter(DemandeBase.client_id == client_id),
                "Aucune demande trouvée pour ce client"
            )
        except SQLAlchemyError as e:
            return {"code": 500, "message": f"Erreur interne : {str(e)}", "data": None}

    def recuperer_demandes_bunec(self) -> Dict[str, Any]:
        """Récupère les demandes du BUNEC (acte de naissance, mariage, décès)."""
        try:
            bunec_types = [
                DocumentEnum.ACTE_NAISSANCE.value,
                DocumentEnum.ACTE_MARIAGE.value,
                DocumentEnum.ACTE_DECES.value,
            ]
            return self._execute_query(
                self.db.query(DemandeBase).filter(DemandeBase.type_document.in_(bunec_types)),
                "Aucune demande trouvée pour le BUNEC"
            )
        except SQLAlchemyError as e:
            return {"code": 500, "message": f"Erreur interne : {str(e)}", "data": None}

    def recuperer_demandes_minjustice(self) -> Dict[str, Any]:
        """Récupère les demandes du Ministère de la Justice (certificat de nationalité, casier judiciaire, plumitif)."""
        try:
            minjustice_types = [
                DocumentEnum.CERTIFICAT_NATIONALITE.value,
                DocumentEnum.CASIER_JUDICIAIRE.value,
                DocumentEnum.PLUMITIF.value,
            ]
            return self._execute_query(
                self.db.query(DemandeBase).filter(DemandeBase.type_document.in_(minjustice_types)),
                "Aucune demande trouvée pour le Ministère de la Justice"
            )
        except SQLAlchemyError as e:
            return {"code": 500, "message": f"Erreur interne : {str(e)}", "data": None}

    def recuperer_demandes_par_centre_etat_civil(self, reference_centre_civil: str) -> Dict[str, Any]:
        """Récupère les demandes associées à un centre d'état civil via sa référence."""
        try:
            return self._execute_query(
                self.db.query(DemandeBase).filter(DemandeBase.reference_centre_civil == reference_centre_civil),
                "Aucune demande trouvée pour ce centre d'état civil"
            )
        except SQLAlchemyError as e:
            return {"code": 500, "message": f"Erreur interne : {str(e)}", "data": None}

    def affecter_demandes_a_agent(self, agent_id: int, demande_ids: List[int]) -> Dict[str, Any]:
        """Affecte une ou plusieurs demandes à un agent."""
        try:
            agent = self.db.query(Utilisateur).filter(Utilisateur.id == agent_id).first()
            if not agent:
                return {"code": 404, "message": "Agent non trouvé", "data": None}

            demandes = self.db.query(DemandeBase).filter(DemandeBase.id.in_(demande_ids)).all()
            if not demandes:
                return {"code": 404, "message": "Aucune demande trouvée avec les IDs fournis", "data": None}

            for demande in demandes:
                demande.agent_id = agent.id

            self.db.commit()
            return {"code": 200, "message": "Demandes affectées à l'agent avec succès", "data": demandes}

        except SQLAlchemyError as e:
            self.db.rollback()
            return {"code": 500, "message": f"Erreur interne : {str(e)}", "data": None}

    def recuperer_demandes_par_type_document(self, type_document: str) -> Dict[str, Any]:
        """Récupère les demandes d'un type de document spécifique."""
        try:
            if type_document not in DocumentEnum.__members__:
                return {"code": 400, "message": "Type de document invalide", "data": None}
            return self._execute_query(
                self.db.query(DemandeBase).filter(DemandeBase.type_document == type_document),
                f"Aucune demande trouvée pour le type de document {type_document}"
            )
        except SQLAlchemyError as e:
            return {"code": 500, "message": f"Erreur interne : {str(e)}", "data": None}
