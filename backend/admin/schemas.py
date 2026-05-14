from pydantic import BaseModel


class RolResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str | None = None

    class Config:
        from_attributes = True


class UsuarioRolesResponse(BaseModel):
    usuario_id: int
    roles: list[RolResponse]


class AsignarRolesRequest(BaseModel):
    roles: list[int]
