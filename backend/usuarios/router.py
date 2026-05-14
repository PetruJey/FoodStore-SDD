from fastapi import APIRouter, Depends

from core.dependencies import require_role

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("/health")
async def health_check(current_user=Depends(require_role(["ADMIN"]))):
    return {"status": "ok", "module": "usuarios"}
