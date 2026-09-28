from mcp.server.fastmcp import FastMCP
from app.mcp.tools.inventario import tool_registrar_salida, tool_registrar_entrada

mcp = FastMCP("Control de Inventario MCP")

@mcp.tool(
    description=(
        "Registra una salida de stock de un producto para el usuario. "
        "Requiere usuario_id para identificar al propietario del producto. "
        "Valida que la cantidad retirada sea mayor a 0 y que el stock resultante "
        "no quede por debajo del umbral de cantidad minima (Regla 1). "
        "Si no cumple, devuelve {'status': 'error', 'error': '...'}"
    )
)
def registrar_salida(producto_id: int, cantidad: int, usuario_id: int) -> dict:
    return tool_registrar_salida(
        producto_id=producto_id,
        cantidad=cantidad,
        usuario_id=usuario_id,
    )


@mcp.tool(
    description=(
        "Registra una entrada de stock aumentando la cantidad disponible de un producto. "
        "Requiere usuario_id para identificar al propietario del producto. "
        "Valida que la cantidad ingresada sea estrictamente mayor a 0. "
        "Devuelve {'status': 'exito', 'data': {...}} o {'status': 'error', 'error': '...'}"
    )
)
def registrar_entrada(producto_id: int, cantidad: int, usuario_id: int) -> dict:
    return tool_registrar_entrada(
        producto_id=producto_id,
        cantidad=cantidad,
        usuario_id=usuario_id,
    )


if __name__ == "__main__":
    mcp.run()
