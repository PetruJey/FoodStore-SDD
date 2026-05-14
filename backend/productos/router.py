from fastapi import APIRouter, Depends

from core.dependencies import require_role

router = APIRouter(prefix="/productos", tags=["productos"])


@router.get("/health")
async def health_check():
    # POST/PUT/DELETE will require require_role(["ADMIN", "STOCK"]) when implemented
    return {"status": "ok", "module": "productos"}
