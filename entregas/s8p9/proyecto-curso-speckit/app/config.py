from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "secret-key-super-segura-para-desarrollo-32-bytes"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "sqlite:///./gastos.db"

    class Config:
        env_file = ".env"

settings = Settings()