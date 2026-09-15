# from pydantic_settings import BaseSettings


# # class Settings(BaseSettings):
# #     secret_key: str
# #     database_url: str = "sqlite:///./gastos.db"
# #     access_token_expire_minutes: int = 30

# #     class Config:
# #         env_file = ".env"

# class Settings(BaseSettings):
#     secret_key: str
#     database_url: str = "sqlite:///./gastos.db"
#     access_token_expire_minutes: int = 30
#     log_level: str = "INFO"
#     mcp_demo_email: str = "demo@curso.com"
#     mcp_demo_password: str = "demo1234"


# settings = Settings()


from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    secret_key: str
    database_url: str = "sqlite:///./gastos.db"
    access_token_expire_minutes: int = 30
    log_level: str = "INFO"
    mcp_demo_email: str = "demo@curso.com"
    mcp_demo_password: str = "demo1234"
    # En app/config.py dentro de la clase Settings:
    mcp_issuer_url: str = "http://127.0.0.1:8000"
    mcp_resource_url: str = "http://127.0.0.1:8000/mcp"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()