from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.config.utils.dependencies import verify_token
from app.documents.schemas.demande import DemandeCreate
from app.documents.services.document_service import DocumentService
from app.documents.services.demande_service import DemandeService
from app.documents.models.types.status import StatusType

router = APIRouter()

# --------------------------------------------------
# Routes "libres" (sans token)
# --------------------------------------------------

# --------------------------------------------------
# Routes sécurisées (token requis)
# --------------------------------------------------

# 📂 Gestion des documents
@router.post("/documents", tags=["Documents"], summary="Uploader un document")
def create_document(
    demande_id: int, document_type: str, file: UploadFile = File(...), 
    token: dict = Depends(verify_token), db: Session = Depends(get_db)
):
    """
    Ajoute un document à une demande.
    """
    service = DocumentService(db)
    result = service.create_document(demande_id, document_type, file)
    return result

@router.put("/documents/{document_id}", tags=["Documents"], summary="Mettre à jour un document")
def update_document(
    document_id: int, file: UploadFile = File(...), 
    token: dict = Depends(verify_token), db: Session = Depends(get_db)
):
    """
    Met à jour un document existant.
    """
    service = DocumentService(db)
    result = service.update_document(document_id, file)
    return result

@router.get("/documents/{document_id}", tags=["Documents"], summary="Récupérer un document")
def get_document(
    document_id: int, token: dict = Depends(verify_token), db: Session = Depends(get_db)
):
    """
    Récupère un document à partir de son ID.
    """
    service = DocumentService(db)
    result = service.get_document(document_id)
    return result

@router.delete("/documents/{document_id}", tags=["Documents"], summary="Supprimer un document")
def delete_document(
    document_id: int, token: dict = Depends(verify_token), db: Session = Depends(get_db)
):
    """
    Supprime un document spécifique.
    """
    service = DocumentService(db)
    result = service.delete_document(document_id)
    if result.get("code") != 200:
        raise HTTPException(status_code=result.get("code"), detail=result.get("message"))
    return result

# 📝 Gestion des demandes


@router.post("/demandes", tags=["Demandes"], summary="Créer une nouvelle demande")
def create_demande(demande_data: DemandeCreate, token: dict = Depends(verify_token), db: Session = Depends(get_db)):
    """
    Crée une demande sans nécessiter de token.
    """
    service = DemandeService(db)
    result = service.create_demande(demande_data)
    return result


@router.get("/demandes/{demande_id}", tags=["Demandes"], summary="Récupérer une demande")
def get_demande(
    demande_id: int, token: dict = Depends(verify_token), db: Session = Depends(get_db)
):
    """
    Récupère une demande spécifique à partir de son ID.
    """
    service = DemandeService(db)
    result = service.get_demande(demande_id)
    return result

@router.get("/demandes", tags=["Demandes"], summary="Récupérer toutes les demandes")
def get_all_demandes(token: dict = Depends(verify_token), db: Session = Depends(get_db)):
    """
    Récupère toutes les demandes.
    """
    service = DemandeService(db)
    result = service.get_all_demandes()
    return result

@router.get("/demandes/session/{session_id}", tags=["Demandes"], summary="Récupérer les demandes d'un client")
def get_demandes_by_session_id(
    session_id: int, token: dict = Depends(verify_token), db: Session = Depends(get_db)
):
    """
    Récupère toutes les demandes associées à un client.
    """
    service = DemandeService(db)
    result = service.get_demandes_by_session_id(session_id)
    return result

@router.put("/demandes/{demande_id}", tags=["Demandes"], summary="Mettre à jour une demande")
def update_demande(
    demande_id: int, demande_data: DemandeCreate, 
    token: dict = Depends(verify_token), db: Session = Depends(get_db)
):
    """
    Met à jour les informations d'une demande existante.
    """
    service = DemandeService(db)
    result = service.update_demande(demande_id, demande_data)
    return result

@router.delete("/demandes/{demande_id}", tags=["Demandes"], summary="Supprimer une demande")
def delete_demande(
    demande_id: int, token: dict = Depends(verify_token), db: Session = Depends(get_db)
):
    """
    Supprime une demande spécifique.
    """
    service = DemandeService(db)
    result = service.delete_demande(demande_id)
    if result.get("code") != 200:
        raise HTTPException(status_code=result.get("code"), detail=result.get("message"))
    return result

@router.patch("/demandes/{demande_id}/status", tags=["Demandes"], summary="Mettre à jour le statut d'une demande")
def update_demande_status(
    demande_id: int, new_status: StatusType, 
    token: dict = Depends(verify_token), db: Session = Depends(get_db)
):
    """
    Met à jour le statut d'une demande (ex: En cours, Validée, Rejetée...).
    """
    service = DemandeService(db)
    result = service.update_demande_status(demande_id, new_status)
    return result
