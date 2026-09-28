from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import app.models.usuario  # Asegura que el mapper de Usuario este registrado en SQLAlchemy

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    nombre = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False, default=0)
    cantidad_minima = Column(Integer, nullable=False, default=0)

    usuario = relationship("Usuario", back_populates="productos")
