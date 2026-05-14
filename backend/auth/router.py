from fastapi import APIRouter, Depends, Request, status
from slowapi import Limiter
from slowapi.util import get_remote_address

from auth.schemas import LoginRequest, RefreshRequest, RegisterRequest
from auth.service import AuthService
from core.dependencies import get_current_user
from core.uow import UnitOfWork

router = APIRouter(prefix="/auth", tags=["auth"])
limiter = Limiter(key_func=get_remote_address)


@router.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit("3/hour")
async def register(request: Request, body: RegisterRequest):
    uow = UnitOfWork()
    service = AuthService(uow)
    return await service.register(
        nombre=body.nombre,
        email=body.email,
        password=body.password,
    )


@router.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, body: LoginRequest):
    uow = UnitOfWork()
    service = AuthService(uow)
    return await service.login(email=body.email, password=body.password)


@router.post("/refresh")
@limiter.limit("10/minute")
async def refresh(request: Request, body: RefreshRequest):
    uow = UnitOfWork()
    service = AuthService(uow)
    return await service.refresh(refresh_token_str=body.refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: Request,
    body: RefreshRequest,
    current_user=Depends(get_current_user),
):
    uow = UnitOfWork()
    service = AuthService(uow)
    await service.logout(refresh_token_str=body.refresh_token)
