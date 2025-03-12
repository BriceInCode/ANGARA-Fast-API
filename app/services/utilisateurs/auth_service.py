import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.configs.settings import settings
from app.models.utilisateurs.utilisateur import Utilisateur
from app.schemas.utilisateurs.utilisateur_schema import UtilisateurRead

# Paramètres de configuration du JWT depuis settings
SECRET_KEY=settings.SECRET_KEY
ALGORITHM=settings.ALGORITHM
# ACCESS_TOKEN_EXPIRE_MINUTES=settings.ACCESS_TOKEN_EXPIRE_MINUTES
ACCESS_TOKEN_EXPIRE_MINUTES = 120

# Initialisation du contexte de hachage pour les mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Liste noire des tokens, par utilisateur
token_blacklist = {}

# Vérifie si le mot de passe fourni correspond au mot de passe haché
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Crée un token JWT avec une expiration définie
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

class AuthService:
    # Authentifie un utilisateur en vérifiant l'email et le mot de passe
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):
        # Récupérer l'utilisateur par email
        user = db.query(Utilisateur).filter(Utilisateur.email == email).first()
        # Vérification du mot de passe
        if not user or not verify_password(password, user.mot_de_passe):
            return {"code": 401, "message": "Email ou mot de passe invalide", "data": None}
        
        # Génération du token JWT
        access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        
        # Convertir l'utilisateur en un format de lecture (en supposant l'existence de UtilisateurRead)
        user_data = UtilisateurRead.from_orm(user)
        
        # Retourne tout sur une seule ligne
        return {"code": 200, "message": "Authentification réussie", "data": {"access_token": access_token, "token_type": "bearer", "user_info": user_data}}

    # Gère la déconnexion en mettant le token dans une blacklist spécifique à l'utilisateur
    @staticmethod
    def logout_user(user_id: str, token: str):
        # Ajouter le token à la blacklist de l'utilisateur
        if user_id not in token_blacklist:
            token_blacklist[user_id] = set()
        token_blacklist[user_id].add(token)
        return {"code": 200, "message": "Déconnexion réussie", "data": None}
    
    # Vérifie si un token est dans la blacklist de l'utilisateur
    @staticmethod
    def is_token_blacklisted(user_id: str, token: str) -> bool:
        return token in token_blacklist.get(user_id, set())
