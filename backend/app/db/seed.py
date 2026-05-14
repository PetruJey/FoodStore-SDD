from sqlmodel import Session, select

from app.core.security import hash_password
from app.db.models import EstadoPedidoModel, FormaPagoModel, RolModel, UsuarioModel, UsuarioRolModel


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

    estados_data = [
        {"nombre": "PENDIENTE", "descripcion": "Pedido creado, esperando pago"},
        {"nombre": "CONFIRMADO", "descripcion": "Pago aprobado, pedido en preparación"},
        {"nombre": "EN_PREPARACION", "descripcion": "Pedido en preparación"},
        {"nombre": "EN_CAMINO", "descripcion": "Pedido en camino"},
        {"nombre": "ENTREGADO", "descripcion": "Entregado al cliente"},
        {"nombre": "CANCELADO", "descripcion": "Pedido cancelado"},
    ]

    for estado_data in estados_data:
        existing = session.exec(
            select(EstadoPedidoModel).where(EstadoPedidoModel.nombre == estado_data["nombre"])
        ).first()
        if not existing:
            session.add(EstadoPedidoModel(**estado_data))

    formas_pago_data = [
        {"nombre": "MERCADOPAGO", "descripcion": "Pago con MercadoPago (tarjeta/débito/efectivo)"},
        {"nombre": "EFECTIVO", "descripcion": "Pago en efectivo al recibir"},
    ]

    for fp_data in formas_pago_data:
        existing = session.exec(
            select(FormaPagoModel).where(FormaPagoModel.nombre == fp_data["nombre"])
        ).first()
        if not existing:
            session.add(FormaPagoModel(**fp_data))

    session.commit()
