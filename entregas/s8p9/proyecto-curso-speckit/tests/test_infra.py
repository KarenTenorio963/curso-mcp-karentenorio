from app.config import settings
from app.database import engine

def test_config_cargada():
    assert settings.SECRET_KEY is not None
    assert settings.ALGORITHM == "HS256"

def test_database_connection():
    assert engine is not None