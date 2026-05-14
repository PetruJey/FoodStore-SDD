from fastapi import APIRouter

router = APIRouter(prefix="/refreshtokens", tags=["refreshtokens"])


@router.get("/health")
async def health_check():
    return {"status": "ok", "module": "refreshtokens"}
