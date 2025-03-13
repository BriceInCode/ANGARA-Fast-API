from typing import List
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.configs.enumerations.Comptes import ComptesEnum
from app.schemas.utilisateurs.utilisateur_schema import UtilisateurCreate, UtilisateurRead
from app.services.utilisateurs.utilisateur_service import UtilisateurService

router = APIRouter(prefix="/utilisateurs", tags=["Utilisateurs"])

@router.post("/", response_model=UtilisateurRead, summary="Créer un utilisateur", description="Créer un nouvel utilisateur et envoyer un email de bienvenue")
def create_utilisateur(utilisateur_data: UtilisateurCreate = Body(..., example={
    "nom": "Doe",
    "prenom": "John",
    "email": "john.doe@example.com",
    "role_id": 1,
    "organisation_id": 1,
    "status": ComptesEnum.ACTIF
}), db: Session = Depends(get_db)):
    # Permission: CREER_UTILISATEUR
    service = UtilisateurService(db)
    result = service.create_utilisateur(utilisateur_data)
    if result["code"] != 201:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result["data"]

@router.get("/{param}", response_model=UtilisateurRead, summary="Obtenir un utilisateur", description="Obtenir un utilisateur par ID ou par email")
def get_utilisateur(param: str, db: Session = Depends(get_db)):
    # Permission: VOIR_UTILISATEUR
    result = UtilisateurService.get_utilisateur(db, param)  # Appel de la méthode de classe
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result["data"]

@router.get("/", response_model=List[UtilisateurRead], summary="Obtenir tous les utilisateurs", description="Récupérer la liste de tous les utilisateurs")
def get_all_utilisateurs(db: Session = Depends(get_db)):
    # Permission: LISTER_UTILISATEURS
    service = UtilisateurService(db)  # Créer une instance avec la session
    result = service.get_all_utilisateurs()
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result["data"]

@router.get("/role/{role}", response_model=List[UtilisateurRead], summary="Obtenir les utilisateurs par rôle")
def get_utilisateurs_by_role(role: str, db: Session = Depends(get_db)):
    # Permission: LISTER_UTILISATEURS_PAR_ROLE
    result = UtilisateurService.get_utilisateurs_by_role(db, role)
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result["data"]

@router.get("/organisation/{organisation}", response_model=List[UtilisateurRead], summary="Obtenir des utilisateurs par organisation", description="Récupérer les utilisateurs en fonction de leur organisation")
def get_utilisateurs_by_organisation(organisation: str, db: Session = Depends(get_db)):
    # Permission: LISTER_UTILISATEURS_PAR_ORGANISATION
    result = UtilisateurService.get_utilisateurs_by_organisation(db, organisation)
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result["data"]

@router.get("/centre/{centre}", response_model=List[UtilisateurRead], summary="Obtenir des utilisateurs par centre", description="Récupérer les utilisateurs en fonction de leur centre d'état civil")
def get_utilisateurs_by_centre(centre: str, db: Session = Depends(get_db)):
    # Permission: LISTER_UTILISATEURS_PAR_CENTRE
    result = UtilisateurService.get_utilisateurs_by_centre(db, centre)
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result["data"]

@router.put("/{utilisateur_id}", response_model=UtilisateurRead, summary="Mettre à jour un utilisateur", description="Mettre à jour les informations d'un utilisateur existant")
def update_utilisateur(utilisateur_id: int, updates: UtilisateurCreate = Body(..., example={
    "nom": "Doe",
    "prenom": "John",
    "email": "john.doe@example.com",
    "role_id": 1,
    "organisation_id": 1,
    "status": ComptesEnum.ACTIF
}), db: Session = Depends(get_db)):
    # Permission: MODIFIER_UTILISATEUR
    result = UtilisateurService.update_utilisateur(db, utilisateur_id, updates.dict())
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result["data"]

@router.delete("/{utilisateur_id}", summary="Supprimer un utilisateur", description="Supprimer un utilisateur existant")
def delete_utilisateur(utilisateur_id: int, db: Session = Depends(get_db)):
    # Permission: SUPPRIMER_UTILISATEUR
    result = UtilisateurService.delete_utilisateur(db, utilisateur_id)
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result

@router.put("/organisation/assign", summary="Affecter un utilisateur à une organisation", description="Assigner un utilisateur à une organisation en précisant l'utilisateur assignant et l'utilisateur affecté")
def assign_user_to_organisation(data: dict = Body(..., example={
    "assigner_id": 1,
    "utilisateur_id": 2,
    "organisation_id": 1
}), db: Session = Depends(get_db)):
    # Permission: AFFECTER_UTILISATEUR_A_ORGANISATION
    assigner_id = data.get("assigner_id")
    utilisateur_id = data.get("utilisateur_id")
    organisation_id = data.get("organisation_id")
    # Vérification de la présence des trois paramètres
    if not all([assigner_id, utilisateur_id, organisation_id]):
        raise HTTPException(status_code=400, detail="assigner_id, utilisateur_id et organisation_id sont requis")
    # Appel à la méthode de service pour affecter l'utilisateur
    result = UtilisateurService.assign_user_to_organisation(db, assigner_id, utilisateur_id, organisation_id)
    # Gestion des erreurs
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    # Retour des données après succès
    return result

@router.put("/centre/assign", summary="Affecter un utilisateur à un centre", description="Assigner un utilisateur à un centre en précisant l'utilisateur assignant et l'utilisateur affecté")
def assign_user_to_centre(data: dict = Body(..., example={
    "assigner_id": 1,
    "utilisateur_id": 2,
    "centre_id": 1
}), db: Session = Depends(get_db)):
    # Permission: AFFECTER_UTILISATEUR_A_CENTRE
    assigner_id = data.get("assigner_id")
    utilisateur_id = data.get("utilisateur_id")
    centre_id = data.get("centre_id")
    if not all([assigner_id, utilisateur_id, centre_id]):
        raise HTTPException(status_code=400, detail="assigner_id, utilisateur_id et centre_id sont requis")
    result = UtilisateurService.assign_user_to_centre(db, assigner_id, utilisateur_id, centre_id)
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result["data"]

@router.put("/permissions/assign", summary="Affecter des permissions à un utilisateur", description="Assigner des permissions à un utilisateur en précisant l'utilisateur assignant et les permissions à affecter")
def assign_permissions_to_user(data: dict = Body(..., example={
    "assigner_id": 1,
    "utilisateur_id": 2,
    "permissions": [1, 2, 3]
}), db: Session = Depends(get_db)):
    # Permission: AFFECTER_PERMISSIONS_A_UTILISATEUR
    assigner_id = data.get("assigner_id")
    utilisateur_id = data.get("utilisateur_id")
    permissions = data.get("permissions")
    if not all([assigner_id, utilisateur_id, permissions]):
        raise HTTPException(status_code=400, detail="assigner_id, utilisateur_id et permissions sont requis")
    result = UtilisateurService.assign_permissions_to_user(db, assigner_id, utilisateur_id, permissions)
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result["data"]


# Route pour retirer un utilisateur d'un centre@router.delete("/utilisateur/{utilisateur_id}/centre", response_model=dict)
@router.delete("/utilisateur/{utilisateur_id}/centre", response_model=dict)
def remove_utilisateur_from_centre(utilisateur_id: int, db: Session = Depends(get_db)):
    utilisateur_service = UtilisateurService(db)  # Instancie le service avec db
    result = utilisateur_service.remove_utilisateur_from_centre(utilisateur_id)  # Passe correctement utilisateur_id
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result

@router.put("/utilisateur/{utilisateur_id}/role", summary="Changer le rôle d'un utilisateur", description="Cette route permet de modifier le rôle d'un utilisateur en spécifiant son ID et le nouvel ID du rôle. Seules les personnes autorisées peuvent effectuer cette action.")
def change_role(utilisateur_id: int, data: dict = Body(..., example={"new_role_id": 2}), db: Session = Depends(get_db)):
    new_role_id = data.get("new_role_id")
    if not new_role_id:
        raise HTTPException(status_code=400, detail="Le champ 'new_role_id' est requis")
    result = UtilisateurService.change_role(db, utilisateur_id, new_role_id)
    if result["code"] != 200:
        raise HTTPException(status_code=result["code"], detail=result["message"])
    return result["data"]