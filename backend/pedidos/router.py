from fastapi import APIRouter

router = APIRouter(prefix="/pedidos", tags=["pedidos"])


@router.get("/health")
async def health_check():
    return {"status": "ok", "module": "pedidos"}
