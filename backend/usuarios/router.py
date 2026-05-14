from fastapi import APIRouter

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("/health")
async def health_check():
    return {"status": "ok", "module": "usuarios"}
