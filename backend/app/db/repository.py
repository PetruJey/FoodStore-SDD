from datetime import datetime, timezone
from typing import Generic, Optional, Type, TypeVar

from sqlmodel import SQLModel, Session, select

T = TypeVar("T", bound=SQLModel)


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session = session

    def get_by_id(self, id: int) -> Optional[T]:
        return self.session.get(self.model, id)

    def list(self, skip: int = 0, limit: int = 100) -> list[T]:
        statement = select(self.model).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def create(self, obj_in: T) -> T:
        self.session.add(obj_in)
        self.session.flush()
        self.session.refresh(obj_in)
        return obj_in

    def update(self, id: int, obj_in: T) -> Optional[T]:
        db_obj = self.get_by_id(id)
        if db_obj is None:
            return None
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        self.session.add(db_obj)
        self.session.flush()
        self.session.refresh(db_obj)
        return db_obj

    def delete(self, id: int) -> bool:
        db_obj = self.get_by_id(id)
        if db_obj is None:
            return False
        if hasattr(db_obj, "deleted_at"):
            setattr(db_obj, "deleted_at", datetime.now(timezone.utc))
            self.session.add(db_obj)
            self.session.flush()
            return True
        self.session.delete(db_obj)
        self.session.flush()
        return True
