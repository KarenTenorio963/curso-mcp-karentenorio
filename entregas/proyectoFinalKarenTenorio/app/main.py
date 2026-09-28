from fastapi import FastAPI
from app.routers import usuarios, productos

app = FastAPI(title="Control de Inventario API")

app.include_router(usuarios.router)
app.include_router(productos.router)

@app.get("/")
def root():
    return {"mensaje": "API de Control de Inventario Activa"}
