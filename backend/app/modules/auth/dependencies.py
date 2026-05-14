from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select

from app.core.database import get_session
from app.core import security
from app.db.models import RolModel, UsuarioModel, UsuarioRolModel

oauth2_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_session),
) -> UsuarioModel:
    payload = security.decode_access_token(credentials.credentials)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    usuario = db.get(UsuarioModel, int(user_id))
    if usuario is None or usuario.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return usuario


def require_role(roles: list[str]):
    async def role_checker(
        current_user: UsuarioModel = Depends(get_current_user),
        db: Session = Depends(get_session),
    ) -> UsuarioModel:
        statement = (
            select(RolModel.nombre)
            .join(UsuarioRolModel, RolModel.id == UsuarioRolModel.rol_id)
            .where(UsuarioRolModel.usuario_id == current_user.id)
        )
        user_roles = db.exec(statement).all()

        if not any(r in user_roles for r in roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para acceder a este recurso",
            )
        return current_user

    return role_checker
