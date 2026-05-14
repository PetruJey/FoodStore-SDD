from typing import Any, Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select, func

T = TypeVar("T", bound=SQLModel)


class BaseRepository(Generic[T]):
    def __init__(self, model_class: type[T], session: AsyncSession):
        self.model_class = model_class
        self.session = session

    async def get_by_id(self, id: Any) -> T | None:
        stmt = select(self.model_class).where(
            self.model_class.id == id,  # type: ignore
        )
        if hasattr(self.model_class, "eliminado_en"):
            stmt = stmt.where(self.model_class.eliminado_en.is_(None))  # type: ignore
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: dict[str, Any] | None = None,
    ) -> list[T]:
        stmt = select(self.model_class)
        if hasattr(self.model_class, "eliminado_en"):
            stmt = stmt.where(self.model_class.eliminado_en.is_(None))  # type: ignore
        if filters:
            for field, value in filters.items():
                column = getattr(self.model_class, field, None)
                if column is not None:
                    stmt = stmt.where(column == value)
        stmt = stmt.offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def count(self, filters: dict[str, Any] | None = None) -> int:
        stmt = select(func.count()).select_from(self.model_class)
        if hasattr(self.model_class, "eliminado_en"):
            stmt = stmt.where(self.model_class.eliminado_en.is_(None))  # type: ignore
        if filters:
            for field, value in filters.items():
                column = getattr(self.model_class, field, None)
                if column is not None:
                    stmt = stmt.where(column == value)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def create(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def update(self, id: Any, data: dict[str, Any]) -> T | None:
        obj = await self.get_by_id(id)
        if obj is None:
            return None
        for field, value in data.items():
            setattr(obj, field, value)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def soft_delete(self, id: Any) -> bool:
        obj = await self.get_by_id(id)
        if obj is None:
            return False
        from datetime import datetime, timezone

        obj.eliminado_en = datetime.now(timezone.utc)  # type: ignore
        await self.session.flush()
        return True

    async def hard_delete(self, id: Any) -> bool:
        obj = await self.get_by_id(id)
        if obj is None:
            return False
        await self.session.delete(obj)
        await self.session.flush()
        return True
