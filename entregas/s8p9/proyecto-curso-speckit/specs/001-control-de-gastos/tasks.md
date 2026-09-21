# Tareas de Implementación — Sistema de Control de Gastos Personales

## Fase 1: Infraestructura y Modelos Base
- [ ] **Tarea 1.1 — Configuración y Base de Datos**: Crear `app/database.py`, `app/config.py` y `.env.example`.
  - *Definition of Done*: Soporta SQLite/Postgres condicionalmente, lee `.env` sin valores por defecto inseguros. Test en `tests/test_infra.py` pasa en verde.
- [ ] **Tarea 1.2 — Modelos ORM y Schemas Pydantic**: Crear `app/models/` (`usuario.py`, `gasto.py`) y `app/schemas/` (`usuario.py`, `gasto.py`).
  - *Definition of Done*: Schemas de entrada/salida separados (`GastoCreate` vs `GastoOut`). FK `usuario_id` explícita[cite: 3]. Test en `tests/test_models.py` pasa en verde.

## Fase 2: Repositorios (Persistencia Pura)
- [ ] **Tarea 2.1 — Repositorio de Usuarios**: Crear `app/repositories/usuarios.py` con funciones `obtener_por_email` y `guardar`[cite: 3].
  - *Definition of Done*: Módulo con funciones (no clases)[cite: 3]. Sin reglas de negocio[cite: 3]. Test en `tests/test_repo_usuarios.py` pasa en verde.
- [ ] **Tarea 2.2 — Repositorio de Gastos**: Crear `app/repositories/gastos.py` con `guardar`, `listar` y `total_por_categoria`[cite: 3].
  - *Definition of Done*: Retorna dicts/modelos sin exponer sesión ORM[cite: 3]. Filtra por `usuario_id` siempre[cite: 3]. Test en `tests/test_repo_gastos.py` pasa en verde.

## Fase 3: Seguridad y Autenticación
- [ ] **Tarea 3.1 — Hashing y Tokens JWT**: Crear `app/core/security.py` y `app/dependencies.py`[cite: 3].
  - *Definition of Done*: Usa `passlib[bcrypt]` y `pyjwt`[cite: 3]. `get_current_user` extrae `usuario_id` del token[cite: 3]. Tests de hash y JWT pasan en verde.

## Fase 4: Capa de Servicios (Lógica de Negocio)
- [ ] **Tarea 4.1 — Servicio de Usuarios**: Crear `app/services/usuarios.py`[cite: 3].
  - *Definition of Done*: Registro y autenticación con hashing. Test unitario con repositorio falso en verde.
- [ ] **Tarea 4.2 — Servicio de Gastos y Reglas de Negocio**: Crear `app/services/gastos.py` con `registrar_gasto` y `listar_gastos`[cite: 3].
  - *Definition of Done*:
    1. Implementa DIP con `repo=gastos_repository` por defecto[cite: 3].
    2. Excepciones `CategoriaInvalidaError` y `LimiteExcedidoError` (`LIMITE_POR_CATEGORIA = 500.0`)[cite: 3].
    3. Cubre Casos de Error 1, 2 y 3 del Spec (monto <= 0, categoría inválida, límite > 500)[cite: 3].
    4. Tests unitarios en `tests/test_gastos_service.py` usando `RepositorioFalso` (sin `unittest.mock`) en verde[cite: 3].

## Fase 5: Routers API REST
- [ ] **Tarea 5.1 — Router de Usuarios**: Crear `app/routers/usuarios.py` (`POST /usuarios/`, `POST /usuarios/token`)[cite: 3].
  - *Definition of Done*: Mapea respuestas a HTTP 201/200 y errores a 400/401/422[cite: 3]. Test de API en verde.
- [ ] **Tarea 5.2 — Router de Gastos y Autorización REST**: Crear `app/routers/gastos.py` (`POST /gastos/`, `GET /gastos/`)[cite: 3].
  - *Definition of Done*:
    1. Obtiene `usuario_id` obligatoriamente de `get_current_user`[cite: 3].
    2. Traduce excepciones de servicio a respuestas HTTP correspondientes[cite: 3].
    3. Cubre Caso de Error 4 (Peticiones sin token devuelven `401`)[cite: 3].
    4. Cubre Caso de Error 5 (Ignora `usuario_id` externo y fuerza aislamiento)[cite: 3].
    5. Tests en `tests/test_api_gastos_extra.py` pasan en verde.

## Fase 6: Servidor e Integración MCP
- [ ] **Tarea 6.1 — Servidor MCP y Tools**: Crear `app/mcp/server.py` y `app/mcp/tools/gastos.py`[cite: 3].
  - *Definition of Done*:
    1. Tools `registrar_gasto` y `listar_gastos` delegan 100% a `services/gastos.py`[cite: 3].
    2. Maneja identidad desde JWT verificado en `streamable-http` o fallback documentado[cite: 3].
    3. Errores se devuelven como `{"error": "..."}`[cite: 3].
    4. Tests de tools en `tests/test_mcp_gastos.py` (caso exitoso y caso de error) en verde[cite: 3].

## Fase 7: Cobertura Global y Compatibilidad
- [ ] **Tarea 7.1 — Verificación Final de Cobertura y Compatibilidad**:
  - *Definition of Done*:
    1. Copiar los tests de S6-S8 (`test_gastos.py`, `test_integracion_gastos.py`, `test_api_gastos.py`) y ejecutar la suite completa sin modificar sus aserciones[cite: 3].
    2. Ejecutar `uv run pytest --cov=app --cov-report=term-missing`[cite: 3].
    3. Confirmar cobertura de `services/` ≥ 90% y conjunto total ≥ 80%[cite: 3].
    4. Confirmar que los 5 casos de error explícitos tienen su test identificable en verde[cite: 3].