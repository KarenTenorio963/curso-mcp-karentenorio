# Especificación 001 — Sistema de Control de Gastos Personales

Sistema de control de gastos personales con interfaz REST y servidor MCP montado sobre la misma backend.

## Entidades
- Usuario: email (único), contraseña (nunca expuesta en respuestas).
- Gasto: descripción, monto (> 0), categoría, pertenece a un usuario.

## Reglas de negocio
- Categorías válidas: comida, transporte, entretenimiento, otros.
  Cualquier otra categoría es un error de negocio, no una excepción genérica.
- El monto de un gasto debe ser mayor a cero; una descripción vacía también
  es inválida.
- Un gasto no puede hacer que el total acumulado de su categoría supere 500.
- Un usuario solo puede ver y crear gastos propios; nunca los de otro usuario,
  sin importar qué identificador se pase en la solicitud.

## Contrato de la API (REST)

| Método | Ruta              | Auth | Request                          | Éxito         | Errores esperados                          |
|--------|-------------------|------|-----------------------------------|---------------|---------------------------------------------|
| POST   | /usuarios/        | No   | email, password                   | 201 Usuario   | 400 email duplicado, 422 validación         |
| POST   | /usuarios/token   | No   | username, password (form)         | 200 token JWT | 401 credenciales inválidas                  |
| POST   | /gastos/          | Sí   | descripcion, monto, categoria     | 201 Gasto     | 400 categoría inválida, 400 límite excedido, 401, 422 |
| GET    | /gastos/          | Sí   | query: skip, limit                | 200 lista     | 401, 422 (skip/limit inválidos)             |

## Contrato equivalente por MCP
- Tool `registrar_gasto(descripcion, monto, categoria)`: mismo comportamiento
  y mismas reglas que POST /gastos/, devolviendo el gasto creado o un error
  de negocio estructurado.
- Tool `listar_gastos(skip=0, limit=20)`: mismo comportamiento que GET /gastos/.
- Ambas tools operan siempre sobre el usuario autenticado de la sesión MCP
  (identidad resuelta desde el token verificado cuando el transporte es
  streamable-http; usuario demo de `.env` solo como fallback documentado
  cuando el transporte es stdio sin identidad propagable), nunca sobre un
  usuario indicado como parámetro.

## Contrato de compatibilidad (no negociable)

Los tests de las Sesiones 6-8 se copian sin modificar. Fijan estas firmas —
sin esta sección, un agente que solo lea las reglas de negocio de arriba
tiene total libertad para inventar otras firmas, y los tres archivos de
tests fallan al importar:

- `app/services/gastos.py`: `CategoriaInvalidaError`, `LimiteExcedidoError`,
  `LIMITE_POR_CATEGORIA = 500.0`,
  `registrar_gasto(db, usuario_id, descripcion, monto, categoria, repo=gastos_repository) -> dict`,
  `listar_gastos(db, usuario_id, skip=0, limit=20, repo=gastos_repository) -> list[dict]`
  — orden posicional exacto, `repo` es keyword con default (DIP).
- `app/repositories/gastos.py` — módulo con funciones, NO clase:
  `guardar(db, usuario_id, descripcion, monto, categoria) -> dict`,
  `listar(db, usuario_id, skip=0, limit=20) -> list[dict]`,
  `total_por_categoria(db, usuario_id, categoria) -> float`. Devuelven
  `dict`, nunca objetos ORM.
- `app/repositories/usuarios.py`: `obtener_por_email(db, email) -> Usuario | None`,
  `guardar(db, email, hashed_password) -> Usuario`.
- `app.database.get_db`, `app.dependencies.get_current_user`,
  `app.dependencies.get_gastos_repo`, `app.models.usuario.Usuario(id=, email=,
  hashed_password=)` — los tests copiados los importan directamente.
- `tests/__init__.py` debe existir: `test_api_gastos.py` hace
  `from tests.test_gastos import RepositorioFalso`.

## Casos de error explícitos que deben tener test
1. Registrar gasto con monto negativo o cero.
2. Registrar gasto con categoría inexistente.
3. Registrar gasto que excede el límite de 500 en su categoría.
4. Listar o registrar gastos sin token → 401.
5. Listar gastos de otro usuario pasando su ID manualmente → debe ignorarse,
   nunca debe filtrar por ese ID.