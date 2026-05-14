from fastapi import APIRouter

router = APIRouter(prefix="/pagos", tags=["pagos"])


@router.get("/health")
async def health_check():
    return {"status": "ok", "module": "pagos"}
