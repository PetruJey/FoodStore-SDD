from fastapi import APIRouter, Depends

from core.dependencies import require_role

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/health")
async def health_check(current_user=Depends(require_role(["ADMIN"]))):
    # RN-RB08: Only ADMIN can cancel orders in EN_PREPARACION state
    return {"status": "ok", "module": "admin"}
