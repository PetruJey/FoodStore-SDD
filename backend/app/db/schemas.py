from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class UsuarioCreate(SQLModel):
    email: str
    nombre: str
    password: str
    telefono: Optional[str] = None


class UsuarioRead(SQLModel):
    id: int
    email: str
    nombre: str
    telefono: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class UsuarioUpdate(SQLModel):
    email: Optional[str] = None
    nombre: Optional[str] = None
    password: Optional[str] = None
    telefono: Optional[str] = None


class RolRead(SQLModel):
    id: int
    nombre: str

    model_config = {"from_attributes": True}
