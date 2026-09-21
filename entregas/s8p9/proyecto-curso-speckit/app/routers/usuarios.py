from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioOut
from app.services import usuarios as usuarios_service
from app.core.security import crear_access_token

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.post("/", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario_in: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        return usuarios_service.registrar_usuario(db, usuario_in.email, usuario_in.password)
    except usuarios_service.EmailYaRegistradoError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/token")
def login_por_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        usuario = usuarios_service.autenticar_usuario(db, form_data.username, form_data.password)
        access_token = crear_access_token(data={"sub": str(usuario["id"])})
        return {"access_token": access_token, "token_type": "bearer"}
    except usuarios_service.CredencialesInvalidasError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
