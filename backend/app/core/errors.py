from typing import Any, Optional

from fastapi import Request
from fastapi.responses import JSONResponse


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


def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    status_map = {
        NotFoundError: 404,
        ConflictError: 409,
        UnauthorizedError: 401,
        ForbiddenError: 403,
        BadRequestError: 400,
    }

    status_code = 500
    for err_cls, code in status_map.items():
        if isinstance(exc, err_cls):
            status_code = code
            break

    problem = {
        "type": f"https://httpstatuses.com/{status_code}",
        "title": exc.message,
        "status": status_code,
        "detail": exc.detail,
        "instance": str(request.url),
    }

    return JSONResponse(content=problem, status_code=status_code)
