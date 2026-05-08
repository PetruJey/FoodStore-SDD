# 2. Arquitectura del Sistema

## 2.1 Capas del Backend — Flujo de Dependencias

El backend aplica una arquitectura de capas con módulos por feature. El patrón Unit of Work (UoW) se ubica entre la capa de servicio y los repositorios, garantizando atomicidad transaccional. El flujo de dependencias es unidireccional y no puede invertirse.

[DIAGRAMA: Arquitectura Backend - Capas y Flujo de Dependencias] Muestra cinco capas del backend conectadas con flechas unidireccionales (Router a Service a UoW a Repository a Model). (1) Router/router.py: parsea requests HTTP, valida schemas Pydantic, delega al Service; no contiene logica de negocio. Conoce a: Service. (2) Service/service.py: logica de negocio stateless, orquesta operaciones via UoW, lanza HTTPException; no hace commit/rollback. Conoce a: UoW. (3) Unit of Work/core/uow.py: gestiona la transaccion, abre sesion de BD, provee acceso a repositorios, hace commit() automatico o rollback() en error. Conoce a: Repository, Session. (4) Repository/repository.py: acceso a BD sin logica de negocio, hereda de BaseRepository[T] generico, recibe sesion del UoW por inyeccion. Conoce a: Model, Session. (5) Model/model.py: tablas SQLModel y relaciones, sin imports de capas superiores. Conoce a: Ninguna.

Figura 1 — Capas del backend y flujo de dependencias unidireccional

Regla de oro — flujo de imports:

```
Router → Service → UoW → Repository → Model
```

Ninguna capa puede importar de la capa superior.
Un Model nunca importa de un Service. Un Repository nunca importa de un Router.

| Capa | Archivo de referencia | Responsabilidad | Conoce a |
|------|----------------------|----------------|----------|
| Router | router.py | HTTP puro: parsear request, validar schema Pydantic, delegar al Service, serializar response con response_model. No contiene lógica de negocio. | Service |
| Service | service.py | Lógica de negocio: stateless, orquesta operaciones sobre los repositorios a través del UoW. Lanza HTTPException. No hace commit/rollback directamente. | UoW |
| Unit of Work | core/uow.py | Gestión de transacción: abre la sesión de BD, provee acceso a todos los repositorios, hace commit() automático al salir sin excepciones o rollback() si ocurre error. | Repository, Session |
| Repository | repository.py | Acceso a BD: queries sin lógica de negocio. Hereda de BaseRepository[T] genérico. Recibe la sesión del UoW por inyección. | Model, Session |
| Model | model.py | SQLModel tables + relaciones. Sin imports de capas superiores. Define la estructura de la base de datos. | Ninguna |
