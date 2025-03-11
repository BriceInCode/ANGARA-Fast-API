from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.client.routes.routes import router as client_router
from app.documents.routes.routes import router as documents_router
from app.config.database import init_db
import logging

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ANGARA-AUTHENTIC API",
    description="Une API pour générer des documents certifiés",
    version="1.0",
    contact={"name": "Support ANGARA-AUTHENTIC", "email": "norepleysjm@gmail.com"},
)

# ✅ Initialiser la base de données au démarrage
@app.on_event("startup")
def startup():
    try:
        init_db()  # ✅ Ne PAS mettre await ici si init_db() n'est pas async
        logger.info("✅ Base de données initialisée avec succès")
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'initialisation de la base de données: {e}")

# 🚀 Configuration CORS (⚠️ À restreindre en production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ En prod, utiliser un domaine spécifique : ["https://mon-site.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📌 Ajouter les routes principales
app.include_router(client_router)
app.include_router(documents_router)

# 🌍 Route racine
@app.get("/", tags=["Root"])
def root():
    return {"message": "Bienvenue sur l'API de gestion des clients et des sessions"}
