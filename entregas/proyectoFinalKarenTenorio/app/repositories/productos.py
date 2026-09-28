from sqlalchemy.orm import Session
from app.models.producto import Producto

def obtener_producto_por_usuario(db: Session, usuario_id: int, producto_id: int) -> Producto | None:
    return db.query(Producto).filter(
        Producto.id == producto_id,
        Producto.usuario_id == usuario_id
    ).first()

def actualizar_stock(db: Session, producto: Producto, nueva_cantidad: int) -> Producto:
    producto.cantidad = nueva_cantidad
    db.commit()
    db.refresh(producto)
    return producto

def guardar(db: Session, usuario_id: int, nombre: str, cantidad: int, cantidad_minima: int) -> Producto:
    producto = Producto(
        usuario_id=usuario_id,
        nombre=nombre,
        cantidad=cantidad,
        cantidad_minima=cantidad_minima
    )
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto

def listar_por_usuario(db: Session, usuario_id: int) -> list[Producto]:
    return db.query(Producto).filter(Producto.usuario_id == usuario_id).all()
