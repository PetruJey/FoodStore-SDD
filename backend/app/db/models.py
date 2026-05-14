from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel, func


class UsuarioModel(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, nullable=False, index=True)
    nombre: str = Field(nullable=False)
    password_hash: str = Field(nullable=False)
    telefono: Optional[str] = Field(default=None)

    created_at: datetime = Field(
        default=None,
        nullable=False,
        sa_column_kwargs={"server_default": func.now()},
    )
    updated_at: datetime = Field(
        default=None,
        nullable=False,
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()},
    )
    deleted_at: Optional[datetime] = Field(default=None, nullable=True)

    roles: list["UsuarioRolModel"] = Relationship(back_populates="usuario")


class RolModel(SQLModel, table=True):
    __tablename__ = "roles"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True, nullable=False, index=True)
    descripcion: Optional[str] = Field(default=None)

    created_at: datetime = Field(
        default=None,
        nullable=False,
        sa_column_kwargs={"server_default": func.now()},
    )
    updated_at: datetime = Field(
        default=None,
        nullable=False,
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()},
    )

    usuarios: list["UsuarioRolModel"] = Relationship(back_populates="rol")


class UsuarioRolModel(SQLModel, table=True):
    __tablename__ = "usuarios_roles"

    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuarios.id", nullable=False)
    rol_id: int = Field(foreign_key="roles.id", nullable=False)

    created_at: datetime = Field(
        default=None,
        nullable=False,
        sa_column_kwargs={"server_default": func.now()},
    )
    updated_at: datetime = Field(
        default=None,
        nullable=False,
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()},
    )

    usuario: UsuarioModel = Relationship(back_populates="roles")
    rol: RolModel = Relationship(back_populates="usuarios")


class RefreshTokenModel(SQLModel, table=True):
    __tablename__ = "refreshtokens"

    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuarios.id", nullable=False, index=True)
    token_hash: str = Field(nullable=False, index=True)
    family_id: str = Field(nullable=False, index=True)
    expires_at: datetime = Field(nullable=False)
    revoked_at: Optional[datetime] = Field(default=None, nullable=True)
    created_at: datetime = Field(
        default=None,
        nullable=False,
        sa_column_kwargs={"server_default": func.now()},
    )


class EstadoPedidoModel(SQLModel, table=True):
    __tablename__ = "estados_pedido"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=50, unique=True, index=True)
    descripcion: Optional[str] = None
    created_at: datetime = Field(
        default=None,
        nullable=False,
        sa_column_kwargs={"server_default": func.now()},
    )
    updated_at: datetime = Field(
        default=None,
        nullable=False,
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()},
    )


class FormaPagoModel(SQLModel, table=True):
    __tablename__ = "formas_pago"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=50, unique=True, index=True)
    descripcion: Optional[str] = None
    created_at: datetime = Field(
        default=None,
        nullable=False,
        sa_column_kwargs={"server_default": func.now()},
    )
    updated_at: datetime = Field(
        default=None,
        nullable=False,
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()},
    )
