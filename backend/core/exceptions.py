from fastapi import HTTPException, status


class AppException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str = "",
        headers: dict[str, str] | None = None,
        errors: list[dict[str, str]] | None = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.errors = errors or []


class ValidationError(AppException):
    def __init__(
        self,
        detail: str = "Error de validación",
        errors: list[dict[str, str]] | None = None,
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            errors=errors,
        )


class UnauthorizedError(AppException):
    def __init__(self, detail: str = "No autorizado"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class ForbiddenError(AppException):
    def __init__(self, detail: str = "Acceso denegado"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class NotFoundError(AppException):
    def __init__(self, detail: str = "Recurso no encontrado"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )
