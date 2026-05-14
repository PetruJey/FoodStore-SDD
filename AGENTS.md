# AGENTS.md — Instrucciones para Agentes IA

> ⚡ Optimizado para inicio de sesión. La documentación de referencia está en `AGENTS-REFERENCIA.md` — cargala on-demand cuando necesités detalles de stack, arquitectura, modelo de datos, FSM, etc.

---

## 📚 Documentación del Sistema

Antes de proponer, diseñar o implementar cualquier cambio, leé la documentación modular desde `openspec/docs/index.md`:

1. Abrí `openspec/docs/index.md` — es el **mapa completo** de toda la documentación
2. Desde ahí navegá al archivo específico (descripción, historias, integrador)
3. **No leas los archivos monolíticos** `docs/Descripcion.txt`, `docs/Integrador.txt` ni `docs/Historias_de_usuario.txt`

Además, **`docs/CHANGES.md`** contiene el mapa completo de épicas con versiones, dependencias y palabras clave para `/opsx:propose`. Consultalo antes de empezar cualquier change.

---

## Visión General del Proyecto

**Food Store** es un sistema de e-commerce para productos alimenticios.

- **5 actores**: Cliente, Admin, Gestor de Stock, Gestor de Pedidos, Sistema
- **Funcionalidades**: catálogo, carrito, pedidos con FSM de 6 estados, pagos con MercadoPago, panel de admin
- **Metodología**: Spec-Driven Development (SDD) con cambios atómicos
- **77 historias de usuario** (US-000 a US-076)

---

## Convenciones de Código

### Backend

| Convención | Padrón |
|-----------|--------|
| Archivos | snake_case: `productos.py`, `unit_of_work.py` |
| Clases | PascalCase: `class ProductoService` |
| Funciones | snake_case: `def get_by_id` |
| Modelos SQLModel | PascalCase + sufijo `Model`: `ProductoModel` |
| Schemas Pydantic | PascalCase + sufijo `Request/Response`: `ProductoCreate`, `ProductoRead` |
| Rutas API | prefijo `/api/v1`, plural: `/productos`, `/pedidos` |
| HTTP verbs | GET (listar), GET /{id} (detalle), POST (crear), PUT (actualizar), PATCH (parcial), DELETE (borrar) |
| Códigos HTTP | 200, 201, 204, 400, 401, 403, 404, 422, 429, 500 |

### Frontend

| Convención | Padrón |
|-----------|--------|
| Archivos | kebab-case: `product-card.tsx` |
| Componentes | PascalCase: `ProductoCard` |
| Hooks | camelCase con prefijo `use`: `useProductos` |
| Stores Zustand | camelCase: `authStore`, `cartStore` |
| Rutas | kebab-case: `/productos`, `/mi-carrito` |
| Estilos | Tailwind utility classes en el markup |

### Git

- Commits: [Conventional Commits](https://conventionalcommits.org)
- Estructura: `tipo(modulo): descripción`
- Tipos: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`

---

## Reglas de Negocio Clave

### Autenticación
- RN-AU01: Contraseña hasheada con bcrypt (cost >= 10)
- RN-AU02: Access token 30 min, refresh 7 días
- RN-AU04: Rotación de refresh token al usar
- RN-AU08: No diferenciar "email no existe" de "contraseña incorrecta"

### Catálogo
- RN-CA01: Categorías jerárquicas con CTE recursivo
- RN-CA02: No permitir ciclos en jerarquía
- RN-CA03: No eliminar categoría con productos activos
- RN-CA05: Stock >= 0, nunca negativo

### Pedidos
- RN-PE01: Creación ATÓMICA (Unit of Work)
- RN-PE02: Snapshot de precios al crear
- RN-PE03: Snapshot de dirección al crear
- RN-PE04: Validar stock DENTRO de la transacción

### Pagos
- RN-PA01: Tokenización en browser (PCI DSS SAQ-A)
- RN-PA02: Idempotency key para evitar cobros duplicados
- RN-PA05: Pago approved → transición automática PENDIENTE → CONFIRMADO

### Datos
- RN-DA01: Campos de auditoría (creado_en, actualizado_en)
- RN-DA06: Snapshots inmutables preservan historial
- RN-DA05: HistorialEstadoPedido append-only (nunca UPDATE/DELETE)

---

## Errores Frecuentes (evitar)

| Error | Por qué es un problema |
|-------|---------------------|
| Login que diferencia "email no existe" | Información que revela cuentas válidas |
| Guardar precios sin snapshots | Cambios afectan pedidos históricos |
| Stock decrement fuera de transacción | Race conditions, inventario inconsistente |
| HistorialEstadoPedido con UPDATE | Pierde auditoría |
| Tokens en localStorage (sin httpOnly) | XSS expone credenciales |
| Mezclar Zustand con TanStack Query | Duplicación y desincronización de estado |
| Queries concatenadas (no parametrizadas) | SQL injection |
| Commits masivos | Imposible de revisar, revertir |
| Implementar sin proposal | Sin trazabilidad, sin diseño |

---

## Referencia rápida del proyecto

Para el detalle completo de cada tema, cargá `AGENTS-REFERENCIA.md`:

| Tema | Dónde está el detalle |
|------|----------------------|
| Stack Tecnológico | `AGENTS-REFERENCIA.md` — sección Stack |
| Arquitectura (capas backend + FSD frontend) | `AGENTS-REFERENCIA.md` — sección Arquitectura |
| Modelo de Datos (3 dominios) | `AGENTS-REFERENCIA.md` — sección Modelo de Datos |
| Máquina de Estados del Pedido (FSM) | `AGENTS-REFERENCIA.md` — sección FSM |
| Autenticación JWT + RBAC | `AGENTS-REFERENCIA.md` — sección Auth |
| Estructura de Archivos (backend + frontend) | `AGENTS-REFERENCIA.md` — sección Estructura |
| Integración MercadoPago | `AGENTS-REFERENCIA.md` — sección MercadoPago |
| Gemas del Proyecto | `AGENTS-REFERENCIA.md` — sección Gemas |
| Variables de Entorno | `AGENTS-REFERENCIA.md` — sección Env Vars |
| Recursos + Glosario | `AGENTS-REFERENCIA.md` — sección Recursos |

---

*Editá `AGENTS-REFERENCIA.md` para ver el detalle completo del proyecto.*
