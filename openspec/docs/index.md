# 📚 Food Store — Documentación Modular

Este directorio contiene la documentación completa del sistema Food Store, modularizada en archivos Markdown independientes para que los changes de OPSX puedan referenciar secciones específicas sin leer archivos monolíticos.

> **⚠️ Entry point oficial**: Este archivo es la puerta de entrada a la documentación del sistema. Los agentes IA deben leer **este índice** (`openspec/docs/index.md`) y navegar al archivo específico que necesiten, en lugar de leer los archivos monolíticos de `docs/`.
>
> **Origen**: Los archivos fuente originales están en `docs/` (`Descripcion.txt`, `Historias_de_usuario.txt`, `Integrador.txt`).
> Los archivos en `openspec/docs/` son una división uno-a-uno del contenido original, sin modificaciones.

---

## 📖 Descripción del Sistema

> Fuente: `docs/Descripcion.txt`

| Archivo | Sección |
|---------|---------|
| `descripcion/01-vision-general.md` | 1. Visión General del Sistema |
| `descripcion/02-stack-tecnologico.md` | 2. Stack Tecnológico |
| `descripcion/03-arquitectura-backend.md` | 3. Arquitectura — Backend |
| `descripcion/04-arquitectura-frontend.md` | 3. Arquitectura — Frontend |
| `descripcion/05-modelo-datos-identidad.md` | 4. Modelo de Datos — Dominio 1 (Identidad) |
| `descripcion/06-modelo-datos-catalogo.md` | 4. Modelo de Datos — Dominio 2 (Catálogo) |
| `descripcion/07-modelo-datos-ventas.md` | 4. Modelo de Datos — Dominio 3 (Ventas) |
| `descripcion/08-maquina-estados.md` | 5. Máquina de Estados del Pedido |
| `descripcion/09-autenticacion-jwt.md` | 6. Autenticación — Flujo JWT |
| `descripcion/10-rbac.md` | 6. Autorización — RBAC + Rate Limiting |
| `descripcion/11-api-rest.md` | 7. API REST |
| `descripcion/12-schemas-pydantic.md` | 8. Schemas Pydantic v2 |
| `descripcion/13-unit-of-work.md` | 9. Unit of Work |
| `descripcion/14-integracion-mercadopago.md` | 10. Integración MercadoPago |

---

## 👤 Historias de Usuario

> Fuente: `docs/Historias_de_usuario.txt`

### Reglas de Negocio

| Archivo | Sección |
|---------|---------|
| `historias/01-actores.md` | Actores del Sistema |
| `historias/02-reglas-autenticacion.md` | RN — Autenticación y Seguridad (RN-AU01 a RN-AU10) |
| `historias/03-reglas-autorizacion.md` | RN — Autorización/RBAC (RN-RB01 a RN-RB10) |
| `historias/04-reglas-catalogo.md` | RN — Catálogo (RN-CA01 a RN-CA10) |
| `historias/05-reglas-direcciones.md` | RN — Direcciones de Entrega (RN-DI01 a RN-DI03) |
| `historias/06-reglas-carrito.md` | RN — Carrito de Compras (RN-CR01 a RN-CR05) |
| `historias/07-reglas-pedidos-creacion.md` | RN — Pedidos: Creación (RN-PE01 a RN-PE08) |
| `historias/08-reglas-fsm.md` | RN — Pedidos: FSM (RN-FS01 a RN-FS09) |
| `historias/09-reglas-pagos.md` | RN — Pagos MercadoPago (RN-PA01 a RN-PA09) |
| `historias/10-reglas-datos.md` | RN — Datos e Integridad (RN-DA01 a RN-DA08) |

### Épicas e Historias de Usuario

| Archivo | Épica | Historias |
|---------|-------|-----------|
| `historias/11-epic00-infraestructura.md` | 00 — Infraestructura y Setup | US-000 a US-000e, US-068, US-074 |
| `historias/12-epic01-autenticacion.md` | 01 — Autenticación y Autorización | US-001 a US-006, US-073 |
| `historias/13-epic02-navegacion.md` | 02 — Navegación y Layout Base | US-075, US-076, US-066, US-067 |
| `historias/14-epic03-categorias.md` | 03 — Gestión de Categorías | US-007 a US-010 |
| `historias/15-epic04-ingredientes.md` | 04 — Ingredientes y Alérgenos | US-011 a US-014 |
| `historias/16-epic05-productos.md` | 05 — Productos y Catálogo | US-015 a US-023 |
| `historias/17-epic06-perfil.md` | 06 — Perfil del Cliente | US-061, US-062, US-063 |
| `historias/18-epic07-direcciones.md` | 07 — Direcciones de Entrega | US-024 a US-028 |
| `historias/19-epic08-carrito.md` | 08 — Carrito de Compras | US-029 a US-034 |
| `historias/20-epic09-precheckout.md` | 09 — Validaciones Pre-Checkout | US-069, US-070 |
| `historias/21-epic10-creacion-pedidos.md` | 10 — Creación de Pedidos | US-035 a US-038 |
| `historias/22-epic11-pagos.md` | 11 — Pagos con MercadoPago | US-045 a US-048 |
| `historias/23-epic12-fsm.md` | 12 — FSM de Pedidos | US-039 a US-044 |
| `historias/24-epic13-visualizacion.md` | 13 — Visualización de Pedidos | US-049 a US-052 |
| `historias/25-epic14-notificaciones.md` | 14 — Notificaciones y Feedback UX | US-071, US-072 |
| `historias/26-epic15-admin-usuarios.md` | 15 — Administración de Usuarios | US-053 a US-055 |
| `historias/27-epic16-catalogo-admin.md` | 16 — Catálogo Admin | US-064, US-065 |
| `historias/28-epic17-metricas.md` | 17 — Métricas y Dashboard | US-056 a US-059 |
| `historias/29-epic18-configuracion.md` | 18 — Configuración del Sistema | US-060 |
| `historias/30-resumen-historias.md` | Resumen + Plan de Sprints | — |

---

## 🏗️ Especificación Técnica (Integrador)

> Fuente: `docs/Integrador.txt`

| Archivo | Sección |
|---------|---------|
| `integrador/01-vision-general.md` | 1. Visión General del Sistema |
| `integrador/02-arquitectura-backend.md` | 2.1 Capas del Backend |
| `integrador/03-arquitectura-frontend.md` | 2.2 Frontend — Feature-Sliced Design |
| `integrador/04-modulos-backend.md` | 2.3 Módulos Backend (Feature-First) |
| `integrador/05-modelo-datos-identidad.md` | 3.1 Modelo de Datos — Dominio 1 (Identidad) |
| `integrador/06-modelo-datos-catalogo.md` | 3.2 Modelo de Datos — Dominio 2 (Catálogo) |
| `integrador/07-modelo-datos-ventas.md` | 3.3 Modelo de Datos — Dominio 3 (Ventas) |
| `integrador/08-maquina-estados.md` | 3.4 Máquina de Estados del Pedido |
| `integrador/09-autenticacion.md` | 4. Autenticación y Autorización |
| `integrador/10-api-rest.md` | 5. Especificación de API REST |
| `integrador/11-schemas-pydantic.md` | 6. Schemas Pydantic v2 |
| `integrador/12-unit-of-work.md` | 7. Patrón Unit of Work |
| `integrador/13-integracion-mercadopago.md` | 8. Integración MercadoPago |
| `integrador/14-gestion-estado-zustand.md` | 9. Gestión de Estado con Zustand |
| `integrador/15-configuracion-setup.md` | 10. Configuración y Setup |
| `integrador/16-patrones-arquitectonicos.md` | 11. Patrones Aplicados |
| `integrador/17-rubrica-correccion.md` | 12. Rúbrica de Corrección |
| `integrador/18-entrega-checklist.md` | 13. Entrega del Proyecto + Apéndice |

---

**Total: 62 archivos** organizados en 3 categorías, preservando el contenido original de los 3 archivos fuente.
