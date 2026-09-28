# Plan de Ejecución: Control de Inventario

## Fase 1: Core de Datos y Persistencia
* **Objetivo:** Definir los modelos SQLAlchemy, esquemas Pydantic y la capa de acceso a datos.
* **Pasos:**
  1. Crear `app/models/usuario.py` y `app/models/producto.py` (con `usuario_id` como FK).
  2. Crear `app/schemas/usuario.py` y `app/schemas/producto.py`.
  3. Crear `app/repositories/usuarios.py` y `app/repositories/productos.py`.
* **Análisis de Diseño:** ¿Se viola el DIP o la separación de capas? No. Los repositorios se limitarán estrictamente a operaciones CRUD en la base de datos sin aplicar validaciones de stock.

## Fase 2: Lógica de Negocio y Reglas Estrictas (Capa Services)
* **Objetivo:** Implementar las reglas del dominio con inyección de dependencias y verificar con tests unitarios.
* **Pasos:**
  1. Implementar `app/services/inventario.py` inyectando `repo` como parámetro.
  2. Programar Regla 1 (Stock mínimo al retirar) y Regla 2 (Validación de enteros positivos).
  3. Crear `tests/test_inventario_services.py` inyectando un `FakeRepository` (prohibido `unittest.mock`).
* **Análisis de Diseño:** Al inyectar un repositorio falso en memoria, los tests unitarios correrán extremadamente rápido y aislarán la verificación matemática del stock mínimo.

## Fase 3: API REST y Seguridad JWT
* **Objetivo:** Exponer la lógica de negocio a través de HTTP protegiendo las rutas.
* **Pasos:**
  1. Implementar `app/routers/usuarios.py` para login y generación de JWT.
  2. Implementar `app/routers/productos.py` asegurando que todos los endpoints inyecten `Depends(get_current_user)`.
  3. Escribir tests de integración para comprobar que peticiones sin token devuelvan `401 Unauthorized`.

## Fase 4: Integración MCP
* **Objetivo:** Exponer las capacidades del inventario a clientes MCP reutilizando el código existente.
* **Pasos:**
  1. Crear `app/mcp/server.py` utilizando FastMCP.
  2. Exponer `tool_registrar_entrada` y `tool_registrar_salida` vinculándolas directamente a `services/inventario.py`.
  3. Manejar las excepciones del dominio (`StockMinimoExcedidoError`) para que devuelvan JSON formatteado (`{"error": "..."}`) sin interrumpir la sesión MCP.