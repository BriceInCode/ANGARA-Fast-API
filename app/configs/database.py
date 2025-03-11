from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.configs import settings

# Adapter l'URL de connexion pour utiliser PyMySQL
DATABASE_URL = settings.DATABASE_URL.replace("mysql://", "mysql+pymysql://")

# Création de l'engine SQLAlchemy
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Création d'une session locale
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles SQLAlchemy
Base = declarative_base()

# Fonction pour récupérer la session de la base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialisation de la base de données (création automatique des tables)
def init_db():
    Base.metadata.create_all(bind=engine)
