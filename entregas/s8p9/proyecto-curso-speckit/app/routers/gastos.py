from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user, get_gastos_repo
from app.schemas.gasto import GastoCreate, GastoOut
from app.services import gastos as gastos_service

router = APIRouter(prefix="/gastos", tags=["gastos"])

@router.post("/", response_model=GastoOut, status_code=status.HTTP_201_CREATED)
def crear_gasto(
    gasto_in: GastoCreate,
    usuario_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
    repo = Depends(get_gastos_repo)
):
    try:
        return gastos_service.registrar_gasto(
            db=db,
            usuario_id=usuario_id,
            descripcion=gasto_in.descripcion,
            monto=gasto_in.monto,
            categoria=gasto_in.categoria,
            repo=repo
        )
    except (gastos_service.CategoriaInvalidaError, gastos_service.LimiteExcedidoError, gastos_service.DatosInvalidosError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=list[GastoOut])
def obtener_gastos(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, gt=0),
    usuario_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
    repo = Depends(get_gastos_repo)
):
    try:
        return gastos_service.listar_gastos(db=db, usuario_id=usuario_id, skip=skip, limit=limit, repo=repo)
    except gastos_service.DatosInvalidosError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
