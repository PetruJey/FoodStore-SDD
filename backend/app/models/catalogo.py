from datetime import datetime
from typing import Optional, List

from sqlalchemy import CheckConstraint, Column, Numeric
from sqlmodel import Field, Relationship, SQLModel


class CategoriaModel(SQLModel, table=True):
    __tablename__ = "categorias"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(nullable=False)
    descripcion: Optional[str] = Field(default=None, nullable=True)
    padre_id: Optional[int] = Field(
        default=None, foreign_key="categorias.id", nullable=True
    )
    activo: bool = Field(default=True, nullable=False)
    creado_en: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    actualizado_en: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
        nullable=False,
    )
    eliminado_en: Optional[datetime] = Field(default=None, nullable=True)

    hijos: List["CategoriaModel"] = Relationship(
        back_populates="padre",
        sa_relationship_kwargs={"remote_side": "CategoriaModel.id"},
    )
    padre: Optional["CategoriaModel"] = Relationship(
        back_populates="hijos",
        sa_relationship_kwargs={"remote_side": "CategoriaModel.id"},
    )
    productos: List["ProductoCategoriaModel"] = Relationship(back_populates="categoria")


class ProductoModel(SQLModel, table=True):
    __tablename__ = "productos"
    __table_args__ = (
        CheckConstraint("stock >= 0", name="check_stock_non_negative"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(nullable=False)
    descripcion: Optional[str] = Field(default=None, nullable=True)
    precio: float = Field(sa_column=Column(Numeric(10, 2), nullable=False))
    stock: int = Field(default=0, nullable=False)
    imagen_url: Optional[str] = Field(default=None, nullable=True)
    activo: bool = Field(default=True, nullable=False)
    creado_en: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    actualizado_en: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
        nullable=False,
    )
    eliminado_en: Optional[datetime] = Field(default=None, nullable=True)

    categorias: List["ProductoCategoriaModel"] = Relationship(back_populates="producto")
    ingredientes: List["ProductoIngredienteModel"] = Relationship(
        back_populates="producto"
    )


class IngredienteModel(SQLModel, table=True):
    __tablename__ = "ingredientes"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(nullable=False)
    es_alergeno: bool = Field(default=False, nullable=False)
    creado_en: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    productos: List["ProductoIngredienteModel"] = Relationship(
        back_populates="ingrediente"
    )


class ProductoCategoriaModel(SQLModel, table=True):
    __tablename__ = "productos_categorias"

    producto_id: int = Field(foreign_key="productos.id", primary_key=True)
    categoria_id: int = Field(foreign_key="categorias.id", primary_key=True)

    producto: ProductoModel = Relationship(back_populates="categorias")
    categoria: CategoriaModel = Relationship(back_populates="productos")


class ProductoIngredienteModel(SQLModel, table=True):
    __tablename__ = "productos_ingredientes"

    producto_id: int = Field(foreign_key="productos.id", primary_key=True)
    ingrediente_id: int = Field(foreign_key="ingredientes.id", primary_key=True)

    producto: ProductoModel = Relationship(back_populates="ingredientes")
    ingrediente: IngredienteModel = Relationship(back_populates="productos")
