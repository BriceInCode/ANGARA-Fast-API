from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.config.database import Base  # Assurez-vous que 'Base' contient tous vos modèles

# Importation des modèles
from app.client.models.client import Client
from app.client.models.session import Session
from app.client.models.otp import OTP
from app.documents.models.demande import Demande
from app.documents.models.DemandeHistory import DemandeHistory
from app.documents.models.document import Document
from app.utilisateurs.models.organisation import Organisation
from app.utilisateurs.models.utilisateur import Utilisateur
from app.utilisateurs.models.permission import Permission
from app.utilisateurs.models.role import Role
from app.utilisateurs.models.role_permissions import role_permissions
from app.utilisateurs.models.user_permissions import user_permissions

from app.utilisateurs.models.enums import organisation_type
from app.utilisateurs.models.enums import permission_enum
from app.utilisateurs.models.enums import role_enum
from app.documents.models.types.gender import GenderType
from app.documents.models.types.documents import DocumentsType
from app.documents.models.types.raisons import RaisonsType
from app.documents.models.types.status import StatusType


# Object Alembic Config pour accéder aux paramètres du fichier .ini
config = context.config

# Configurer le logger si nécessaire
if config.config_file_name:
    fileConfig(config.config_file_name)

# Utilisation des métadonnées globales de Base
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Exécuter les migrations en mode 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Exécuter les migrations en mode 'online'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

# Déterminer si nous sommes en mode 'offline' ou 'online'
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
