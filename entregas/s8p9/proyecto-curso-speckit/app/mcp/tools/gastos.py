from app.services import gastos as gastos_service
from app.database import SessionLocal

def tool_registrar_gasto(descripcion: str, monto: float, categoria: str, usuario_id: int = 1) -> dict:
    db = SessionLocal()
    try:
        resultado = gastos_service.registrar_gasto(
            db=db,
            usuario_id=usuario_id,
            descripcion=descripcion,
            monto=monto,
            categoria=categoria
        )
        return {"status": "exito", "data": resultado}
    except (gastos_service.CategoriaInvalidaError, gastos_service.LimiteExcedidoError, gastos_service.DatosInvalidosError) as e:
        return {"status": "error", "error": str(e)}
    finally:
        db.close()

def tool_listar_gastos(skip: int = 0, limit: int = 20, usuario_id: int = 1) -> dict:
    db = SessionLocal()
    try:
        gastos = gastos_service.listar_gastos(
            db=db,
            usuario_id=usuario_id,
            skip=skip,
            limit=limit
        )
        return {"status": "exito", "data": gastos}
    except gastos_service.DatosInvalidosError as e:
        return {"status": "error", "error": str(e)}
    finally:
        db.close()
