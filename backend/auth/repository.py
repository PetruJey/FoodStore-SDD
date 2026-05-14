from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.identidad import RefreshTokenModel
from core.repository import BaseRepository


class RefreshTokenRepository(BaseRepository[RefreshTokenModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(RefreshTokenModel, session)

    async def create_token(
        self,
        user_id: int,
        token_id: str,
        family_id: str,
        expires_at: datetime,
        token: str,
    ) -> RefreshTokenModel:
        rt = RefreshTokenModel(
            token_id=token_id,
            token=token,
            family_id=family_id,
            usuario_id=user_id,
            expires_at=expires_at,
        )
        return await self.create(rt)

    async def find_by_token_id(self, token_id: str) -> Optional[RefreshTokenModel]:
        stmt = select(RefreshTokenModel).where(RefreshTokenModel.token_id == token_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def revoke_token(self, token_id: str) -> None:
        token = await self.find_by_token_id(token_id)
        if token:
            token.revoked = True
            await self.session.flush()

    async def revoke_family(self, family_id: str) -> None:
        stmt = select(RefreshTokenModel).where(RefreshTokenModel.family_id == family_id)
        result = await self.session.execute(stmt)
        tokens = result.scalars().all()
        for token in tokens:
            token.revoked = True
        await self.session.flush()

    async def get_active_by_user(self, user_id: int) -> list[RefreshTokenModel]:
        stmt = (
            select(RefreshTokenModel)
            .where(RefreshTokenModel.usuario_id == user_id)
            .where(RefreshTokenModel.revoked == False)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
