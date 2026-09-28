from sqlalchemy.orm import Session
from app.repositories import productos as productos_repository
from app.models.producto import Producto

class StockMinimoExcedidoError(Exception):
    """Lanzada cuando una salida de stock deja la cantidad por debajo de cantidad_minima."""
    pass

class DatosInvalidosError(ValueError):
    """Lanzada cuando los datos de entrada o cantidades son inválidos (<= 0 o vacíos)."""
    pass

class ProductoNoEncontradoError(Exception):
    """Lanzada cuando el producto no existe o pertenece a otro usuario."""
    pass

def registrar_salida(
    db: Session,
    usuario_id: int,
    producto_id: int,
    cantidad_retirada: int,
    repo=productos_repository
) -> Producto:
    """
    Registra la salida de inventario verificando Regla 1, Regla 2 y Regla 3.
    Regla 1: cantidad_actual - cantidad_retirada >= cantidad_minima
    Regla 2: cantidad_retirada > 0
    Regla 3: Aislamiento de propietario por usuario_id
    """
    if cantidad_retirada <= 0:
        raise DatosInvalidosError("La cantidad retirada debe ser estrictamente mayor a cero")

    producto = repo.obtener_producto_por_usuario(db, usuario_id, producto_id)
    if producto is None:
        raise ProductoNoEncontradoError(f"Producto con id {producto_id} no encontrado para el usuario")

    nuevo_stock = producto.cantidad - cantidad_retirada
    if nuevo_stock < producto.cantidad_minima:
        raise StockMinimoExcedidoError(
            f"No se puede retirar {cantidad_retirada} unidades. "
            f"El stock actual es {producto.cantidad} y la cantidad minima permitida es {producto.cantidad_minima}"
        )

    return repo.actualizar_stock(db, producto, nuevo_stock)

def registrar_entrada(
    db: Session,
    usuario_id: int,
    producto_id: int,
    cantidad_ingresada: int,
    repo=productos_repository
) -> Producto:
    """
    Registra el ingreso de inventario cumpliendo Regla 2 y Regla 3.
    """
    if cantidad_ingresada <= 0:
        raise DatosInvalidosError("La cantidad ingresada debe ser estrictamente mayor a cero")

    producto = repo.obtener_producto_por_usuario(db, usuario_id, producto_id)
    if producto is None:
        raise ProductoNoEncontradoError(f"Producto con id {producto_id} no encontrado para el usuario")

    nuevo_stock = producto.cantidad + cantidad_ingresada
    return repo.actualizar_stock(db, producto, nuevo_stock)

def crear_producto(
    db: Session,
    usuario_id: int,
    nombre: str,
    cantidad: int,
    cantidad_minima: int,
    repo=productos_repository
) -> Producto:
    """
    Crea un nuevo producto validando nombre y cantidades no negativas.
    """
    if not nombre or not nombre.strip():
        raise DatosInvalidosError("El nombre del producto no puede estar vacio")

    if cantidad < 0 or cantidad_minima < 0:
        raise DatosInvalidosError("Las cantidades no pueden ser negativas")

    return repo.guardar(
        db,
        usuario_id=usuario_id,
        nombre=nombre.strip(),
        cantidad=cantidad,
        cantidad_minima=cantidad_minima
    )

def listar_productos(
    db: Session,
    usuario_id: int,
    repo=productos_repository
) -> list[Producto]:
    """
    Lista los productos del usuario garantizando aislamiento.
    """
    return repo.listar_por_usuario(db, usuario_id)

def obtener_producto(
    db: Session,
    usuario_id: int,
    producto_id: int,
    repo=productos_repository
) -> Producto:
    """
    Obtiene un producto verificando propiedad.
    """
    producto = repo.obtener_producto_por_usuario(db, usuario_id, producto_id)
    if producto is None:
        raise ProductoNoEncontradoError(f"Producto con id {producto_id} no encontrado para el usuario")
    return producto

