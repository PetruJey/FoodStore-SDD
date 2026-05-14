from fastapi import APIRouter, Depends

from core.dependencies import require_role

router = APIRouter(prefix="/pagos", tags=["pagos"])


@router.get("/health")
async def health_check():
    # POST endpoint will require Depends(require_role(["CLIENT"])) when implemented; webhook stays public
    return {"status": "ok", "module": "pagos"}
