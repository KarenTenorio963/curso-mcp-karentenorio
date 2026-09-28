import os
from dotenv import load_dotenv
from app.services import inventario as inventario_service
from app.database import SessionLocal
from app.config import settings

def get_default_user_id() -> int:
    """
    Obtiene dinamicamente en tiempo de ejecucion el usuario_id por defecto.
    Recarga el archivo .env para reflejar cualquier actualizacion y busca MCP_DEFAULT_USER_ID,
    con fallback al valor en settings o 1.
    """
    load_dotenv(override=True)
    env_val = os.getenv("MCP_DEFAULT_USER_ID")
    if env_val:
        try:
            return int(env_val)
        except ValueError:
            pass
    return getattr(settings, "MCP_DEFAULT_USER_ID", 2)


def tool_registrar_salida(producto_id: int, cantidad: int, usuario_id: int | None = None) -> dict:
    """
    Registra una salida de stock de un producto verificando la regla de stock minimo.
    Si usuario_id es None, invoca get_default_user_id() en tiempo de ejecucion.
    Captura excepciones de negocio y devuelve formato estructurado.
    """
    if usuario_id is None:
        usuario_id = get_default_user_id()

    db = SessionLocal()
    try:
        resultado = inventario_service.registrar_salida(
            db=db,
            usuario_id=usuario_id,
            producto_id=producto_id,
            cantidad_retirada=cantidad
        )
        return {
            "status": "exito",
            "data": {
                "id": resultado.id,
                "nombre": resultado.nombre,
                "cantidad": resultado.cantidad,
                "cantidad_minima": resultado.cantidad_minima,
                "usuario_id": resultado.usuario_id
            }
        }
    except (
        inventario_service.StockMinimoExcedidoError,
        inventario_service.ProductoNoEncontradoError,
        inventario_service.DatosInvalidosError
    ) as e:
        return {"status": "error", "error": str(e)}
    finally:
        db.close()


def tool_registrar_entrada(producto_id: int, cantidad: int, usuario_id: int | None = None) -> dict:
    """
    Registra una entrada de stock de un producto para el usuario.
    Si usuario_id es None, invoca get_default_user_id() en tiempo de ejecucion.
    Captura excepciones de negocio y devuelve formato estructurado.
    """
    if usuario_id is None:
        usuario_id = get_default_user_id()

    db = SessionLocal()
    try:
        resultado = inventario_service.registrar_entrada(
            db=db,
            usuario_id=usuario_id,
            producto_id=producto_id,
            cantidad_ingresada=cantidad
        )
        return {
            "status": "exito",
            "data": {
                "id": resultado.id,
                "nombre": resultado.nombre,
                "cantidad": resultado.cantidad,
                "cantidad_minima": resultado.cantidad_minima,
                "usuario_id": resultado.usuario_id
            }
        }
    except (
        inventario_service.ProductoNoEncontradoError,
        inventario_service.DatosInvalidosError
    ) as e:
        return {"status": "error", "error": str(e)}
    finally:
        db.close()
