from sqlalchemy.orm import Session
from app.repositories import gastos as gastos_repository

CATEGORIAS_VALIDAS = {"comida", "transporte", "entretenimiento", "otros"}
LIMITE_POR_CATEGORIA = 500.0

class CategoriaInvalidaError(Exception):
    pass

class LimiteExcedidoError(Exception):
    pass

class DatosInvalidosError(ValueError):
    pass

def registrar_gasto(db: Session, usuario_id: int, descripcion: str, monto: float, categoria: str, repo=gastos_repository) -> dict:
    if not descripcion or not descripcion.strip():
        raise DatosInvalidosError("La descripción no puede estar vacía")
    
    if monto <= 0:
        raise DatosInvalidosError("El monto debe ser mayor a cero")
    
    if categoria not in CATEGORIAS_VALIDAS:
        raise CategoriaInvalidaError(f"Categoría inválida: {categoria}")
    
    total_actual = repo.total_por_categoria(db, usuario_id, categoria)
    if total_actual + monto > LIMITE_POR_CATEGORIA:
        raise LimiteExcedidoError("El gasto excede el límite permitido para esta categoría")
    
    return repo.guardar(db, usuario_id, descripcion.strip(), monto, categoria)

def listar_gastos(db: Session, usuario_id: int, skip: int = 0, limit: int = 20, repo=gastos_repository) -> list[dict]:
    if skip < 0 or limit <= 0:
        raise DatosInvalidosError("Parámetros de paginación inválidos")
    return repo.listar(db, usuario_id, skip=skip, limit=limit)
