from fastapi import FastAPI
from app.database import engine, Base
from app.routers import usuarios, gastos

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Control de Gastos API")

app.include_router(usuarios.router)
app.include_router(gastos.router)

@app.get("/")
def root():
    return {"mensaje": "API de Control de Gastos Activa"}
