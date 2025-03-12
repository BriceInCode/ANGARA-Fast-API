from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.configs.database import init_db
from app.routes.clients.client_routes import router as client_router
from app.routes.clients.session_routes import router as session_router
from app.routes.clients.otp_routes import router as otp_router

# Configuration du logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Lifespan pour une meilleure gestion des événements
@asynccontextmanager
async def lifespan(app: FastAPI):
    
    try:
        logger.info("🔄 Initialisation de la base de données...")
        init_db()
        logger.info("✅ Base de données initialisée avec succès")
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'initialisation de la base de données: {e}")
    yield  # D'autres actions peuvent être ajoutées ici

# Création de l'application FastAPI
app = FastAPI(
    title="ANGARA-AUTHENTIC API",
    description="Une API pour générer des documents certifiés",
    version="1.0",
    contact={
        "name": "Support ANGARA-AUTHENTIC",
        "email": "norepleysjm@gmail.com"
    },
    lifespan=lifespan  # Gestion optimisée des événements de démarrage
)

# Configuration CORS (🔒 Sécurisation en ajoutant des domaines spécifiques)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes
app.include_router(client_router)
app.include_router(session_router)
app.include_router(otp_router)

# Endpoint racine
@app.get("/", tags=["Root"])
def root():
    return {"message": "Bienvenue sur l'API de gestion des clients et des sessions"}
