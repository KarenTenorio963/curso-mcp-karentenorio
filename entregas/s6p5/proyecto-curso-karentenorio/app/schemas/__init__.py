# Modelos Pydantic de entrada/salida. Se llena en la Sesi�n 7.
#importa los esquemas:
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.schemas.gasto import GastoCreate, GastoResponse

__all__ = ["UsuarioCreate", "UsuarioResponse", "GastoCreate", "GastoResponse"]