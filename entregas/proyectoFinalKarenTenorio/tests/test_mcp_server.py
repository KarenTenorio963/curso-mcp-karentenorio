import os
import pytest
from app.database import Base, SessionLocal, engine
from app.models.usuario import Usuario
from app.models.producto import Producto
from app.mcp.tools.inventario import tool_registrar_salida, tool_registrar_entrada, get_default_user_id
from app.mcp.server import registrar_salida, registrar_entrada

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    # Asegurar que el usuario_id=1 exista
    u = db.query(Usuario).filter(Usuario.id == 1).first()
    if not u:
        u = Usuario(id=1, email="mcp_user@example.com", hashed_password="hashed_dummy")
        db.add(u)
        db.commit()

    # Asegurar usuario_id=2 para pruebas de env
    u2 = db.query(Usuario).filter(Usuario.id == 2).first()
    if not u2:
        u2 = Usuario(id=2, email="mcp_user2@example.com", hashed_password="hashed_dummy2")
        db.add(u2)
        db.commit()

    # Limpiar productos previos
    db.query(Producto).filter(Producto.usuario_id.in_([1, 2])).delete()
    db.commit()

    # Producto de prueba para user 1: cantidad=20, minima=5
    p1 = Producto(id=100, usuario_id=1, nombre="Item MCP", cantidad=20, cantidad_minima=5)
    # Producto de prueba para user 2: cantidad=50, minima=10
    p2 = Producto(id=1, usuario_id=2, nombre="Avena", cantidad=50, cantidad_minima=10)
    db.add_all([p1, p2])
    db.commit()
    db.close()

    yield

    db = SessionLocal()
    db.query(Producto).filter(Producto.usuario_id.in_([1, 2])).delete()
    db.commit()
    db.close()


def test_tool_registrar_entrada_exito():
    res = tool_registrar_entrada(producto_id=100, cantidad=10, usuario_id=1)
    assert res["status"] == "exito"
    assert res["data"]["cantidad"] == 30


def test_tool_registrar_entrada_cantidad_invalida():
    res = tool_registrar_entrada(producto_id=100, cantidad=0, usuario_id=1)
    assert res["status"] == "error"
    assert "error" in res


def test_tool_registrar_salida_exito():
    # 20 - 10 = 10 (>= 5)
    res = tool_registrar_salida(producto_id=100, cantidad=10, usuario_id=1)
    assert res["status"] == "exito"
    assert res["data"]["cantidad"] == 10


def test_tool_registrar_salida_stock_minimo_excedido():
    # 20 - 18 = 2 (< 5) -> Debe atrapar StockMinimoExcedidoError y devolver formato consistente
    res = tool_registrar_salida(producto_id=100, cantidad=18, usuario_id=1)
    assert res["status"] == "error"
    assert "error" in res
    assert "minima permitida es 5" in res["error"]


def test_tool_registrar_salida_producto_no_encontrado():
    res = tool_registrar_salida(producto_id=9999, cantidad=2, usuario_id=1)
    assert res["status"] == "error"
    assert "no encontrado" in res["error"]


def test_mcp_server_entrypoints():
    # Probar las tools exportadas por el servidor FastMCP usando default user (1 o el que este en .env)
    res_in = registrar_entrada(producto_id=1, cantidad=5, usuario_id=2)
    assert res_in["status"] == "exito"
    assert res_in["data"]["nombre"] == "Avena"
    assert res_in["data"]["usuario_id"] == 2
    assert res_in["data"]["cantidad"] == 55

    res_out = tool_registrar_salida(producto_id=100, cantidad=10, usuario_id=1)
    assert res_out["status"] == "exito"
    assert res_out["data"]["cantidad"] == 10


def test_usuario_id_dinamico_por_variable_entorno(monkeypatch):
    # Configurar variable de entorno MCP_DEFAULT_USER_ID=2
    monkeypatch.setenv("MCP_DEFAULT_USER_ID", "2")
    assert get_default_user_id() == 2

    # Salida ejecutada sin especificar usuario_id: debe operar sobre el producto 1 de user 2
    res = tool_registrar_salida(producto_id=1, cantidad=20)
    assert res["status"] == "exito"
    assert res["data"]["usuario_id"] == 2
    assert res["data"]["cantidad"] == 30

    # Entrada ejecutada sin especificar usuario_id: debe operar sobre el producto 1 de user 2
    res_in = tool_registrar_entrada(producto_id=1, cantidad=10)
    assert res_in["status"] == "exito"
    assert res_in["data"]["usuario_id"] == 2
    assert res_in["data"]["cantidad"] == 40

    # Si la variable de entorno es invalida, debe caer en fallback
    monkeypatch.setenv("MCP_DEFAULT_USER_ID", "invalido")
    assert isinstance(get_default_user_id(), int)
