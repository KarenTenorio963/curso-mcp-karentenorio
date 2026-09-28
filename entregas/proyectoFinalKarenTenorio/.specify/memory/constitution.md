
# Constitución del Proyecto: Control de Inventario

## Artículo I. Arquitectura y Responsabilidades (SOLID)
1. El proyecto sigue una arquitectura estricta en capas: `routers/`, `services/`, `repositories/`, `models/`, `schemas/`, y `mcp/`.
2. La lógica de negocio vive EXCLUSIVAMENTE en la capa `services/`. NUNCA en `routers/` ni en `repositories/`.
3. Los repositorios (`repositories/`) se limitan a operaciones de base de datos (persistencia). No validan reglas de negocio.

## Artículo II. Inyección de Dependencias (DIP)
1. Toda función en `services/` que necesite acceso a datos debe recibir el repositorio como parámetro (inyección de dependencias), utilizando un valor por defecto (ej. `repo=productos_repository`).
2. Nunca se debe importar y usar el repositorio directamente dentro de la lógica de la función de servicio sin permitir su inyección por parámetro para facilitar el testing.

## Artículo III. Persistencia y Aislamiento de Datos
1. Se utiliza SQLAlchemy como ORM y Alembic para migraciones.
2. Nunca se devuelve un modelo SQLAlchemy directamente en la respuesta de un endpoint; se debe convertir a un schema Pydantic.
3. Cada modelo con datos de usuario incluye `usuario_id` como clave foránea (FK). Ninguna consulta de datos de `Producto` puede omitir el filtro por `usuario_id` para garantizar el aislamiento total de la información entre usuarios.

## Artículo IV. Seguridad y Autenticación
1. Toda contraseña debe ser hasheada usando bcrypt (vía `passlib`) antes de guardarse en la base de datos.
2. La autenticación se realiza mediante OAuth2 con tokens JWT.
3. Los secretos (como `SECRET_KEY` o `DATABASE_URL`) deben cargarse desde variables de entorno (`.env`) usando `pydantic-settings`. El archivo `.env` real nunca se sube a Git; se debe versionar un archivo `.env.example` como plantilla.
4. El `usuario_id` para operaciones protegidas se extrae SIEMPRE del token JWT (vía dependencia `get_current_user`), nunca se acepta como un parámetro en el payload del cliente. Los endpoints protegidos deben devolver `401 Unauthorized` si no hay token o es inválido.

## Artículo V. API REST y Manejo de Errores
1. Los errores en la capa `services/` deben lanzar excepciones personalizadas del dominio (ej. `StockMinimoExcedidoError`).
2. Los routers deben atrapar estas excepciones y traducirlas al código de estado HTTP correspondiente (ej. 400 Bad Request) usando `HTTPException`.

## Artículo VI. Integración MCP (Model Context Protocol)
1. Cada tool de MCP llama a una función de `services/`, punto. Ejemplo: `ajustar_stock` (tool) y `POST /productos/{id}/ajustar` (router) llaman a la misma función `services/inventario.py::ajustar_stock()`.
2. El manejo de errores en tools de MCP debe ser consistente, devolviendo estructuras claras (ej. `{"error": "..."}`) sin interrumpir la ejecución del servidor.
3. Cualquier tool con efecto destructivo (ej. `eliminar_producto`) debe pedir confirmación explícita gestionada por el servidor, nunca depender de que el modelo decida preguntar por su cuenta.
4. Identidad en MCP: si las tools exponen datos por usuario, se identifica al usuario real extrayéndolo del transporte adecuado. Si por limitaciones del transporte se usa un ID fijo, debe quedar anotado explícitamente en el código. Nunca se deja un usuario fijo sin documentar el motivo.

## Artículo VII. Pruebas (Testing)
1. Se utiliza `pytest` para todas las pruebas.
2. Los tests unitarios de `services/` deben inyectar un repositorio falso (Fake Repository) por parámetro. Está estrictamente prohibido usar `unittest.mock`.
3. Cobertura mínima obligatoria: capa `services/` >= 90%, y un umbral global del proyecto >= 70% medido con `pytest --cov=app --cov-report=term-missing`.
4. Debe haber al menos un test unitario por cada regla de negocio explícita, y al menos 1 test de integración contra base de datos real (ej. SQLite en memoria).