import pytest
from app.services import inventario as inventario_service
from app.services.inventario import (
    StockMinimoExcedidoError,
    DatosInvalidosError,
    ProductoNoEncontradoError
)

class FakeProducto:
    def __init__(self, id: int, usuario_id: int, nombre: str, cantidad: int, cantidad_minima: int):
        self.id = id
        self.usuario_id = usuario_id
        self.nombre = nombre
        self.cantidad = cantidad
        self.cantidad_minima = cantidad_minima

class FakeProductoRepository:
    """Test double que implementa el contrato de acceso a datos sin persistencia real en BD."""

    def __init__(self):
        self._productos: dict[tuple[int, int], FakeProducto] = {}
        self._next_id = 1

    def obtener_producto_por_usuario(self, db, usuario_id: int, producto_id: int):
        return self._productos.get((usuario_id, producto_id))

    def actualizar_stock(self, db, producto: FakeProducto, nueva_cantidad: int):
        producto.cantidad = nueva_cantidad
        return producto

    def guardar(self, db, usuario_id: int, nombre: str, cantidad: int, cantidad_minima: int):
        prod = FakeProducto(
            id=self._next_id,
            usuario_id=usuario_id,
            nombre=nombre,
            cantidad=cantidad,
            cantidad_minima=cantidad_minima
        )
        self._productos[(usuario_id, prod.id)] = prod
        self._next_id += 1
        return prod

    def listar_por_usuario(self, db, usuario_id: int):
        return [p for (uid, _), p in self._productos.items() if uid == usuario_id]


# --- Pruebas de registrar_salida (Regla 1, Regla 2, Regla 3) ---

def test_registrar_salida_exitosa():
    repo = FakeProductoRepository()
    prod = repo.guardar(db=None, usuario_id=1, nombre="Monitor", cantidad=10, cantidad_minima=2)

    resultado = inventario_service.registrar_salida(
        db=None, usuario_id=1, producto_id=prod.id, cantidad_retirada=5, repo=repo
    )

    assert resultado.cantidad == 5


def test_registrar_salida_hasta_limite_exacto():
    repo = FakeProductoRepository()
    prod = repo.guardar(db=None, usuario_id=1, nombre="Teclado", cantidad=10, cantidad_minima=2)

    # Puede llegar exactamente al limite minimo
    resultado = inventario_service.registrar_salida(
        db=None, usuario_id=1, producto_id=prod.id, cantidad_retirada=8, repo=repo
    )

    assert resultado.cantidad == 2


def test_registrar_salida_excede_stock_minimo_lanza_error():
    repo = FakeProductoRepository()
    prod = repo.guardar(db=None, usuario_id=1, nombre="Mouse", cantidad=10, cantidad_minima=3)

    # 10 - 8 = 2 < 3 -> StockMinimoExcedidoError
    with pytest.raises(StockMinimoExcedidoError):
        inventario_service.registrar_salida(
            db=None, usuario_id=1, producto_id=prod.id, cantidad_retirada=8, repo=repo
        )


def test_registrar_salida_cantidad_cero_o_negativa_lanza_datos_invalidos():
    repo = FakeProductoRepository()
    prod = repo.guardar(db=None, usuario_id=1, nombre="Mouse", cantidad=10, cantidad_minima=3)

    with pytest.raises(DatosInvalidosError):
        inventario_service.registrar_salida(
            db=None, usuario_id=1, producto_id=prod.id, cantidad_retirada=0, repo=repo
        )

    with pytest.raises(DatosInvalidosError):
        inventario_service.registrar_salida(
            db=None, usuario_id=1, producto_id=prod.id, cantidad_retirada=-5, repo=repo
        )


def test_registrar_salida_producto_inexistente_o_ajeno_lanza_error():
    repo = FakeProductoRepository()
    prod = repo.guardar(db=None, usuario_id=1, nombre="Mouse", cantidad=10, cantidad_minima=3)

    # Producto de otro usuario (usuario_id=2 no es dueno de prod.id)
    with pytest.raises(ProductoNoEncontradoError):
        inventario_service.registrar_salida(
            db=None, usuario_id=2, producto_id=prod.id, cantidad_retirada=2, repo=repo
        )

    # Producto inexistente
    with pytest.raises(ProductoNoEncontradoError):
        inventario_service.registrar_salida(
            db=None, usuario_id=1, producto_id=999, cantidad_retirada=2, repo=repo
        )


# --- Pruebas de registrar_entrada ---

def test_registrar_entrada_exitosa():
    repo = FakeProductoRepository()
    prod = repo.guardar(db=None, usuario_id=1, nombre="Headset", cantidad=5, cantidad_minima=1)

    resultado = inventario_service.registrar_entrada(
        db=None, usuario_id=1, producto_id=prod.id, cantidad_ingresada=10, repo=repo
    )

    assert resultado.cantidad == 15


def test_registrar_entrada_cantidad_invalida_lanza_error():
    repo = FakeProductoRepository()
    prod = repo.guardar(db=None, usuario_id=1, nombre="Headset", cantidad=5, cantidad_minima=1)

    with pytest.raises(DatosInvalidosError):
        inventario_service.registrar_entrada(
            db=None, usuario_id=1, producto_id=prod.id, cantidad_ingresada=0, repo=repo
        )

    with pytest.raises(DatosInvalidosError):
        inventario_service.registrar_entrada(
            db=None, usuario_id=1, producto_id=prod.id, cantidad_ingresada=-3, repo=repo
        )


def test_registrar_entrada_producto_no_encontrado_lanza_error():
    repo = FakeProductoRepository()
    with pytest.raises(ProductoNoEncontradoError):
        inventario_service.registrar_entrada(
            db=None, usuario_id=1, producto_id=999, cantidad_ingresada=5, repo=repo
        )


# --- Pruebas de crear_producto, listar y obtener ---

def test_crear_producto_exitoso():
    repo = FakeProductoRepository()
    prod = inventario_service.crear_producto(
        db=None, usuario_id=1, nombre="Laptop Gamer", cantidad=20, cantidad_minima=5, repo=repo
    )

    assert prod.id == 1
    assert prod.nombre == "Laptop Gamer"
    assert prod.cantidad == 20
    assert prod.cantidad_minima == 5


def test_crear_producto_validaciones_invalidas():
    repo = FakeProductoRepository()

    # Nombre vacio
    with pytest.raises(DatosInvalidosError):
        inventario_service.crear_producto(
            db=None, usuario_id=1, nombre="   ", cantidad=10, cantidad_minima=2, repo=repo
        )

    # Cantidad negativa
    with pytest.raises(DatosInvalidosError):
        inventario_service.crear_producto(
            db=None, usuario_id=1, nombre="Laptop", cantidad=-1, cantidad_minima=2, repo=repo
        )

    # Cantidad minima negativa
    with pytest.raises(DatosInvalidosError):
        inventario_service.crear_producto(
            db=None, usuario_id=1, nombre="Laptop", cantidad=10, cantidad_minima=-2, repo=repo
        )


def test_listar_y_obtener_producto():
    repo = FakeProductoRepository()
    p1 = inventario_service.crear_producto(db=None, usuario_id=1, nombre="P1", cantidad=5, cantidad_minima=1, repo=repo)
    p2 = inventario_service.crear_producto(db=None, usuario_id=1, nombre="P2", cantidad=8, cantidad_minima=2, repo=repo)
    inventario_service.crear_producto(db=None, usuario_id=2, nombre="P3", cantidad=15, cantidad_minima=3, repo=repo)

    lista_u1 = inventario_service.listar_productos(db=None, usuario_id=1, repo=repo)
    assert len(lista_u1) == 2

    prod_obtenido = inventario_service.obtener_producto(db=None, usuario_id=1, producto_id=p1.id, repo=repo)
    assert prod_obtenido.nombre == "P1"

    with pytest.raises(ProductoNoEncontradoError):
        inventario_service.obtener_producto(db=None, usuario_id=1, producto_id=999, repo=repo)
