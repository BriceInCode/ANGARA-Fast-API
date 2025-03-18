from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List

from app.services.demandes.demande_service import DemandeService
from app.schemas.demandes.demande_schema import DemandeBase, DemandeReadBase
from app.configs.database import get_db
from app.configs.enumerations.Documents import DocumentEnum
from app.configs.enumerations.Raisons import RaisonEnum
from app.configs.enumerations.Status import StatusEnum

router = APIRouter()

# Dépendance pour obtenir le service DemandeService
def get_demande_service(db: Session = Depends(get_db)):
    return DemandeService(db)

@router.post("/demandes/", response_model=DemandeReadBase, tags=["Demandes"])
def creer_demande(
    data: DemandeBase = Body(
        ...,
        example={
            "client_id": 1,
            "type_document": DocumentEnum.ACTE_NAISSANCE.value,
            "raison_demande": RaisonEnum.PERTE_DOCUMENT.value,
            "status": StatusEnum.EN_COURS.value,
            "motif_id": None,
            "reference_centre_civil": "CEC-YAO-003",
            "numero_acte_naissance": "ACTE2025001234",
            "date_creation_acte": "2025-03-01T00:00:00",
            "declare_par": "Paul Dupont",
            "autorise_par": "Marie Claire",
            "nom_pere": "Paul Dupont",
            "date_naissance_pere": "1980-07-12T00:00:00",
            "lieu_naissance_pere": "Yaoundé",
            "profession_pere": "Ingénieur",
            "nom_mere": "Marie Claire",
            "date_naissance_mere": "1983-04-05T00:00:00",
            "lieu_naissance_mere": "Douala",
            "profession_mere": "Médecin",
            "prenom": "Jean",
            "nom": "Dupont",
            "sexe": "MASCULIN",
            "date_naissance": "2003-02-28T00:00:00",
            "lieu_naissance": "Douala"
        }
    ),
    service: DemandeService = Depends(get_demande_service)
):
    """
    Crée une nouvelle demande.
    """
    try:
        result = service.creer_demande(data.dict())
        if result["code"] != 201:
            raise HTTPException(status_code=result["code"], detail=result["message"])
        return result["data"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/demandes/{demande_id}", response_model=DemandeReadBase, tags=["Demandes"])
def modifier_demande(
    demande_id: int,
    data: DemandeBase = Body(
        ...,
        example={
            "client_id": 1,
            "type_document": DocumentEnum.ACTE_NAISSANCE.value,
            "raison_demande": RaisonEnum.VOL_DOCUMENT.value,
            "status": StatusEnum.VALIDE.value,
            "motif_id": 2,
            "reference_centre_civil": "CEC-YAO-003",
            "date_creation": "2023-10-01T00:00:00",
            "date_modification": "2023-10-05T00:00:00"
        }
    ),
    service: DemandeService = Depends(get_demande_service)
):
    """
    Modifie une demande existante.
    """
    try:
        result = service.modifier_demande(demande_id, data.dict())
        if result["code"] != 200:
            raise HTTPException(status_code=result["code"], detail=result["message"])
        return result["data"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/demandes/client/{client_id}", response_model=List[DemandeReadBase], tags=["Demandes"])
def recuperer_demandes_par_client(client_id: int, service: DemandeService = Depends(get_demande_service)):
    """
    Récupère toutes les demandes d'un client.
    """
    result = service.recuperer_demandes_par_client(client_id)
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result["data"]

@router.get("/demandes/bunec", response_model=List[DemandeReadBase], tags=["Demandes"])
def recuperer_demandes_bunec(service: DemandeService = Depends(get_demande_service)):
    """
    Récupère les demandes du BUNEC (Actes de naissance, mariage, décès).
    """
    result = service.recuperer_demandes_bunec()
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result["data"]

@router.get("/demandes/minjustice", response_model=List[DemandeReadBase], tags=["Demandes"])
def recuperer_demandes_minjustice(service: DemandeService = Depends(get_demande_service)):
    """
    Récupère les demandes du Ministère de la Justice (Certificat de nationalité, extrait du casier judiciaire, extrait plumitif).
    """
    result = service.recuperer_demandes_minjustice()
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result["data"]

@router.get("/demandes/centre/{reference_centre_civil}", response_model=List[DemandeReadBase], tags=["Demandes"])
def recuperer_demandes_par_centre_etat_civil(reference_centre_civil: str, service: DemandeService = Depends(get_demande_service)):
    """
    Récupère toutes les demandes d'un centre d'état civil.
    """
    result = service.recuperer_demandes_par_centre_etat_civil(reference_centre_civil)
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result["data"]

@router.post("/demandes/affecter", response_model=List[DemandeReadBase], tags=["Demandes"])
def affecter_demandes_a_agent(
    agent_id: int,
    demande_ids: List[int] = Body(
        ...,
        example=[1, 2, 3]
    ),
    service: DemandeService = Depends(get_demande_service)
):
    """
    Affecte une ou plusieurs demandes à un agent.
    """
    result = service.affecter_demandes_a_agent(agent_id, demande_ids)
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result["data"]

@router.get("/demandes/type/{type_document}", response_model=List[DemandeReadBase], tags=["Demandes"])
def recuperer_demandes_par_type_document(type_document: str, service: DemandeService = Depends(get_demande_service)):
    """
    Récupère toutes les demandes d'un type de document spécifique.
    """
    result = service.recuperer_demandes_par_type_document(type_document)
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result["data"]
