from sqlalchemy.orm import Session
from app.client.models.client import Client
from app.client.schemas.session import SessionCreate
from app.client.schemas.client import ClientCreate
from app.client.services.session_service import SessionService
from app.client.schemas.client import ClientRead
from app.client.schemas.session import SessionRead
from typing import Dict, Any

class ClientService:
    def __init__(self, db: Session):
        self.db = db

    def create_client_and_session(self, client_data: ClientCreate) -> Dict[str, Any]:
        """Crée un client et une session associée, ou récupère le client existant."""
        client = None
        if client_data.email:
            client = self.get_client_by_email(client_data.email).get("data")
        if not client and client_data.phone:
            client = self.get_client_by_phone(client_data.phone).get("data")

        if not client:
            # Création du client s'il n'existe pas
            client = Client(email=client_data.email, phone=client_data.phone)
            self.db.add(client)
            self.db.commit()
            self.db.refresh(client)
            creation_message = "Client créé avec succès"
        else:
            creation_message = "Client déjà existant"

        # Création de la session associée
        session_service = SessionService(self.db)
        session_response = session_service.create_session(SessionCreate(client_id=client.id))
        
        # Conversion des objets ORM en modèles Pydantic pour la sérialisation
        client_data_out = ClientRead.from_orm(client)
        session_data_out = SessionRead.from_orm(session_response.get("data"))

        return {
            "code": 200,
            "message": f"{creation_message} et session créée.",
            "data": {"client": client_data_out, "session": session_data_out}
        }


    def get_client_by_id(self, client_id: int) -> Dict[str, Any]:
        """Récupère un client par son ID."""
        client = self.db.query(Client).filter(Client.id == client_id).first()
        return {
            "code": 200 if client else 404,
            "message": "Client trouvé avec succès." if client else "Désolé mais ce client n'existe pas dans notre système.",
            "data": client
        }

    def get_client_by_email(self, email: str) -> Dict[str, Any]:
        """Récupère un client par son adresse e-mail."""
        client = self.db.query(Client).filter(Client.email == email).first()
        return {
            "code": 200 if client else 404,
            "message": "Client trouvé avec succès." if client else "Désolé mais ce client n'existe pas dans notre système.",
            "data": client
        }

    def get_client_by_phone(self, phone: str) -> Dict[str, Any]:
        """Récupère un client par son numéro de téléphone."""
        client = self.db.query(Client).filter(Client.phone == phone).first()
        return {
            "code": 200 if client else 404,
            "message": "Client trouvé avec succès." if client else "Désolé mais ce client n'existe pas dans notre système.",
            "data": client
        }

    def get_all_clients(self) -> Dict[str, Any]:
        """Récupère la liste de tous les clients."""
        clients = self.db.query(Client).all()
        return {
            "code": 200,
            "message": "Liste des clients récupérée avec succès.",
            "data": clients
        }

    def delete_client(self, client_id: int) -> Dict[str, Any]:
        """Supprime un client existant."""
        client = self.db.query(Client).filter(Client.id == client_id).first()
        if client:
            self.db.delete(client)
            self.db.commit()
            return {
                "code": 200,
                "message": "Client supprimé avec succès.",
                "data": client
            }
        return {
            "code": 404,
            "message": "Désolé mais ce client n'existe pas dans notre système.",
            "data": None
        }

    def activate_client_session(self, client_id: int, session_id: int, otp_code: str) -> Dict[str, Any]:
        """Active une session spécifique pour un client en désactivant les autres sessions actives."""
        client = self.get_client_by_id(client_id).get("data")

        if not client:
            return {
                "code": 404,
                "message": "Désolé mais ce client n'existe pas dans notre système.",
                "data": None
            }

        session_service = SessionService(self.db)
        session_response = session_service.activate_session(session_id, otp_code)

        return {
            "code": session_response.get("code"),
            "message": session_response.get("message"),
            "data": session_response.get("data")
        }
