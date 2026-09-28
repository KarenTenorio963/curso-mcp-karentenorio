from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user, get_productos_repo
from app.schemas.producto import ProductoCreate, ProductoResponse
from app.services import inventario as inventario_service

router = APIRouter(prefix="/productos", tags=["productos"])

@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(
    producto_in: ProductoCreate,
    usuario_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
    repo = Depends(get_productos_repo)
):
    try:
        return inventario_service.crear_producto(
            db=db,
            usuario_id=usuario_id,
            nombre=producto_in.nombre,
            cantidad=producto_in.cantidad,
            cantidad_minima=producto_in.cantidad_minima,
            repo=repo
        )
    except inventario_service.DatosInvalidosError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=list[ProductoResponse])
def listar_productos(
    usuario_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
    repo = Depends(get_productos_repo)
):
    return inventario_service.listar_productos(db=db, usuario_id=usuario_id, repo=repo)

@router.post("/{id}/entrada", response_model=ProductoResponse)
def registrar_entrada(
    id: int,
    cantidad: int,
    usuario_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
    repo = Depends(get_productos_repo)
):
    try:
        return inventario_service.registrar_entrada(
            db=db,
            usuario_id=usuario_id,
            producto_id=id,
            cantidad_ingresada=cantidad,
            repo=repo
        )
    except inventario_service.ProductoNoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except inventario_service.DatosInvalidosError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/{id}/salida", response_model=ProductoResponse)
def registrar_salida(
    id: int,
    cantidad: int,
    usuario_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
    repo = Depends(get_productos_repo)
):
    try:
        return inventario_service.registrar_salida(
            db=db,
            usuario_id=usuario_id,
            producto_id=id,
            cantidad_retirada=cantidad,
            repo=repo
        )
    except inventario_service.StockMinimoExcedidoError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except inventario_service.ProductoNoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except inventario_service.DatosInvalidosError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
