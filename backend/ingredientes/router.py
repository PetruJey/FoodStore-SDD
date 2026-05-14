from fastapi import APIRouter

router = APIRouter(prefix="/ingredientes", tags=["ingredientes"])


@router.get("/health")
async def health_check():
    return {"status": "ok", "module": "ingredientes"}
