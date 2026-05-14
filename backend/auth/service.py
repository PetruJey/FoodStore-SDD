from datetime import datetime, timedelta, timezone
from uuid import uuid4

from fastapi import HTTPException, status
from jose import JWTError
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.models.identidad import RolModel, UsuarioModel, UsuarioRolModel
from auth.repository import RefreshTokenRepository
from auth.schemas import AuthResponse, TokenRefreshResponse, UserRead
from core.config import get_settings
from core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from core.uow import UnitOfWork


class AuthService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def register(self, nombre: str, email: str, password: str) -> AuthResponse:
        async with self.uow:
            stmt = select(UsuarioModel).where(UsuarioModel.email == email)
            result = await self.uow.session.execute(stmt)
            existing = result.scalar_one_or_none()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="EMAIL_ALREADY_REGISTERED",
                )

            usuario = UsuarioModel(
                nombre=nombre,
                email=email,
                password_hash=hash_password(password),
                activo=True,
            )
            usuario = await self.uow.usuarios.create(usuario)

            stmt = select(RolModel).where(RolModel.nombre == "CLIENT")
            result = await self.uow.session.execute(stmt)
            rol = result.scalar_one_or_none()

            if rol:
                ur = UsuarioRolModel(usuario_id=usuario.id, rol_id=rol.id)
                self.uow.session.add(ur)
                await self.uow.session.flush()

            # Eager reload to avoid lazy loading in async context
            stmt = (
                select(UsuarioModel)
                .options(selectinload(UsuarioModel.roles).selectinload(UsuarioRolModel.rol))
                .where(UsuarioModel.id == usuario.id)
            )
            result = await self.uow.session.execute(stmt)
            usuario = result.scalar_one()

            roles_list = [ur.rol.nombre for ur in (usuario.roles or []) if ur.rol]

            settings = get_settings()
            token_id = str(uuid4())
            family_id = str(uuid4())

            access_token = create_access_token(data={"sub": str(usuario.id)})
            refresh_token = create_refresh_token(
                data={
                    "sub": str(usuario.id),
                    "jti": token_id,
                    "family_id": family_id,
                }
            )

            expires_at = datetime.now(timezone.utc) + timedelta(
                days=settings.refresh_token_expire_days
            )

            repo = RefreshTokenRepository(self.uow.session)
            await repo.create_token(
                user_id=usuario.id,
                token_id=token_id,
                family_id=family_id,
                expires_at=expires_at,
                token=refresh_token,
            )

            user_read = UserRead(
                id=usuario.id,
                nombre=usuario.nombre,
                email=usuario.email,
                roles=roles_list,
            )

            return AuthResponse(
                access_token=access_token,
                refresh_token=refresh_token,
                user=user_read,
            )

    async def login(self, email: str, password: str) -> AuthResponse:
        async with self.uow:
            users = await self.uow.usuarios.list_all(filters={"email": email})
            if not users:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales inválidas",
                )

            user = users[0]

            # Eager reload roles to avoid lazy loading in async context
            stmt = (
                select(UsuarioModel)
                .options(selectinload(UsuarioModel.roles).selectinload(UsuarioRolModel.rol))
                .where(UsuarioModel.id == user.id)
            )
            result = await self.uow.session.execute(stmt)
            user = result.scalar_one()

            if not user.activo:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales inválidas",
                )

            if not verify_password(password, user.password_hash):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales inválidas",
                )

            roles_list = [ur.rol.nombre for ur in (user.roles or []) if ur.rol]

            settings = get_settings()
            token_id = str(uuid4())
            family_id = str(uuid4())

            access_token = create_access_token(data={"sub": str(user.id)})
            refresh_token = create_refresh_token(
                data={
                    "sub": str(user.id),
                    "jti": token_id,
                    "family_id": family_id,
                }
            )

            expires_at = datetime.now(timezone.utc) + timedelta(
                days=settings.refresh_token_expire_days
            )

            repo = RefreshTokenRepository(self.uow.session)
            await repo.create_token(
                user_id=user.id,
                token_id=token_id,
                family_id=family_id,
                expires_at=expires_at,
                token=refresh_token,
            )

            user_read = UserRead(
                id=user.id,
                nombre=user.nombre,
                email=user.email,
                roles=roles_list,
            )

            return AuthResponse(
                access_token=access_token,
                refresh_token=refresh_token,
                user=user_read,
            )

    async def refresh(self, refresh_token_str: str) -> TokenRefreshResponse:
        try:
            payload = decode_token(refresh_token_str)
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
            )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
            )

        jti = payload.get("jti")
        if not jti or not isinstance(jti, str):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
            )

        async with self.uow:
            repo = RefreshTokenRepository(self.uow.session)
            stored_token = await repo.find_by_token_id(jti)

            if stored_token is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido",
                )

            if stored_token.revoked:
                await repo.revoke_family(stored_token.family_id)
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Sesión comprometida",
                )

            await repo.revoke_token(jti)

            family_id = stored_token.family_id
            user_id = stored_token.usuario_id

            # Verify user still exists and is active
            stmt = select(UsuarioModel).where(
                UsuarioModel.id == user_id,
                UsuarioModel.activo == True,
            )
            result = await self.uow.session.execute(stmt)
            user = result.scalar_one_or_none()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Usuario no encontrado",
                )

            new_token_id = str(uuid4())

            access_token = create_access_token(data={"sub": str(user_id)})
            new_refresh_token = create_refresh_token(
                data={
                    "sub": str(user_id),
                    "jti": new_token_id,
                    "family_id": family_id,
                }
            )

            settings = get_settings()
            expires_at = datetime.now(timezone.utc) + timedelta(
                days=settings.refresh_token_expire_days
            )

            await repo.create_token(
                user_id=user_id,
                token_id=new_token_id,
                family_id=family_id,
                expires_at=expires_at,
                token=new_refresh_token,
            )

            return TokenRefreshResponse(
                access_token=access_token,
                refresh_token=new_refresh_token,
            )

    async def logout(self, refresh_token_str: str) -> None:
        try:
            payload = decode_token(refresh_token_str)
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
            )

        jti = payload.get("jti")
        if not jti or not isinstance(jti, str):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
            )

        async with self.uow:
            repo = RefreshTokenRepository(self.uow.session)
            await repo.revoke_token(jti)
