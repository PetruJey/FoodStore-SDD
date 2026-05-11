from typing import Any, Optional


class AppError(Exception):
    def __init__(self, message: str, detail: Optional[Any] = None):
        self.message = message
        self.detail = detail
        super().__init__(self.message)


class NotFoundError(AppError):
    def __init__(self, message: str = "Recurso no encontrado", entity: Optional[str] = None):
        detail = {"entity": entity} if entity else None
        super().__init__(message=message, detail=detail)


class ConflictError(AppError):
    def __init__(self, message: str = "Conflicto", detail: Optional[Any] = None):
        super().__init__(message=message, detail=detail)


class UnauthorizedError(AppError):
    def __init__(self, message: str = "No autorizado"):
        super().__init__(message=message)


class ForbiddenError(AppError):
    def __init__(self, message: str = "Prohibido"):
        super().__init__(message=message)


class BadRequestError(AppError):
    def __init__(self, message: str = "Solicitud inválida", detail: Optional[Any] = None):
        super().__init__(message=message, detail=detail)
