from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.repositories import productos as productos_repo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/token")

def get_productos_repo():
    return productos_repo

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> int:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticacion invalidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        usuario_id_str = payload.get("sub")
        if usuario_id_str is None:
            raise credentials_exception
        return int(usuario_id_str)
    except (jwt.PyJWTError, ValueError):
        raise credentials_exception
