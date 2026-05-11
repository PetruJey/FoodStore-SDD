from sqlmodel import Session, select

from app.core.security import hash_password
from app.db.models import RolModel, UsuarioModel, UsuarioRolModel


def create_seed_data(session: Session) -> None:
    roles_data = [
        {"nombre": "ADMIN", "descripcion": "Acceso completo al sistema"},
        {"nombre": "STOCK", "descripcion": "Gestión de catálogo y stock"},
        {"nombre": "PEDIDOS", "descripcion": "Gestión de pedidos"},
        {"nombre": "CLIENT", "descripcion": "Usuario cliente"},
    ]

    existing_roles = {}
    for role_data in roles_data:
        existing = session.exec(
            select(RolModel).where(RolModel.nombre == role_data["nombre"])
        ).first()
        if existing:
            existing_roles[role_data["nombre"]] = existing
        else:
            rol = RolModel(**role_data)
            session.add(rol)
            session.flush()
            existing_roles[role_data["nombre"]] = rol

    existing_user = session.exec(
        select(UsuarioModel).where(UsuarioModel.email == "admin@foodstore.com")
    ).first()
    if existing_user is None:
        admin_user = UsuarioModel(
            email="admin@foodstore.com",
            nombre="Admin",
            password_hash=hash_password("Admin123!"),
            telefono="",
        )
        session.add(admin_user)
        session.flush()

        admin_rol = existing_roles["ADMIN"]
        usuario_rol = UsuarioRolModel(
            usuario_id=admin_user.id,
            rol_id=admin_rol.id,
        )
        session.add(usuario_rol)

    session.commit()
