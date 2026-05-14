from datetime import datetime
from typing import Optional, List

from sqlmodel import Field, Relationship, SQLModel


class UsuarioModel(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    nombre: str = Field(nullable=False)
    password_hash: str = Field(nullable=False)
    telefono: Optional[str] = Field(default=None, nullable=True)
    activo: bool = Field(default=True, nullable=False)
    creado_en: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    actualizado_en: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
        nullable=False,
    )
    eliminado_en: Optional[datetime] = Field(default=None, nullable=True)

    roles: List["UsuarioRolModel"] = Relationship(back_populates="usuario")
    refresh_tokens: List["RefreshTokenModel"] = Relationship(back_populates="usuario")
    direcciones: List["DireccionEntregaModel"] = Relationship(back_populates="usuario")
    pedidos: List["PedidoModel"] = Relationship(back_populates="usuario")


class RolModel(SQLModel, table=True):
    __tablename__ = "roles"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True, nullable=False)
    descripcion: Optional[str] = Field(default=None, nullable=True)
    creado_en: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    usuarios: List["UsuarioRolModel"] = Relationship(back_populates="rol")


class UsuarioRolModel(SQLModel, table=True):
    __tablename__ = "usuarios_roles"

    usuario_id: int = Field(foreign_key="usuarios.id", primary_key=True)
    rol_id: int = Field(foreign_key="roles.id", primary_key=True)
    creado_en: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    usuario: UsuarioModel = Relationship(back_populates="roles")
    rol: RolModel = Relationship(back_populates="usuarios")


class RefreshTokenModel(SQLModel, table=True):
    __tablename__ = "refresh_tokens"

    id: Optional[int] = Field(default=None, primary_key=True)
    token: str = Field(unique=True, index=True, nullable=False)
    usuario_id: int = Field(foreign_key="usuarios.id", nullable=False)
    expires_at: datetime = Field(nullable=False)
    revoked: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    usuario: UsuarioModel = Relationship(back_populates="refresh_tokens")


class DireccionEntregaModel(SQLModel, table=True):
    __tablename__ = "direcciones_entrega"

    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuarios.id", nullable=False)
    calle: str = Field(nullable=False)
    numero: str = Field(nullable=False)
    piso: Optional[str] = Field(default=None, nullable=True)
    depto: Optional[str] = Field(default=None, nullable=True)
    ciudad: str = Field(nullable=False)
    codigo_postal: str = Field(nullable=False)
    referencia: Optional[str] = Field(default=None, nullable=True)
    es_predeterminada: bool = Field(default=False, nullable=False)
    creado_en: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    actualizado_en: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
        nullable=False,
    )

    usuario: UsuarioModel = Relationship(back_populates="direcciones")
