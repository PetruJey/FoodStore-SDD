from collections.abc import AsyncIterator
from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import async_session_factory
from core.repository import BaseRepository


class UnitOfWork:
    def __init__(self) -> None:
        self.session: AsyncSession | None = None
        self._repos: dict[str, BaseRepository] = {}

    async def __aenter__(self) -> "UnitOfWork":
        self.session = async_session_factory()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self.session is None:
            return
        try:
            if exc_type is None:
                await self.session.commit()
            else:
                await self.session.rollback()
        finally:
            await self.session.close()
            self.session = None
            self._repos.clear()

    def _get_repo(self, model_class: type, name: str) -> BaseRepository:
        if name not in self._repos:
            from sqlmodel import SQLModel

            if not issubclass(model_class, SQLModel):
                raise TypeError(f"{model_class.__name__} must be a SQLModel subclass")
            self._repos[name] = BaseRepository(model_class, self.session)
        return self._repos[name]

    @property
    def usuarios(self) -> BaseRepository:
        from app.models.identidad import UsuarioModel

        return self._get_repo(UsuarioModel, "usuarios")

    @property
    def auth(self) -> BaseRepository:
        from app.models.identidad import RefreshTokenModel

        return self._get_repo(RefreshTokenModel, "auth")

    @property
    def categorias(self) -> BaseRepository:
        from app.models.catalogo import CategoriaModel

        return self._get_repo(CategoriaModel, "categorias")

    @property
    def productos(self) -> BaseRepository:
        from app.models.catalogo import ProductoModel

        return self._get_repo(ProductoModel, "productos")

    @property
    def ingredientes(self) -> BaseRepository:
        from app.models.catalogo import IngredienteModel

        return self._get_repo(IngredienteModel, "ingredientes")

    @property
    def pedidos(self) -> BaseRepository:
        from app.models.ventas import PedidoModel

        return self._get_repo(PedidoModel, "pedidos")

    @property
    def pagos(self) -> BaseRepository:
        from app.models.ventas import PagoModel

        return self._get_repo(PagoModel, "pagos")

    @property
    def direcciones(self) -> BaseRepository:
        from app.models.identidad import DireccionEntregaModel

        return self._get_repo(DireccionEntregaModel, "direcciones")

    @property
    def admin(self) -> BaseRepository:
        from app.models.identidad import UsuarioModel

        return self._get_repo(UsuarioModel, "admin")


