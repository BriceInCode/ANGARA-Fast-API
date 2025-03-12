from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.clients.client import Client
from app.schemas.clients.client_schema import ClientCreate
from app.schemas.clients.session_schema import SessionCreate
from app.services.clients.session_services import SessionService

class ClientService:
    def __init__(self, db: Session):
        self.db = db

    def _serialize_model(self, obj: any) -> Dict:
        """
        Sérialise un objet SQLAlchemy en dictionnaire.
        """
        if not obj:
            return {}
        return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}

    def create_client(self, client_in: ClientCreate) -> Dict[str, Any]:
        try:
            client = self._find_client(email=client_in.email, phone=client_in.phone)
            if not client:
                client = Client(email=client_in.email, phone=client_in.phone)
                self.db.add(client)
                self.db.commit()
                self.db.refresh(client)
                message = "Votre client a été créé avec succès."
            else:
                message = "Le client existe déjà."

            session_response = SessionService(self.db).create_session(
                SessionCreate(client_id=client.id)
            )
            if session_response.get("code") != 200 or not session_response.get("data"):
                return {"code": 500, "message": "La création de la session a échoué.", "data": None}

            data = session_response.get("data")
            serialized_client = self._serialize_model(data.get("client"))
            serialized_session = self._serialize_model(data.get("session"))
            token = data.get("token", None)

            return {
                "code": 201,
                "message": message,
                "data": {"client": serialized_client, "session": serialized_session, "token": token},
            }
        except Exception as e:
            self.db.rollback()
            return {"code": 500, "message": f"Erreur lors de la création du compte : {str(e)}.", "data": None}

    def get_client_by_id(self, client_id: int) -> Dict[str, Any]:
        return self._get_client_by_field("id", client_id, "Client trouvé avec succès.", "Désolé, ce client n'existe pas.")

    def get_client_by_email(self, email: str) -> Dict[str, Any]:
        return self._get_client_by_field("email", email, "Client trouvé avec succès.", "Désolé, ce client n'existe pas.")

    def get_client_by_phone(self, phone: str) -> Dict[str, Any]:
        return self._get_client_by_field("phone", phone, "Client trouvé avec succès.", "Désolé, ce client n'existe pas.")

    def _find_client(self, email: Optional[str] = None, phone: Optional[str] = None) -> Optional[Client]:
        if email:
            client = self.get_client_by_email(email).get("data")
            if client:
                return client
        if phone:
            return self.get_client_by_phone(phone).get("data")
        return None

    def _get_client_by_field(self, field: str, value: any, success_msg: str, error_msg: str) -> Dict[str, Any]:
        client = self.db.query(Client).filter(getattr(Client, field) == value).first()
        if client:
            return {"code": 200, "message": success_msg, "data": client}
        return {"code": 404, "message": error_msg, "data": None}
