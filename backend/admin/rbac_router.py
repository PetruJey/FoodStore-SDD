from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import selectinload
from sqlmodel import select, delete, func

from admin.schemas import AsignarRolesRequest, RolResponse, UsuarioRolesResponse
from app.models.identidad import RolModel, UsuarioModel, UsuarioRolModel
from core.dependencies import require_role
from core.uow import UnitOfWork

router = APIRouter(tags=["roles"])


class RolesService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def list_roles(self) -> list[RolResponse]:
        async with self.uow:
            roles = await self.uow.roles.list_all()
            return [RolResponse.model_validate(r) for r in roles]

    async def get_user_roles(self, usuario_id: int) -> UsuarioRolesResponse:
        async with self.uow:
            stmt = (
                select(UsuarioModel)
                .options(selectinload(UsuarioModel.roles).selectinload(UsuarioRolModel.rol))
                .where(UsuarioModel.id == usuario_id)
            )
            result = await self.uow.session.execute(stmt)
            user = result.scalar_one_or_none()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="USUARIO_NO_ENCONTRADO",
                )
            roles = [RolResponse.model_validate(ur.rol) for ur in user.roles]
            return UsuarioRolesResponse(usuario_id=user.id, roles=roles)

    async def assign_roles(self, usuario_id: int, rol_ids: list[int]) -> UsuarioRolesResponse:
        async with self.uow:
            user = await self.uow.usuarios.get_by_id(usuario_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="USUARIO_NO_ENCONTRADO",
                )

            if rol_ids:
                stmt = select(RolModel.id).where(RolModel.id.in_(rol_ids))
                result = await self.uow.session.execute(stmt)
                existing_ids = {row[0] for row in result.all()}
                invalid_ids = set(rol_ids) - existing_ids
                if invalid_ids:
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail=f"ROLES_NOT_FOUND: {sorted(invalid_ids)}",
                    )

            stmt = delete(UsuarioRolModel).where(UsuarioRolModel.usuario_id == usuario_id)
            await self.uow.session.execute(stmt)

            for rol_id in rol_ids:
                ur = UsuarioRolModel(usuario_id=usuario_id, rol_id=rol_id)
                self.uow.session.add(ur)

            stmt = (
                select(UsuarioModel)
                .options(selectinload(UsuarioModel.roles).selectinload(UsuarioRolModel.rol))
                .where(UsuarioModel.id == usuario_id)
            )
            result = await self.uow.session.execute(stmt)
            user = result.scalar_one()
            roles = [RolResponse.model_validate(ur.rol) for ur in user.roles]
            return UsuarioRolesResponse(usuario_id=user.id, roles=roles)

    async def remove_role(self, usuario_id: int, rol_id: int, current_user_id: int) -> None:
        async with self.uow:
            stmt = (
                select(UsuarioModel)
                .options(selectinload(UsuarioModel.roles).selectinload(UsuarioRolModel.rol))
                .where(UsuarioModel.id == usuario_id)
            )
            result = await self.uow.session.execute(stmt)
            user = result.scalar_one_or_none()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="USUARIO_NO_ENCONTRADO",
                )

            stmt = select(UsuarioRolModel).where(
                UsuarioRolModel.usuario_id == usuario_id,
                UsuarioRolModel.rol_id == rol_id,
            )
            result = await self.uow.session.execute(stmt)
            ur = result.scalar_one_or_none()
            if not ur:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="ASIGNACION_NO_ENCONTRADA",
                )

            if rol_id == 1 and usuario_id == current_user_id:
                stmt = (
                    select(func.count())
                    .select_from(UsuarioRolModel)
                    .where(UsuarioRolModel.rol_id == 1)
                )
                result = await self.uow.session.execute(stmt)
                admin_count = result.scalar_one()
                if admin_count <= 1:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="LAST_ADMIN",
                    )

            await self.uow.session.delete(ur)


@router.get("/roles")
async def list_roles(current_user=Depends(require_role(["ADMIN"]))):
    uow = UnitOfWork()
    service = RolesService(uow)
    return await service.list_roles()


@router.get("/usuarios/{usuario_id}/roles")
async def get_user_roles(usuario_id: int, current_user=Depends(require_role(["ADMIN"]))):
    uow = UnitOfWork()
    service = RolesService(uow)
    return await service.get_user_roles(usuario_id)


@router.put("/usuarios/{usuario_id}/roles")
async def assign_roles(
    usuario_id: int,
    body: AsignarRolesRequest,
    current_user=Depends(require_role(["ADMIN"])),
):
    uow = UnitOfWork()
    service = RolesService(uow)
    return await service.assign_roles(usuario_id, body.roles)


@router.delete("/usuarios/{usuario_id}/roles/{rol_id}", status_code=204)
async def remove_role(
    usuario_id: int,
    rol_id: int,
    current_user=Depends(require_role(["ADMIN"])),
):
    uow = UnitOfWork()
    service = RolesService(uow)
    await service.remove_role(usuario_id, rol_id, current_user.id)
