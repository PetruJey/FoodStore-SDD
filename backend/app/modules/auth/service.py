import hashlib
import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException, Request, status

from app.core.errors import BadRequestError, NotFoundError, UnauthorizedError
from sqlmodel import Session, select

from app.core.config import get_settings
from app.core import security
from app.core.unit_of_work import UnitOfWork
from app.db.models import RefreshTokenModel, RolModel, UsuarioModel, UsuarioRolModel

settings = get_settings()


def _generate_refresh_token() -> str:
    return str(uuid.uuid4())


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def _get_roles(db: Session, usuario: UsuarioModel) -> list[str]:
    statement = (
        select(RolModel.nombre)
        .join(UsuarioRolModel, RolModel.id == UsuarioRolModel.rol_id)
        .where(UsuarioRolModel.usuario_id == usuario.id)
    )
    return list(db.exec(statement).all())


def _create_tokens(db: Session, usuario: UsuarioModel) -> dict:
    roles = _get_roles(db, usuario)

    access_token = security.create_access_token(
        data={
            "sub": str(usuario.id),
            "email": usuario.email,
            "rol": roles,
        }
    )

    raw_token = _generate_refresh_token()
    token_hash = _hash_token(raw_token)
    family_id = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    refresh = RefreshTokenModel(
        usuario_id=usuario.id,
        token_hash=token_hash,
        family_id=family_id,
        expires_at=expires_at,
    )
    db.add(refresh)

    return {
        "access_token": access_token,
        "refresh_token": raw_token,
        "token_type": "bearer",
        "user": {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "roles": roles,
        },
    }


def register(db: Session, data: "RegisterRequest") -> dict:
    with UnitOfWork(db):
        existing = db.exec(
            select(UsuarioModel).where(UsuarioModel.email == data.email)
        ).first()
        if existing:
            raise BadRequestError(message="El email ya está registrado")

        hashed = security.hash_password(data.password)
        usuario = UsuarioModel(
            nombre=data.nombre,
            email=data.email,
            password_hash=hashed,
        )
        db.add(usuario)
        db.flush()

        rol = db.exec(
            select(RolModel).where(RolModel.nombre == "CLIENT")
        ).first()
        if not rol:
            raise NotFoundError(message="Error de configuración: rol CLIENT no encontrado")
        user_rol = UsuarioRolModel(usuario_id=usuario.id, rol_id=rol.id)
        db.add(user_rol)

        return _create_tokens(db, usuario)


def login(db: Session, data: "LoginRequest", request: Request) -> dict:
    with UnitOfWork(db):
        usuario = db.exec(
            select(UsuarioModel).where(UsuarioModel.email == data.email)
        ).first()

        if (
            not usuario
            or usuario.deleted_at is not None
            or not security.verify_password(data.password, usuario.password_hash)
        ):
            raise UnauthorizedError(message="Credenciales inválidas")

        return _create_tokens(db, usuario)


def refresh_token(db: Session, token_str: str) -> dict:
    token_hash = _hash_token(token_str)

    refresh = db.exec(
        select(RefreshTokenModel).where(
            RefreshTokenModel.token_hash == token_hash
        )
    ).first()

    # NOTA: Se mantiene HTTPException (no AppError) porque refresh_token() hace commit
    # antes del raise (detección de replay attacks). El error es genuinamente HTTP
    # y el commit ya fue ejecutado, por lo que AppError no aplica aquí.
    if refresh is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de refresco inválido",
        )

    now = datetime.utcnow()

    if refresh.revoked_at is not None:
        family = db.exec(
            select(RefreshTokenModel).where(
                RefreshTokenModel.family_id == refresh.family_id,
                RefreshTokenModel.revoked_at.is_(None),
            )
        ).all()
        for t in family:
            t.revoked_at = now
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de refresco inválido",
        )

    if refresh.expires_at < now:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de refresco expirado",
        )

    refresh.revoked_at = now

    usuario = db.get(UsuarioModel, refresh.usuario_id)
    if usuario is None or usuario.deleted_at is not None:
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
        )

    db.commit()
    return _create_tokens(db, usuario)


def logout(db: Session, token_str: str) -> None:
    with UnitOfWork(db):
        token_hash = _hash_token(token_str)
        refresh = db.exec(
            select(RefreshTokenModel).where(
                RefreshTokenModel.token_hash == token_hash,
                RefreshTokenModel.revoked_at.is_(None),
            )
        ).first()
        if refresh:
            refresh.revoked_at = datetime.utcnow()
