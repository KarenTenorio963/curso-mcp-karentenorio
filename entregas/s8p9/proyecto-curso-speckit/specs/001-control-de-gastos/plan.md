# Plan de Implementación — Sistema de Control de Gastos Personales

## Stack Técnico
FastAPI, uvicorn[standard], SQLAlchemy + Alembic, pyjwt, passlib[bcrypt], bcrypt<4.1, pydantic-settings, email-validator, python-multipart, SDK oficial "mcp" montado vía streamable-http, pytest + pytest-cov + httpx.

## Trazabilidad Plan → Constitución
- **Artículo I (Arquitectura en capas):** La separación `routers/services/repositories/utils` se implementa como paquetes Python separados bajo `app/`, sin imports cruzados que violen la dirección de dependencia.
- **Artículo II.3 (SOLID - DIP):** DIP se implementa con parámetros por defecto en las funciones de `services/`, no con un contenedor de inyección de dependencias externo — mantenerlo simple.
- **Artículo IV (Seguridad):** Se implementa con `pyjwt` para JWT (una sola librería, no "pyjwt o python-jose" — dar a elegir reintroduce la ambigüedad que la constitución existe para eliminar; además python-jose está sin mantenimiento), `passlib.context.CryptContext(schemes=["bcrypt"])` para hashing (con `bcrypt<4.1` fijado — passlib 1.7.4 rompe en runtime con versiones más nuevas de bcrypt), y `pydantic_settings.BaseSettings` leyendo `.env` para `SECRET_KEY` y `DATABASE_URL`. `email-validator` y `python-multipart` son dependencias transitivas obligatorias de `pydantic.EmailStr` y `OAuth2PasswordRequestForm` respectivamente — sin ellas la app ni siquiera arranca.
- **Artículo IV.4 (Autorización):** Toda ruta y tool que opera sobre gastos depende de `get_current_user` (o su equivalente MCP) para obtener `usuario_id`; ningún endpoint acepta `usuario_id` como parámetro de entrada.
- **Artículo VII (Testing):** Se implementa con fixtures de pytest para DB en memoria, `app.dependency_overrides` para tests de API (`httpx` como dependencia de `TestClient`), y `pytest-cov` con el umbral del Artículo VII.3 verificado como último paso de `/speckit-implement`, no como una tarea opcional.
- **Artículo VI (MCP):** Se monta dentro de la misma app FastAPI (`streamable-http`), reutilizando `get_current_user` adaptado para extraer el JWT del header Authorization de la sesión MCP.