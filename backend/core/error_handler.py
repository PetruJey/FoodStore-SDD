import logging
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from core.exceptions import AppException

logger = logging.getLogger("foodstore")


def _problem_response(
    request: Request,
    status: int,
    title: str,
    detail: str,
    errors: list[dict[str, str]] | None = None,
) -> JSONResponse:
    body: dict = {
        "type": "about:blank",
        "title": title,
        "status": status,
        "detail": detail,
        "instance": str(request.url),
    }
    if errors:
        body["errors"] = errors
    return JSONResponse(status_code=status, content=body)


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return _problem_response(
            request=request,
            status=exc.status_code,
            title=exc.detail,
            detail=exc.detail,
            errors=exc.errors or None,
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return _problem_response(
            request=request,
            status=exc.status_code,
            title=exc.detail or "Error HTTP",
            detail=exc.detail or "Error HTTP",
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        error_id = uuid4().hex[:8]
        logger.exception(
            "Error interno del servidor [%s]: %s", error_id, str(exc)
        )
        return _problem_response(
            request=request,
            status=500,
            title="Error interno del servidor",
            detail=(
                "Ocurrió un error inesperado. "
                f"ID de referencia: {error_id}"
            ),
        )
