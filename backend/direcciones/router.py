from fastapi import APIRouter

router = APIRouter(prefix="/direcciones", tags=["direcciones"])


@router.get("/health")
async def health_check():
    return {"status": "ok", "module": "direcciones"}
