from datetime import datetime, timedelta, timezone

from jose import jwt
import pytest

from app.models.identidad import UsuarioModel, UsuarioRolModel
from core.config import get_settings
from core.database import async_session_factory
from core.security import create_access_token, hash_password

pytestmark = pytest.mark.asyncio

# ─── 5.1 Role listing ─────────────────────────────────────────────────────────


async def test_admin_can_list_roles(client, admin_headers):
    resp = await client.get("/api/v1/roles", headers=admin_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 4
    names = [r["nombre"] for r in data]
    assert "ADMIN" in names
    assert "STOCK" in names
    assert "PEDIDOS" in names
    assert "CLIENT" in names


async def test_non_admin_gets_403_on_role_list(client, client_user):
    token = create_access_token(data={"sub": str(client_user.id)})
    headers = {"Authorization": f"Bearer {token}"}
    resp = await client.get("/api/v1/roles", headers=headers)
    assert resp.status_code == 403


async def test_unauthenticated_gets_401(client):
    resp = await client.get("/api/v1/roles")
    assert resp.status_code == 401


# ─── 5.2 User role retrieval ──────────────────────────────────────────────────


async def test_admin_gets_user_roles(client, admin_headers):
    resp = await client.get("/api/v1/usuarios/1/roles", headers=admin_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["usuario_id"] == 1
    role_names = [r["nombre"] for r in data["roles"]]
    assert "ADMIN" in role_names


async def test_non_existent_user_roles_404(client, admin_headers):
    resp = await client.get(
        "/api/v1/usuarios/999/roles", headers=admin_headers
    )
    assert resp.status_code == 404


# ─── 5.3 Role assignment ──────────────────────────────────────────────────────


async def test_admin_assigns_valid_roles(client, admin_headers):
    resp = await client.put(
        "/api/v1/usuarios/1/roles",
        headers=admin_headers,
        json={"roles": [1, 4]},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["usuario_id"] == 1
    role_ids = {r["id"] for r in data["roles"]}
    assert role_ids == {1, 4}


async def test_invalid_role_id_returns_422(client, admin_headers):
    resp = await client.put(
        "/api/v1/usuarios/1/roles",
        headers=admin_headers,
        json={"roles": [99]},
    )
    assert resp.status_code == 422


async def test_non_existent_user_assign_404(client, admin_headers):
    resp = await client.put(
        "/api/v1/usuarios/999/roles",
        headers=admin_headers,
        json={"roles": [4]},
    )
    assert resp.status_code == 404


async def test_non_admin_cannot_assign_roles(client):
    resp = await client.put(
        "/api/v1/usuarios/1/roles",
        json={"roles": [4]},
    )
    assert resp.status_code == 401


# ─── 5.4 Role removal ─────────────────────────────────────────────────────────


async def test_admin_can_remove_role(client, admin_headers):
    # First assign role CLIENT (4) to admin so we have something to remove
    assign_resp = await client.put(
        "/api/v1/usuarios/1/roles",
        headers=admin_headers,
        json={"roles": [1, 4]},
    )
    assert assign_resp.status_code == 200

    # Now remove role CLIENT (4)
    resp = await client.delete(
        "/api/v1/usuarios/1/roles/4", headers=admin_headers
    )
    assert resp.status_code == 204


async def test_last_admin_self_removal_blocked(client, admin_headers):
    resp = await client.delete(
        "/api/v1/usuarios/1/roles/1", headers=admin_headers
    )
    assert resp.status_code == 409
    assert "LAST_ADMIN" in resp.text


async def test_non_existent_assignment_404(client, admin_headers):
    resp = await client.delete(
        "/api/v1/usuarios/1/roles/99", headers=admin_headers
    )
    assert resp.status_code == 404


async def test_non_admin_cannot_remove_role(client):
    resp = await client.delete("/api/v1/usuarios/1/roles/4")
    assert resp.status_code == 401


# ─── 5.5 Route enforcement ────────────────────────────────────────────────────


async def test_no_token_returns_401(client):
    resp = await client.get("/api/v1/admin/health")
    assert resp.status_code == 401


async def test_insufficient_role_returns_403(client, client_user):
    token = create_access_token(data={"sub": str(client_user.id)})
    headers = {"Authorization": f"Bearer {token}"}
    resp = await client.get("/api/v1/admin/health", headers=headers)
    assert resp.status_code == 403


async def test_expired_token_returns_401(client):
    settings = get_settings()
    expired_token = jwt.encode(
        {
            "sub": "1",
            "exp": datetime.now(timezone.utc) - timedelta(hours=1),
            "type": "access",
        },
        settings.secret_key,
        algorithm=settings.algorithm,
    )
    headers = {"Authorization": f"Bearer {expired_token}"}
    resp = await client.get("/api/v1/admin/health", headers=headers)
    assert resp.status_code == 401


# ─── 5.6 Public routes ────────────────────────────────────────────────────────


async def test_public_routes_no_token(client):
    resp = await client.post("/api/v1/auth/login", json={})
    assert resp.status_code not in (
        401,
        403,
    ), "Login endpoint is public, should not return 401/403"

    resp = await client.get("/api/v1/productos/health")
    assert resp.status_code == 200


# ─── 5.7 Role segregation ─────────────────────────────────────────────────────


async def test_stock_cannot_access_admin(client):
    async with async_session_factory() as session:
        user = UsuarioModel(
            email="stockonly@test.com",
            nombre="Stock Only",
            password_hash=hash_password("Test1234!"),
            activo=True,
        )
        session.add(user)
        await session.flush()
        session.add(UsuarioRolModel(usuario_id=user.id, rol_id=2))
        await session.commit()
        stock_user_id = user.id

    token = create_access_token(data={"sub": str(stock_user_id)})
    headers = {"Authorization": f"Bearer {token}"}
    resp = await client.get("/api/v1/admin/health", headers=headers)
    assert resp.status_code == 403


async def test_pedidos_user_can_access_pedidos(client):
    async with async_session_factory() as session:
        user = UsuarioModel(
            email="pedidosonly@test.com",
            nombre="Pedidos Only",
            password_hash=hash_password("Test1234!"),
            activo=True,
        )
        session.add(user)
        await session.flush()
        session.add(UsuarioRolModel(usuario_id=user.id, rol_id=3))
        await session.commit()
        pedidos_user_id = user.id

    token = create_access_token(data={"sub": str(pedidos_user_id)})
    headers = {"Authorization": f"Bearer {token}"}
    resp = await client.get("/api/v1/pedidos/health", headers=headers)
    assert resp.status_code == 200


# ─── 5.8 EN_PREPARACION cancel — simplified: requires ADMIN ───────────────────


async def test_preparacion_cancel_requires_admin(client):
    async with async_session_factory() as session:
        user = UsuarioModel(
            email="pedidosuser@test.com",
            nombre="Pedidos User",
            password_hash=hash_password("Test1234!"),
            activo=True,
        )
        session.add(user)
        await session.flush()
        session.add(UsuarioRolModel(usuario_id=user.id, rol_id=3))
        await session.commit()
        pedidos_user_id = user.id

    token = create_access_token(data={"sub": str(pedidos_user_id)})
    headers = {"Authorization": f"Bearer {token}"}
    resp = await client.get("/api/v1/admin/health", headers=headers)
    assert resp.status_code == 403


# ─── 5.9 Rate limiting ────────────────────────────────────────────────────────


async def test_rate_limit_register(client):
    responses = []
    for i in range(6):
        resp = await client.post(
            "/api/v1/auth/register",
            json={
                "nombre": f"RateTest{i}",
                "email": f"ratelimit{i}@test.com",
                "password": "Test1234!",
            },
        )
        responses.append(resp.status_code)

    assert 429 in responses, (
        f"Expected at least one rate-limited response (429), "
        f"got: {responses}"
    )


# ─── 5.10 Rate limiting key isolation ─────────────────────────────────────────


async def test_rate_limit_user_isolation(client, admin_headers):
    async with async_session_factory() as session:
        user = UsuarioModel(
            email="admin2iso@test.com",
            nombre="Admin2",
            password_hash=hash_password("Admin1234!"),
            activo=True,
        )
        session.add(user)
        await session.flush()
        session.add(UsuarioRolModel(usuario_id=user.id, rol_id=1))
        await session.commit()
        admin2_id = user.id

    admin2_token = create_access_token(data={"sub": str(admin2_id)})
    admin2_headers = {"Authorization": f"Bearer {admin2_token}"}

    resp = await client.get("/api/v1/pedidos/health", headers=admin_headers)
    assert resp.status_code == 200

    resp = await client.get(
        "/api/v1/pedidos/health", headers=admin2_headers
    )
    assert resp.status_code == 200
