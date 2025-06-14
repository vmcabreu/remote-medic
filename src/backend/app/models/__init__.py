from app.extensions import db

# Importa todos los modelos aquí para que queden registrados
from .user import User
from .patients import Patient

# Opcional: exporta en __all__ para importaciones limpias
__all__ = [
    "User",
    "Patient"
]