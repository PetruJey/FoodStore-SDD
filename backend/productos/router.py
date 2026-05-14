from fastapi import APIRouter

router = APIRouter(prefix="/productos", tags=["productos"])


@router.get("/health")
async def health_check():
    return {"status": "ok", "module": "productos"}
