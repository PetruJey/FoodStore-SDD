# 13. Entrega del Proyecto

## 13.1 Checklist de Entrega

| Ítem | Descripción | Estado |
|------|-------------|--------|
| CE-01 | Link a repositorio GitHub público en la entrega | ☐ Pendiente |
| CE-02 | README.md con instrucciones de setup funcionando en máquina limpia | ☐ Pendiente |
| CE-03 | .env.example completo con variables de MercadoPago documentadas | ☐ Pendiente |
| CE-04 | alembic upgrade head sin errores | ☐ Pendiente |
| CE-05 | python -m app.db.seed ejecuta correctamente y carga datos iniciales | ☐ Pendiente |
| CE-06 | npm install + npm run dev sin errores | ☐ Pendiente |
| CE-07 | pip install -r requirements.txt + uvicorn app.main:app sin errores | ☐ Pendiente |
| CE-08 | Swagger UI (/docs) accesible con todos los endpoints documentados | ☐ Pendiente |
| CE-09 | Pago de prueba con tarjeta sandbox MP funciona end-to-end | ☐ Pendiente |
| CE-10 | Unit of Work correctamente implementado (ningún service.session.commit() directo) | ☐ Pendiente |
| CE-11 | 4 Zustand stores implementados, tipados y con persist correcto | ☐ Pendiente |
| CE-12 | Screenshots de al menos 10 pantallas distintas | ☐ Pendiente |
| CE-13 | Link a video demostración (5-10 min) en README | ☐ Pendiente |
| CE-14 | Repositorio público verificado con sesión cerrada | ☐ Pendiente |

# Apéndice — Referencias y Recursos

| Tecnología | URL |
|-----------|-----|
| FastAPI | https://fastapi.tiangolo.com |
| SQLModel | https://sqlmodel.tiangolo.com |
| Pydantic v2 | https://docs.pydantic.dev |
| Alembic | https://alembic.sqlalchemy.org |
| TanStack Query v5 | https://tanstack.com/query |
| TanStack Form | https://tanstack.com/form |
| Zustand | https://zustand-demo.pmnd.rs |
| Tailwind CSS | https://tailwindcss.com/docs |
| recharts | https://recharts.org |
| slowapi — rate limiting FastAPI | https://github.com/laurentS/slowapi |
| MercadoPago Developers (AR) | https://www.mercadopago.com.ar/developers/es |
| MercadoPago SDK Python | https://github.com/mercadopago/sdk-python |
| MercadoPago SDK React | https://github.com/mercadopago/sdk-react |

— Fin de la Especificación Técnica · Food Store v5.0 — SDD · Feature-First —
