from fastapi import APIRouter, Depends, Request
from sqlmodel import Session

from app.core.database import get_session
from app.core.limiter import limiter
from app.db.models import UsuarioModel
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.schemas import (
    LoginRequest,
    LogoutRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
)
from app.modules.auth import service as auth_service

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_session)):
    return auth_service.register(db, data)


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/15minutes")
def login(
    request: Request,
    data: LoginRequest,
    db: Session = Depends(get_session),
):
    return auth_service.login(db, data, request)


@router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshRequest, db: Session = Depends(get_session)):
    return auth_service.refresh_token(db, data.refresh_token)


@router.post("/logout")
def logout(
    data: LogoutRequest,
    current_user: UsuarioModel = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    auth_service.logout(db, data.refresh_token)
    return {"message": "Sesión cerrada exitosamente"}
