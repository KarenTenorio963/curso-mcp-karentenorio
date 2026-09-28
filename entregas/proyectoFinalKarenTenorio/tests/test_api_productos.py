import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine_test = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


def test_root_endpoint():
    res = client.get("/")
    assert res.status_code == 200
    assert "Activa" in res.json()["mensaje"]


def test_endpoints_sin_token_devuelven_401():
    # GET /productos/ sin token
    res_get = client.get("/productos/")
    assert res_get.status_code == 401

    # POST /productos/ sin token
    res_post = client.post("/productos/", json={"nombre": "Mouse", "cantidad": 10, "cantidad_minima": 2})
    assert res_post.status_code == 401

    # POST /productos/1/entrada sin token
    res_entrada = client.post("/productos/1/entrada?cantidad=5")
    assert res_entrada.status_code == 401

    # POST /productos/1/salida sin token
    res_salida = client.post("/productos/1/salida?cantidad=3")
    assert res_salida.status_code == 401

    # Token inválido
    res_invalid_token = client.get("/productos/", headers={"Authorization": "Bearer tokeninvalido123"})
    assert res_invalid_token.status_code == 401


def test_registro_y_autenticacion():
    # Registro exitoso
    res_reg = client.post("/usuarios/", json={"email": "nuevo@test.com", "password": "mipassword"})
    assert res_reg.status_code == 201

    # Email duplicado -> 400
    res_dup = client.post("/usuarios/", json={"email": "nuevo@test.com", "password": "mipassword"})
    assert res_dup.status_code == 400

    # Login incorrecto -> 401
    res_login_bad = client.post("/usuarios/token", data={"username": "nuevo@test.com", "password": "wrong"})
    assert res_login_bad.status_code == 401

    # Login correcto -> 200
    res_login_ok = client.post("/usuarios/token", data={"username": "nuevo@test.com", "password": "mipassword"})
    assert res_login_ok.status_code == 200
    assert "access_token" in res_login_ok.json()


def test_flujo_completo_y_stock_minimo_excedido_devuelve_400():
    # 1. Registrar usuario
    res_reg = client.post("/usuarios/", json={"email": "karen@example.com", "password": "password123"})
    assert res_reg.status_code == 201

    # 2. Login y obtener token JWT
    res_login = client.post(
        "/usuarios/token",
        data={"username": "karen@example.com", "password": "password123"}
    )
    token = res_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Crear producto con datos invalidos -> 400
    res_prod_bad = client.post("/productos/", json={"nombre": "  ", "cantidad": 10, "cantidad_minima": 2}, headers=headers)
    assert res_prod_bad.status_code == 400

    # 4. Crear producto válido (stock: 10, cantidad_minima: 3)
    res_prod = client.post(
        "/productos/",
        json={"nombre": "Teclado Mecanico", "cantidad": 10, "cantidad_minima": 3},
        headers=headers
    )
    assert res_prod.status_code == 201
    producto = res_prod.json()
    prod_id = producto["id"]

    # 5. Listar productos
    res_list = client.get("/productos/", headers=headers)
    assert res_list.status_code == 200
    assert len(res_list.json()) == 1

    # 6. Entrada cantidad <= 0 -> 400
    res_ent_bad = client.post(f"/productos/{prod_id}/entrada?cantidad=0", headers=headers)
    assert res_ent_bad.status_code == 400

    # 7. Entrada producto inexistente -> 404
    res_ent_404 = client.post("/productos/999/entrada?cantidad=5", headers=headers)
    assert res_ent_404.status_code == 404

    # 8. Entrada válida (+5 -> 15)
    res_entrada = client.post(f"/productos/{prod_id}/entrada?cantidad=5", headers=headers)
    assert res_entrada.status_code == 200
    assert res_entrada.json()["cantidad"] == 15

    # 9. Salida cantidad <= 0 -> 400
    res_sal_bad = client.post(f"/productos/{prod_id}/salida?cantidad=-1", headers=headers)
    assert res_sal_bad.status_code == 400

    # 10. Salida válida (-10 -> 5, que es >= cantidad_minima 3)
    res_salida = client.post(f"/productos/{prod_id}/salida?cantidad=10", headers=headers)
    assert res_salida.status_code == 200
    assert res_salida.json()["cantidad"] == 5

    # 11. Salida que infringe stock mínimo: actual es 5, minima es 3, intentamos retirar 3 -> 5 - 3 = 2 < 3.
    # Debe retornar HTTP 400 Bad Request
    res_salida_error = client.post(f"/productos/{prod_id}/salida?cantidad=3", headers=headers)
    assert res_salida_error.status_code == 400
    assert "cantidad minima" in res_salida_error.json()["detail"]


def test_aislamiento_entre_usuarios():
    # Crear usuario 1 y su producto
    client.post("/usuarios/", json={"email": "u1@example.com", "password": "pass"})
    t1 = client.post("/usuarios/token", data={"username": "u1@example.com", "password": "pass"}).json()["access_token"]
    h1 = {"Authorization": f"Bearer {t1}"}

    p1 = client.post("/productos/", json={"nombre": "P1", "cantidad": 10, "cantidad_minima": 1}, headers=h1).json()

    # Crear usuario 2
    client.post("/usuarios/", json={"email": "u2@example.com", "password": "pass"})
    t2 = client.post("/usuarios/token", data={"username": "u2@example.com", "password": "pass"}).json()["access_token"]
    h2 = {"Authorization": f"Bearer {t2}"}

    # Usuario 2 no debe ver el producto de Usuario 1
    res_list2 = client.get("/productos/", headers=h2)
    assert res_list2.status_code == 200
    assert len(res_list2.json()) == 0

    # Usuario 2 no debe poder operar salida sobre el producto de Usuario 1 -> 404
    res_salida_u2 = client.post(f"/productos/{p1['id']}/salida?cantidad=1", headers=h2)
    assert res_salida_u2.status_code == 404
