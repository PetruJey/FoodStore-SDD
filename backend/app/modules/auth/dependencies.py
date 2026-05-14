from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.errors import UnauthorizedError, ForbiddenError
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
        raise UnauthorizedError(message="Token inválido o expirado")

    user_id = payload.get("sub")
    if user_id is None:
        raise UnauthorizedError(message="Token inválido")

    usuario = db.get(UsuarioModel, int(user_id))
    if usuario is None or usuario.deleted_at is not None:
        raise UnauthorizedError(message="Usuario no encontrado")

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
            raise ForbiddenError(message="No tienes permisos para acceder a este recurso")
        return current_user

    return role_checker
