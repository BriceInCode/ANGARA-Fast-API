from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.client.routes.routes import router 
from app.config.database import init_db

app = FastAPI(
    title="ANGARA-AUTHENTIC API",
    description="Une API pour générer des documents certifiés",
    version="1.0",
    contact={"name": "Support API", "email": "support@example.com"},
)

# Initialiser la base de données au démarrage
@app.on_event("startup")
def startup():
    try:
        init_db()  # ✅ Ne PAS mettre await ici si init_db() n'est pas async
        print("✅ Base de données initialisée avec succès")
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation de la base de données: {e}")


# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ajouter les routes principales
app.include_router(router)

@app.get("/", tags=["Root"])
def root():
    return {"message": "Bienvenue sur l'API de gestion des clients et des sessions"}

