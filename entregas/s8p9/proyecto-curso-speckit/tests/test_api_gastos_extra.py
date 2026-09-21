import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, get_db
from sqlalchemy.orm import sessionmaker

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_caso_4_sin_token_devuelve_401():
    response = client.get("/gastos/")
    assert response.status_code == 401

    response_post = client.post("/gastos/", json={"descripcion": "Taxi", "monto": 10.0, "categoria": "transporte"})
    assert response_post.status_code == 401

def test_caso_5_usuario_id_ajeno_es_ignorado():
    client.post("/usuarios/", json={"email": "usuario1@test.com", "password": "password123"})
    login_res = client.post("/usuarios/token", data={"username": "usuario1@test.com", "password": "password123"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get("/gastos/?usuario_id=999", headers=headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)
