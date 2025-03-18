from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.schemas.demandes.motif_schema import MotifCreate, MotifRead
from app.services.demandes.motif_service import MotifService

router = APIRouter(
    prefix="/motifs",
    tags=["Motifs"]
)

@router.post("", summary="Créer un motif", response_model=MotifRead)
def create_motif(motif_in: MotifCreate = Body(..., example={
    "motif": "AUTRE",
    "description": "Description par défaut"
}), db: Session = Depends(get_db)):
    response = MotifService.create_motif(db, motif_in)
    if response["code"] != 201:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response["data"]

@router.get("/{motif_id}", summary="Obtenir un motif par ID", response_model=MotifRead)
def get_motif_by_id(motif_id: int, db: Session = Depends(get_db)):
    response = MotifService.get_motif_by_id(db, motif_id)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response["data"]

@router.get("", summary="Obtenir tous les motifs", response_model=list[MotifRead])
def get_all_motifs(db: Session = Depends(get_db)):
    response = MotifService.get_all_motifs(db)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return response["data"]

@router.delete("/{motif_id}", summary="Supprimer un motif")
def delete_motif(motif_id: int, db: Session = Depends(get_db)):
    response = MotifService.delete_motif(db, motif_id)
    if response["code"] != 200:
        raise HTTPException(status_code=response["code"], detail=response["message"])
    return {"message": response["message"]}
