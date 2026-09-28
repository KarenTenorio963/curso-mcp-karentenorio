# Especificación: Control de Inventario Simple

## 1. Visión General
Sistema backend para gestionar el inventario de productos. Permite llevar el control del stock actual y define un umbral de "cantidad mínima". Si una operación de salida intenta dejar el stock por debajo de este límite, el sistema la rechaza.

## 2. Entidades de Dominio
**Producto**
* `id`: int (Primary Key)
* `usuario_id`: int (Foreign Key, vincula el producto a su dueño)
* `nombre`: str (no vacío)
* `cantidad`: int (stock actual, >= 0)
* `cantidad_minima`: int (umbral de alerta/límite, >= 0)

**Usuario**
* `id`: int (Primary Key)
* `email`: str (único)
* `hashed_password`: str

## 3. Reglas de Negocio (Capa Services)
Estas reglas deben vivir EXCLUSIVAMENTE en `services/inventario.py` y tener sus propios tests unitarios:
* **Regla 1 (Control de Stock Mínimo):** Al registrar una salida de inventario, si `cantidad_actual - cantidad_retirada < cantidad_minima`, la operación se rechaza lanzando la excepción de negocio `StockMinimoExcedidoError`.
* **Regla 2 (Cantidades Válidas):** No se puede crear un producto con cantidades negativas. Las operaciones de entrada/salida deben usar valores estrictamente mayores a cero, de lo contrario lanzan `DatosInvalidosError`.
* **Regla 3 (Aislamiento de Propietario):** Un usuario solo puede operar (ver, modificar stock) sobre los productos donde `usuario_id` coincida con su token JWT. Si intenta operar un producto ajeno, lanza `ProductoNoEncontradoError`.

## 4. API REST (Endpoints)
* `POST /usuarios/` - Registra un nuevo usuario.
* `POST /usuarios/token` - Autenticación y generación de JWT.
* `POST /productos/` - Crea un producto (requiere token).
* `GET /productos/` - Lista los productos del usuario autenticado.
* `POST /productos/{id}/entrada` - Aumenta el stock.
* `POST /productos/{id}/salida` - Disminuye el stock (aplica Regla 1).

## 5. Integración MCP (Tools)
* `tool_registrar_entrada(producto_id: int, cantidad: int, usuario_id: int)`: Reutiliza la lógica de entrada de `services/` y distingue al propietario del producto.
* `tool_registrar_salida(producto_id: int, cantidad: int, usuario_id: int)`: Reutiliza la lógica de salida de `services/`, distingue al propietario del producto y traduce `StockMinimoExcedidoError` a un formato `{"error": "..."}`.