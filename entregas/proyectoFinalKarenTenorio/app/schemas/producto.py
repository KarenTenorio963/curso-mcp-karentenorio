from pydantic import BaseModel, Field, ConfigDict

class ProductoBase(BaseModel):
    nombre: str
    cantidad: int = Field(ge=0, description="Stock actual mayor o igual a 0")
    cantidad_minima: int = Field(ge=0, description="Umbral minimo mayor o igual a 0")

class ProductoCreate(ProductoBase):
    pass

class ProductoResponse(ProductoBase):
    id: int
    usuario_id: int
    model_config = ConfigDict(from_attributes=True)
