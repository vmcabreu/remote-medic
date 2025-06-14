from app.extensions import db

# Importa todos los modelos aquí para que queden registrados
from .user import User

# Opcional: exporta en __all__ para importaciones limpias
__all__ = [
    "User",
]