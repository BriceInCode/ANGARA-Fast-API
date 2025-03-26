from datetime import datetime, timedelta
from sqlalchemy import Column, DateTime, Boolean, String, func, Enum as SQLAlchemyEnum

from app.configs.enumerations.Sexe import SexeEnum

def default_expires_at(delta: timedelta):
    """
    Retourne une fonction calculant la date d'expiration en ajoutant le delta spécifié à l'heure actuelle.
    """
    return lambda: datetime.utcnow() + delta

class TimestampMixin:
    """Mixin pour historiser la création et la modification des enregistrements."""
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

class SoftDeleteMixin:
    """Mixin pour activer la suppression douce (soft delete)."""
    is_active = Column(Boolean, default=True, nullable=False)

class ExpiresAtMixin:
    """
    Mixin générique pour ajouter un champ expires_at.
    La valeur par défaut est à définir via la fonction `default_expires_at`.
    """
    # Ce champ doit être défini dans les sous-classes
    expires_at = None

class SoftExpiredMixin(ExpiresAtMixin):
    """
    Mixin qui ajoute un champ expires_at avec un délai de 2 heures.
    Utile pour des enregistrements dont l'expiration doit être programmée dans 2 heures.
    """
    expires_at = Column(DateTime, default=default_expires_at(timedelta(hours=2)), index=True)

class SoftSessionExpiredMixin(ExpiresAtMixin):
    """
    Mixin qui ajoute un champ expires_at avec un délai de 1 heure et 10 minutes.
    Par exemple, pour des sessions dont l'expiration se calcule différemment.
    """
    expires_at = Column(DateTime, default=default_expires_at(timedelta(hours=1, minutes=10)), index=True)


# Mixin pour les informations personnelles communes aux actes de naissance et de décès
class PersonMixin:
    """
    Mixin regroupant les informations d'identité communes pour un individu.
    
    Ce mixin est utilisé pour éviter la redondance des champs nom, prénom, sexe, date et lieu de naissance 
    dans les demandes d'acte de naissance et d'acte de décès.
    """
    nom = Column(String(255), nullable=False)
    prenom = Column(String(255), nullable=False)
    sexe = Column(SQLAlchemyEnum(SexeEnum), nullable=False)
    date_naissance = Column(DateTime, nullable=False)
    lieu_naissance = Column(String(255), nullable=False)