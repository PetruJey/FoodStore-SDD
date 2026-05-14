from fastapi import APIRouter, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from core.dependencies import require_role
from core.security import get_user_key

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/pedidos", tags=["pedidos"])


@router.get("/health")
@limiter.limit("10/hour", key_func=get_user_key)
async def health_check(request: Request, current_user=Depends(require_role(["ADMIN", "PEDIDOS"]))):
    # 429 responses include: Retry-After, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset
    return {"status": "ok", "module": "pedidos"}
