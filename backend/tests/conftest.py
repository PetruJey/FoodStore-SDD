import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)

import core.database

core.database.async_session_factory = TestSessionLocal
core.database.engine = test_engine

from main import app
from core.database import get_session
from core.security import create_access_token, hash_password
from core.config import get_settings
from app.models.identidad import UsuarioModel, RolModel, UsuarioRolModel


async def override_get_session():
    async with TestSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# Only create identity tables needed for RBAC tests
# (avoids ARRAY type from ventas/detalles_pedido not supported by SQLite)
IDENTITY_TABLES = [
    SQLModel.metadata.tables["usuarios"],
    SQLModel.metadata.tables["roles"],
    SQLModel.metadata.tables["usuarios_roles"],
    SQLModel.metadata.tables["refresh_tokens"],
    SQLModel.metadata.tables["direcciones_entrega"],
]


@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all, tables=IDENTITY_TABLES)

    async with TestSessionLocal() as session:
        roles_data = [
            RolModel(id=1, nombre="ADMIN", descripcion="Administrador del sistema"),
            RolModel(id=2, nombre="STOCK", descripcion="Gestor de Stock"),
            RolModel(id=3, nombre="PEDIDOS", descripcion="Gestor de Pedidos"),
            RolModel(id=4, nombre="CLIENT", descripcion="Cliente"),
        ]
        for r in roles_data:
            session.add(r)

        admin = UsuarioModel(
            id=1,
            email="admin@test.com",
            nombre="Admin Test",
            password_hash=hash_password("Admin1234!"),
            activo=True,
        )
        session.add(admin)
        await session.flush()
        session.add(UsuarioRolModel(usuario_id=1, rol_id=1))
        await session.commit()

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all, tables=IDENTITY_TABLES)


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def admin_token():
    return create_access_token(data={"sub": "1"})


@pytest_asyncio.fixture
async def admin_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


@pytest_asyncio.fixture
async def client_user():
    async with TestSessionLocal() as session:
        user = UsuarioModel(
            email="client@test.com",
            nombre="Client Test",
            password_hash=hash_password("Client1234!"),
            activo=True,
        )
        session.add(user)
        await session.flush()
        session.add(UsuarioRolModel(usuario_id=user.id, rol_id=4))
        await session.commit()
    return user
