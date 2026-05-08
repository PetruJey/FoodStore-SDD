# 1. Visión General del Sistema

🍔 FOOD STORE
Sistema de Gestión de Pedidos de Comida

Especificación Técnica del Sistema
Versión 5.0  ·  Spec-Driven Development (SDD)  ·  Feature-First

| Campo | Valor |
|-------|-------|
| Materia |  |
| Carrera |  |
| Modalidad | Trabajo Práctico Integrador (TPI) |
| Stack | React + TypeScript + FastAPI + PostgreSQL |
| Metodología | Spec-Driven Development (SDD) |
| Versión doc. | 5.0 — ERD v5 + Arquitectura SDD + Diagramas + Feature-First |

Food Store es una aplicación web full-stack para la gestión integral de un negocio de comidas. Permite a los clientes explorar el catálogo, agregar productos al carrito, realizar pedidos con pago integrado vía MercadoPago y hacer seguimiento en tiempo real del estado de su pedido. Los administradores gestionan el catálogo, el stock, los pedidos y los usuarios desde un panel centralizado.

## 1.1 Objetivos del Sistema

| # | Actor | Objetivo principal |
|---|-------|-------------------|
| OBJ-01 | Cliente | Navegar el catálogo, gestionar carrito, pagar con MercadoPago y rastrear pedidos con trazabilidad completa |
| OBJ-02 | Administrador | Gestionar categorías, productos, stock y ciclo de vida de pedidos desde el panel |
| OBJ-03 | Gestor de Stock | Controlar disponibilidad y cantidad de stock de productos |
| OBJ-04 | Gestor de Pedidos | Avanzar el estado de los pedidos según la máquina de estados definida |
| OBJ-05 | Sistema | Garantizar trazabilidad completa de transiciones de estado mediante audit trail append-only |
| OBJ-06 | Sistema | Procesar y registrar pagos a través de la pasarela MercadoPago de forma atómica |

## 1.2 Alcance v5.0

- Autenticación y autorización con JWT y RBAC (4 roles) + invalidación de refresh token en base de datos
- Catálogo de productos con categorías jerárquicas e ingredientes con campo es_alergeno
- Carrito de compras con persistencia mediante Zustand + localStorage
- Gestión de pedidos con máquina de estados de 6 estados y audit trail append-only
- Pasarela de pagos MercadoPago Checkout API: tarjeta de crédito/débito, Rapipago, Pago Fácil
- Notificaciones webhook IPN de MercadoPago para confirmación automática de pagos
- Módulo DireccionEntrega: CRUD completo con dirección principal por usuario
- Panel de administración: dashboard con recharts, CRUD de entidades, gestión de pedidos y stock
- Rate limiting con slowapi: máximo 5 intentos fallidos por IP en 15 minutos en el login
- CORS configurado correctamente con CORSMiddleware para la separación frontend/backend
- Seed data obligatorio: roles, estados de pedido, formas de pago y usuario administrador
- API REST documentada con FastAPI/OpenAPI — accesible en /docs y /redoc

## 1.3 Stack Tecnológico

| Capa | Tecnología | Versión | Rol en el sistema |
|------|-----------|---------|-------------------|
| Frontend | React + TypeScript | 18.x + 5.x | UI, enrutamiento, componentes |
| Frontend | Vite | 5.x | Build tool y dev server |
| Frontend | Tailwind CSS | 3.x | Estilos utility-first |
| Frontend | TanStack Query | 5.x | Fetching, caché y sincronización de datos del servidor |
| Frontend | TanStack Form | 0.x | Gestión de formularios con validación |
| Frontend | Zustand | 4.x | Estado global del cliente (carrito, sesión, pagos, UI) |
| Frontend | Axios | 1.x | Cliente HTTP con interceptors JWT |
| Frontend | recharts | 2.x | Gráficos del dashboard de administración |
| Frontend | @mercadopago/sdk-react | — | SDK oficial MercadoPago para tokenización PCI-compliant |
| Backend | FastAPI | 0.111+ | Framework REST + generación automática OpenAPI |
| Backend | SQLModel | 0.0.19+ | ORM + schemas Pydantic integrados |
| Backend | PostgreSQL | 15+ | Base de datos relacional |
| Backend | Alembic | 1.13+ | Migraciones versionadas de base de datos |
| Backend | Passlib (bcrypt) | — | Hashing de contraseñas (cost factor ≥ 12) |
| Backend | mercadopago | 2.3.0+ | SDK oficial MercadoPago Python |
| Backend | slowapi | 0.1.9+ | Rate limiting por IP en endpoints críticos |
