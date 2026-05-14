import asyncio

from sqlalchemy import text

from core.database import async_session_factory, engine
from core.security import hash_password


ROLES = [
    {"id": 1, "nombre": "ADMIN", "descripcion": "Administrador del sistema"},
    {"id": 2, "nombre": "STOCK", "descripcion": "Gestor de Stock"},
    {"id": 3, "nombre": "PEDIDOS", "descripcion": "Gestor de Pedidos"},
    {"id": 4, "nombre": "CLIENT", "descripcion": "Cliente"},
]

ESTADOS_PEDIDO = [
    {"id": 1, "nombre": "PENDIENTE", "es_terminal": False},
    {"id": 2, "nombre": "CONFIRMADO", "es_terminal": False},
    {"id": 3, "nombre": "EN_PREPARACION", "es_terminal": False},
    {"id": 4, "nombre": "EN_CAMINO", "es_terminal": False},
    {"id": 5, "nombre": "ENTREGADO", "es_terminal": True},
    {"id": 6, "nombre": "CANCELADO", "es_terminal": True},
]

FORMAS_PAGO = [
    {"id": 1, "nombre": "MercadoPago", "habilitado": True},
    {"id": 2, "nombre": "Efectivo", "habilitado": True},
    {"id": 3, "nombre": "Transferencia Bancaria", "habilitado": True},
]


async def seed() -> None:
    async with async_session_factory() as session:
        for rol in ROLES:
            await session.execute(
                text("""
                    INSERT INTO roles (id, nombre, descripcion, creado_en)
                    VALUES (:id, :nombre, :descripcion, NOW())
                    ON CONFLICT (id) DO NOTHING
                """),
                rol,
            )

        for estado in ESTADOS_PEDIDO:
            await session.execute(
                text("""
                    INSERT INTO estados_pedido (id, nombre, es_terminal, creado_en)
                    VALUES (:id, :nombre, :es_terminal, NOW())
                    ON CONFLICT (id) DO NOTHING
                """),
                estado,
            )

        for fp in FORMAS_PAGO:
            await session.execute(
                text("""
                    INSERT INTO formas_pago (id, nombre, habilitado, creado_en)
                    VALUES (:id, :nombre, :habilitado, NOW())
                    ON CONFLICT (id) DO NOTHING
                """),
                fp,
            )

        admin_email = "admin@foodstore.com"
        hashed = hash_password("Admin1234!")
        result = await session.execute(
            text("""
                INSERT INTO usuarios (email, nombre, password_hash, activo, creado_en, actualizado_en)
                VALUES (:email, :nombre, :password_hash, TRUE, NOW(), NOW())
                ON CONFLICT (email) DO NOTHING
                RETURNING id
            """),
            {"email": admin_email, "nombre": "Admin", "password_hash": hashed},
        )
        admin_id = result.scalar_one_or_none()
        if admin_id is not None:
            await session.execute(
                text("""
                    INSERT INTO usuarios_roles (usuario_id, rol_id, creado_en)
                    VALUES (:usuario_id, 1, NOW())
                    ON CONFLICT (usuario_id, rol_id) DO NOTHING
                """),
                {"usuario_id": admin_id},
            )

        await session.commit()


async def main() -> None:
    try:
        await seed()
        print("Seed completado exitosamente.")
    except Exception as e:
        print(f"Seed falló: {e}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
