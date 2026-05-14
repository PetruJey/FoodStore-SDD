from datetime import datetime
from typing import Optional, List

from sqlalchemy import JSON, Column, Numeric
from sqlalchemy.dialects.postgresql import ARRAY, INTEGER
from sqlmodel import Field, Relationship, SQLModel


class FormaPagoModel(SQLModel, table=True):
    __tablename__ = "formas_pago"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(nullable=False)
    habilitado: bool = Field(default=True, nullable=False)
    creado_en: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    pagos: List["PagoModel"] = Relationship(back_populates="forma_pago")


class EstadoPedidoModel(SQLModel, table=True):
    __tablename__ = "estados_pedido"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True, nullable=False)
    es_terminal: bool = Field(default=False, nullable=False)
    creado_en: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    pedidos: List["PedidoModel"] = Relationship(back_populates="estado")


class PedidoModel(SQLModel, table=True):
    __tablename__ = "pedidos"

    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuarios.id", nullable=False)
    estado_id: int = Field(foreign_key="estados_pedido.id", nullable=False)
    direccion_entrega: Optional[dict] = Field(
        default=None, sa_column=Column(JSON, nullable=True)
    )
    total: float = Field(sa_column=Column(Numeric(10, 2), nullable=False))
    creado_en: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    actualizado_en: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
        nullable=False,
    )

    usuario: "UsuarioModel" = Relationship(back_populates="pedidos")
    estado: EstadoPedidoModel = Relationship(back_populates="pedidos")
    detalles: List["DetallePedidoModel"] = Relationship(back_populates="pedido")
    historial_estados: List["HistorialEstadoPedidoModel"] = Relationship(
        back_populates="pedido"
    )
    pagos: List["PagoModel"] = Relationship(back_populates="pedido")


class DetallePedidoModel(SQLModel, table=True):
    __tablename__ = "detalles_pedido"

    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key="pedidos.id", nullable=False)
    producto_id: int = Field(foreign_key="productos.id", nullable=False)
    producto_snapshot: Optional[dict] = Field(
        default=None, sa_column=Column(JSON, nullable=True)
    )
    cantidad: int = Field(nullable=False)
    precio_unitario: float = Field(sa_column=Column(Numeric(10, 2), nullable=False))
    personalizacion: Optional[list] = Field(
        default=None,
        sa_column=Column(ARRAY(INTEGER), nullable=True),
    )
    creado_en: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    pedido: PedidoModel = Relationship(back_populates="detalles")


class HistorialEstadoPedidoModel(SQLModel, table=True):
    __tablename__ = "historial_estados_pedido"

    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key="pedidos.id", nullable=False)
    estado_anterior_id: Optional[int] = Field(
        default=None, foreign_key="estados_pedido.id", nullable=True
    )
    estado_nuevo_id: int = Field(foreign_key="estados_pedido.id", nullable=False)
    cambiado_por_id: int = Field(foreign_key="usuarios.id", nullable=False)
    razon: Optional[str] = Field(default=None, nullable=True)
    creado_en: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    pedido: PedidoModel = Relationship(back_populates="historial_estados")


class PagoModel(SQLModel, table=True):
    __tablename__ = "pagos"

    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int = Field(
        foreign_key="pedidos.id", nullable=False, unique=True
    )
    forma_pago_id: int = Field(foreign_key="formas_pago.id", nullable=False)
    monto: float = Field(sa_column=Column(Numeric(10, 2), nullable=False))
    estado_pago: str = Field(nullable=False)
    mp_preference_id: Optional[str] = Field(default=None, nullable=True)
    mp_payment_id: Optional[str] = Field(default=None, nullable=True)
    mp_status: Optional[str] = Field(default=None, nullable=True)
    mp_status_detail: Optional[str] = Field(default=None, nullable=True)
    idempotency_key: str = Field(unique=True, nullable=False)
    creado_en: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    actualizado_en: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
        nullable=False,
    )

    pedido: PedidoModel = Relationship(back_populates="pagos")
    forma_pago: FormaPagoModel = Relationship(back_populates="pagos")
