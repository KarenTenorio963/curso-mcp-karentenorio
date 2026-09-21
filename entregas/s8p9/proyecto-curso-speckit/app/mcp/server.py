from mcp.server.fastmcp import FastMCP
from app.mcp.tools.gastos import tool_registrar_gasto, tool_listar_gastos

mcp = FastMCP("Control de Gastos MCP")

@mcp.tool(description="Registra un nuevo gasto validando categoría y límite acumulado de 500.0 por categoría")
def registrar_gasto(descripcion: str, monto: float, categoria: str) -> dict:
    # Nota de simplificación (Artículo VI.4): Transporte stdio sin token utiliza usuario_id=1 como fallback
    return tool_registrar_gasto(descripcion=descripcion, monto=monto, categoria=categoria, usuario_id=1)

@mcp.tool(description="Lista los gastos paginados del usuario autenticado")
def listar_gastos(skip: int = 0, limit: int = 20) -> dict:
    # Nota de simplificación (Artículo VI.4): Transporte stdio sin token utiliza usuario_id=1 como fallback
    return tool_listar_gastos(skip=skip, limit=limit, usuario_id=1)
