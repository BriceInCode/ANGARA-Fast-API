from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.configs.database import init_db

# Importation des routes
from app.routes.clients.client_routes import router as client_router
from app.routes.clients.session_routes import router as session_router
from app.routes.clients.otp_routes import router as otp_router
from app.routes.organisations.organisations_routes import router as organisation_router
from app.routes.organisations.centres_etat_civil_routes import router as centre_etat_civil_router
from app.routes.utilisateurs.auth_routes import router as auth_router  # Importer les routes d'authentification
from app.routes.utilisateurs.role_routes import router as role_router  # Importer la route pour les rôles
from app.routes.utilisateurs.permission_routes import router as permission_router  # Importer la route pour les permissions
from app.routes.utilisateurs.utilisateur_routes import router as utilisateur_router  # Importer la route pour les utilisateurs

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],  # Affichage des logs dans la console
)
logger = logging.getLogger(__name__)

# Gestion du cycle de vie de l'application
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("🔄 Initialisation de la base de données...")
        init_db()
        logger.info("✅ Base de données initialisée avec succès")
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'initialisation de la base de données: {e}")
    yield  # Actions supplémentaires peuvent être ajoutées ici

# Création de l'application FastAPI
app = FastAPI(
    title="ANGARA-AUTHENTIC API",
    description="Une API pour générer des documents certifiés",
    version="1.0",
    contact={
        "name": "Support ANGARA-AUTHENTIC",
        "email": "norepleysjm@gmail.com"
    },
    lifespan=lifespan,  # Gestion optimisée des événements de démarrage
)

# Configuration CORS (⚠️ Modifier pour la production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔴 ⚠️ À modifier avec des domaines spécifiques en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes
app.include_router(client_router)
app.include_router(session_router)
app.include_router(otp_router)
app.include_router(organisation_router)
app.include_router(centre_etat_civil_router)
app.include_router(auth_router)  # Inclusion des routes d'authentification
app.include_router(role_router)  # Inclusion des routes pour les rôles
app.include_router(permission_router)  # Inclusion des routes pour les permissions
app.include_router(utilisateur_router)  # Inclusion des routes pour les utilisateurs

# Endpoint racine
@app.get("/", tags=["Root"])
def root():
    logger.info("✅ Endpoint root appelé")
    return {"message": "Bienvenue sur l'API de gestion des clients, organisations et centre d'état civil"}

# Point d'entrée
if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Démarrage du serveur...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
