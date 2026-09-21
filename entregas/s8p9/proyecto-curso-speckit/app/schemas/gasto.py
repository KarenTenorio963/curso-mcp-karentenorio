from pydantic import BaseModel

class GastoCreate(BaseModel):
    descripcion: str
    monto: float
    categoria: str

class GastoOut(BaseModel):
    id: int
    descripcion: str
    monto: float
    categoria: str
    usuario_id: int

    class Config:
        from_attributes = True
