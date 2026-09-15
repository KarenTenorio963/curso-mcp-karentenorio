# # from app.services import gastos as gastos_service
# # from app.utils.formato import formatear_moneda

# # if __name__ == "__main__":
# #     gastos_service.registrar_gasto("Almuerzo", 12.50, "comida")
# #     gastos_service.registrar_gasto("Bus", 2.00, "transporte")

# #     for gasto in gastos_service.listar_gastos():
# #         print(f"{gasto['descripcion']}: {formatear_moneda(gasto['monto'])} ({gasto['categoria']})")

# # actualizaciòn de la sesiòn 7, se agregan los endpoints REST para usuarios y gastos

# from fastapi import FastAPI
# from app.routers import usuarios, gastos

# app = FastAPI(title="API de Control de Gastos")
# app.include_router(usuarios.router)
# app.include_router(gastos.router)


# import logging
# import time
# from contextlib import asynccontextmanager

# from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse

# from app.config import settings
# from app.logging_config import configurar_logging
# from app.routers import usuarios, gastos
# from app.mcp.server import mcp as mcp_server

# configurar_logging(settings.log_level)
# logger = logging.getLogger(__name__)

# # Streamable-HTTP: el mismo servidor MCP servido como sub-app ASGI montable en FastAPI.
# mcp_app = mcp_server.streamable_http_app()


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Arranca el session manager de streamable-http de MCP para que acepte conexiones en /mcp
#     async with mcp_server.session_manager.run():
#         yield


# app = FastAPI(title="API de Control de Gastos", lifespan=lifespan)
# app.include_router(usuarios.router)
# app.include_router(gastos.router)
# app.mount("/mcp", mcp_app)


# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     inicio = time.perf_counter()
#     response = await call_next(request)
#     duracion_ms = (time.perf_counter() - inicio) * 1000
#     logger.info(
#         "%s %s -> %d (%.1f ms)",
#         request.method,
#         request.url.path,
#         response.status_code,
#         duracion_ms,
#     )
#     return response


# @app.exception_handler(Exception)
# async def manejar_error_no_controlado(request: Request, exc: Exception):
#     logger.exception("Error no controlado en %s %s", request.method, request.url.path)
#     return JSONResponse(status_code=500, content={"detail": "Error interno del servidor"})



import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import settings
from app.routers import usuarios, gastos
from app.mcp.server import mcp as mcp_server

# Configuración estándar de logging sin dependencia de app.logging_config
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

# Streamable-HTTP: el servidor MCP servido como sub-app ASGI montable en FastAPI
mcp_app = mcp_server.streamable_http_app()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Arranca el session manager de streamable-http de MCP para aceptar conexiones en /mcp
    async with mcp_server.session_manager.run():
        yield


app = FastAPI(title="API de Control de Gastos", lifespan=lifespan)
app.include_router(usuarios.router)
app.include_router(gastos.router)
app.mount("/mcp", mcp_app)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    inicio = time.perf_counter()
    response = await call_next(request)
    duracion_ms = (time.perf_counter() - inicio) * 1000
    logger.info(
        "%s %s -> %d (%.1f ms)",
        request.method,
        request.url.path,
        response.status_code,
        duracion_ms,
    )
    return response


@app.exception_handler(Exception)
async def manejar_error_no_controlado(request: Request, exc: Exception):
    logger.exception("Error no controlado en %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Error interno del servidor"})