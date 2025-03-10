from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import init_db 

app = FastAPI(
    title="Gestion des Sessions API",
    description="Une API pour gérer les clients, les sessions et l'authentification OTP",
    version="1.0",
    contact={"name": "Support API", "email": "support@example.com"},
)

# Initialiser la base de données au démarrage
@app.on_event("startup")
def startup():
    init_db()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
def root():
    return {"message": "Bienvenue sur l'API de gestion des clients et des sessions"}
