from sqlalchemy.orm import Session
from app.repositories import usuarios as usuarios_repository
from app.core.security import obtener_password_hash, verificar_password

class EmailYaRegistradoError(Exception):
    pass

class CredencialesInvalidasError(Exception):
    pass

def registrar_usuario(db: Session, email: str, password: str, repo=usuarios_repository) -> dict:
    existente = repo.obtener_por_email(db, email)
    if existente:
        raise EmailYaRegistradoError("El email ya está registrado")
    
    hashed_pwd = obtener_password_hash(password)
    usuario = repo.guardar(db, email, hashed_pwd)
    return {"id": usuario.id, "email": usuario.email}

def autenticar_usuario(db: Session, email: str, password: str, repo=usuarios_repository) -> dict:
    usuario = repo.obtener_por_email(db, email)
    if not usuario or not verificar_password(password, usuario.hashed_password):
        raise CredencialesInvalidasError("Credenciales inválidas")
    return {"id": usuario.id, "email": usuario.email}
