# Tareas de Implementación

- [x] **Tarea 1: Setup y Modelos de Datos**
  - [x] Crear `app/models/producto.py` asegurando los campos `cantidad` y `cantidad_minima`.
  - [x] Generar e instanciar la base de datos vía Alembic.

- [x] **Tarea 2: Repositorios (Acceso a BD)**
  - [x] Implementar `obtener_producto_por_usuario` y `actualizar_stock` en `app/repositories/productos.py`.
  - [x] Validar que no exista lógica de negocio (como ifs validando mínimos) en estos archivos.

- [x] **Tarea 3: Servicios y Pruebas (El Core)**
  - [x] Crear `app/services/inventario.py`.
  - [x] Implementar `registrar_salida(db, usuario_id, producto_id, cantidad_retirada, repo)`.
  - [x] Lanzar `StockMinimoExcedidoError` si el retiro rompe la Regla 1.
  - [x] Escribir tests en `tests/test_inventario_services.py` usando una clase `FakeProductoRepository`.
  - [x] Verificar con `pytest --cov=app.services` que la cobertura sea >= 90%.

- [x] **Tarea 4: API REST y Seguridad**
  - [x] Implementar `POST /productos/{id}/salida` en `routers/productos.py`.
  - [x] Atrapar `StockMinimoExcedidoError` y lanzar `HTTPException(400)`.
  - [x] Verificar que se lance un error 401 si no hay un JWT válido en el header.

- [x] **Tarea 5: Herramientas MCP**
  - [x] Crear `app/mcp/server.py`.
  - [x] Implementar `tool_registrar_salida` que llame a `services.inventario.registrar_salida`.
  - [x] Añadir descripciones claras (docstrings) a cada tool para que el cliente IA entienda las restricciones.
