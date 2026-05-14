from fastapi import APIRouter, Depends

from core.dependencies import require_role

router = APIRouter(prefix="/direcciones", tags=["direcciones"])


@router.get("/health")
async def health_check(current_user=Depends(require_role(["CLIENT"]))):
    return {"status": "ok", "module": "direcciones"}
