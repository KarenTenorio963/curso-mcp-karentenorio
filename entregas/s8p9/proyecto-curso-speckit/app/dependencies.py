from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.repositories import usuarios as usuarios_repo
from app.repositories import gastos as gastos_repo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/token")

def get_gastos_repo():
    return gastos_repo

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> int:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        usuario_id: int = payload.get("sub")
        if usuario_id is None:
            raise credentials_exception
        return usuario_id
    except jwt.PyJWTError:
        raise credentials_exception
