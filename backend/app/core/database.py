from collections.abc import AsyncGenerator

from sqlmodel import Session, SQLModel, create_engine

from app.core.config import get_settings

settings = get_settings()

engine = create_engine(settings.DATABASE_URL, echo=False)


async def get_session() -> AsyncGenerator[Session, None]:
    with Session(engine) as session:
        yield session
