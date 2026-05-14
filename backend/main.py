from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from core.config import get_settings
from core.error_handler import register_error_handlers

settings = get_settings()

limiter = Limiter(key_func=get_remote_address, default_limits=["5/15minute"])

app = FastAPI(
    title="Food Store API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

register_error_handlers(app)

from admin.rbac_router import router as rbac_router
from admin.router import router as admin_router
from auth.router import router as auth_router
from categorias.router import router as categorias_router
from direcciones.router import router as direcciones_router
from ingredientes.router import router as ingredientes_router
from pagos.router import router as pagos_router
from pedidos.router import router as pedidos_router
from productos.router import router as productos_router
from refreshtokens.router import router as refreshtokens_router
from usuarios.router import router as usuarios_router

API_PREFIX = "/api/v1"

app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(usuarios_router, prefix=API_PREFIX)
app.include_router(productos_router, prefix=API_PREFIX)
app.include_router(categorias_router, prefix=API_PREFIX)
app.include_router(ingredientes_router, prefix=API_PREFIX)
app.include_router(pedidos_router, prefix=API_PREFIX)
app.include_router(pagos_router, prefix=API_PREFIX)
app.include_router(direcciones_router, prefix=API_PREFIX)
app.include_router(admin_router, prefix=API_PREFIX)
app.include_router(rbac_router, prefix=API_PREFIX)
app.include_router(refreshtokens_router, prefix=API_PREFIX)


@app.get("/")
async def root():
    return {
        "message": "Food Store API",
        "version": "0.1.0",
        "docs": "/docs",
    }
