from fastapi import APIRouter

router = APIRouter(prefix="/categorias", tags=["categorias"])


@router.get("/health")
async def health_check():
    return {"status": "ok", "module": "categorias"}
