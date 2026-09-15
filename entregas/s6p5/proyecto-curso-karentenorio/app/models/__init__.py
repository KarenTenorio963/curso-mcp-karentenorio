# Tablas SQLAlchemy (Usuario, Gasto). Se llena en la Sesi�n 7.
# importa ambos modelos para que SQLAlchemy y Alembic los detecten fácilmente
from app.models.usuario import Usuario
from app.models.gasto import Gasto

__all__ = ["Usuario", "Gasto"]