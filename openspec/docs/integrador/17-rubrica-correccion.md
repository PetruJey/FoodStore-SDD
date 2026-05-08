# 12. Rúbrica de Corrección — v5.0

Puntaje total: 200 puntos. Corrección escrita + video de demostración obligatorio.

| Criterio | Pts | Excelente | Bueno | Regular | Insuficiente |
|----------|-----|-----------|-------|---------|-------------|
| Backend — Estructura y Configuración | 10 | Capas router/service/uow/repository/model. Módulos por dominio. core/ separado. Alembic + seed. CORS + rate limiting. | Separación parcial. Seed incompleto. | Estructura plana o sin capas. | Sin estructura reconocible. |
| Backend — Modelo de Datos | 15 | SQLModel correcto, constraints, soft-delete, snapshot, entidades completas (Ingrediente, FormaPago, DireccionEntrega, RefreshToken, Pago). | Correctos, faltan algunas entidades. | Básicos sin patrones avanzados. | Incorrectos o incompletos. |
| Backend — Unit of Work y Repository | 15 | UoW completo con context manager, commit/rollback automático. BaseRepository[T] genérico. Ningún service hace session.commit(). | UoW presente pero incompleto. | Sin UoW, transacciones manuales. | Sin gestión de transacciones. |
| Backend — Capa de Servicio | 15 | FSM implementada. RN-01/02/03/05 validadas. Services stateless. Service recibe uow por parámetro. | Lógica presente pero algunas RN en routers. | Lógica básica sin validaciones. | Sin capa de servicio. |
| Backend — Controladores REST | 15 | Verbos HTTP correctos, rutas semánticas, status codes precisos (201/204/422/402), prefijo /api/v1. Schemas Pydantic separados Read/Create/Update. | Verbos y rutas correctas, algunos status codes incorrectos. | Verbos incorrectos o rutas no semánticas. | Sin convenciones REST. |
| Backend — MercadoPago | 15 | SDK Python configurado con idempotency_key UUID. Webhook /pagos/webhook que procesa topic=payment y avanza pedido. Tabla Pago completa. | SDK configurado, sin idempotency_key. | Integración parcial o hardcodeada. | Sin integración MP. |
| Frontend — Estructura y TypeScript | 10 | Feature-sliced: pages/features/components/hooks/store/api/types. Sin cross-imports. strict: true, no any. | Estructura presente, algunos módulos mezclados. | Estructura plana. | Sin estructura. |
| Frontend — Zustand | 10 | 4 stores implementados y tipados. persist correcto por store. Suscripción por slice. | 3 stores correctos. | Solo authStore y cartStore básicos. | Sin Zustand. |
| Frontend — TanStack Query | 15 | useQuery/useMutation para todo el fetch. queryKeys descriptivos. Invalidación tras mutaciones. Interceptor refresh 401 automático. | TanStack Query presente, invalidación parcial. | Fetch directo con useEffect. | Sin TanStack Query. |
| Frontend — Funcionalidades Cliente | 15 | Catálogo con debounce/filtros/paginación/skeleton. Carrito persist. Checkout con CardPayment de MP. Timeline con polling 30s. | Funcional con algunas carencias. | Lista sin filtros ni paginación. | Sin funcionalidades. |
| Frontend — Panel Admin | 15 | Dashboard KPIs + recharts. CRUD categorías/productos con relaciones. Gestión pedidos con FSM. Gestión stock. | CRUD funcional, falta alguna feature. | Solo visualización. | Sin panel admin. |
| UI/UX y Diseño | 10 | Sistema de diseño consistente. Mobile-first. Skeleton loaders, toasts, modales de confirmación, estados vacíos. | Diseño consistente con pequeñas inconsistencias. | Diseño básico sin sistema. | Sin diseño coherente. |
| Calidad de Código | 10 | snake_case/camelCase/PascalCase. Funciones < 50 líneas. SRP. Docstrings. JSDoc. README.md completo. | Nomenclatura correcta, algunas funciones largas. | Mezcla de convenciones. | Sin convenciones. |

**Escala de calificación:**

- 181-200 pts (90-100%) — EXCELENTE: Proyecto completo, profesional, con todas las capas y buenas prácticas.
- 141-180 pts (70-89%)  — BUENO: Proyecto funcional con pequeños ajustes o funcionalidades faltantes.
- 101-140 pts (50-69%)  — REGULAR: Proyecto básico con errores o funcionalidades incompletas.
- 0-100 pts  (0-49%)  — INSUFICIENTE: Proyecto incompleto, no funcional o no sigue la especificación.

**Bonus** +10 pts: Tests unitarios con pytest, cobertura > 60% (test_pedidos, test_pagos, test_auth).

**Bonus** +10 pts: Deploy funcional en Railway, Render o Fly.io con URL accesible.

⚠ **Penalización** -30%: El proyecto que no corra localmente siguiendo el README.
