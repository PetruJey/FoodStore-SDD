# EPIC 01 — Autenticacion y Autorizacion

## US-001: Registro de cliente

- **Titulo**: Registro de nuevo cliente
- **Historia**: Como **Cliente**, quiero registrarme en la plataforma con mi email y contrasena, para poder acceder a las funcionalidades de compra.
- **Prioridad**: Alta
- **Dependencias**: US-000a, US-000b, US-000d (backend configurado, BD con tablas y seed data, patrones base implementados)

**Criterios de Aceptacion**:
- [ ] GIVEN un usuario no registrado, WHEN completa el formulario con nombre, email y contrasena validos, THEN se crea la cuenta con rol CLIENT asignado automaticamente.
- [ ] GIVEN un email ya registrado, WHEN intenta registrarse con ese email, THEN el sistema muestra error "El email ya esta registrado".
- [ ] GIVEN una contrasena con menos de 8 caracteres, WHEN intenta registrarse, THEN el sistema rechaza el registro con mensaje de validacion.
- [ ] La contrasena se almacena hasheada con bcrypt (cost factor >= 10).
- [ ] Al registrarse exitosamente, se retorna un par de tokens (access + refresh).

**Reglas de Negocio**: RN-AU01, RN-AU07, RN-DA04.

**Notas Tecnicas**:
- Endpoint: `POST /api/auth/register`
- Hashing: bcrypt con salt automatico
- Rol CLIENT se asigna en la capa de servicio, no viene del request
- Validacion de email con regex RFC 5322 simplificado

## US-002: Login de usuario

- **Titulo**: Inicio de sesion
- **Historia**: Como **Cliente**, quiero iniciar sesion con mis credenciales, para acceder a mi cuenta y realizar compras.
- **Prioridad**: Alta
- **Dependencias**: US-001

**Criterios de Aceptacion**:
- [ ] GIVEN credenciales validas, WHEN el usuario envia email y contrasena, THEN recibe un access token (30 min) y un refresh token (7 dias).
- [ ] GIVEN credenciales invalidas, WHEN intenta loguearse, THEN recibe error 401 sin revelar si el email existe o no.
- [ ] GIVEN 5 intentos fallidos en 15 minutos desde la misma IP, WHEN intenta un 6to login, THEN recibe error 429 "Demasiados intentos, reintenta en X minutos".
- [ ] El access token contiene: userId, email, rol, exp.
- [ ] El refresh token se almacena de forma segura (httpOnly cookie o storage seguro).

**Reglas de Negocio**: RN-AU02, RN-AU06, RN-AU08, RN-DA04.

**Notas Tecnicas**:
- Endpoint: `POST /api/auth/login`
- JWT firmado con RS256 o HS256 segun config
- Rate limiting implementado con sliding window (Redis o in-memory)
- Respuesta no debe diferenciar "email no existe" de "contrasena incorrecta"

## US-003: Refresh de token

- **Titulo**: Renovacion automatica de sesion
- **Historia**: Como **Sistema**, quiero rotar los tokens de acceso usando el refresh token, para mantener la sesion del usuario activa de forma segura.
- **Prioridad**: Alta
- **Dependencias**: US-002

**Criterios de Aceptacion**:
- [ ] GIVEN un refresh token valido y no expirado, WHEN se envia al endpoint de refresh, THEN se genera un nuevo par access + refresh token y se invalida el refresh token anterior (rotacion).
- [ ] GIVEN un refresh token expirado, WHEN se envia al endpoint, THEN se retorna 401 y el usuario debe re-loguearse.
- [ ] GIVEN un refresh token ya utilizado (replay attack), WHEN se envia, THEN se invalidan TODOS los refresh tokens del usuario y se retorna 401.
- [ ] El nuevo refresh token tiene una nueva fecha de expiracion (7 dias desde la emision).

**Notas Tecnicas**:
- Endpoint: `POST /api/auth/refresh`
- Familia de tokens: cada refresh token tiene un `familyId` para detectar reuso
- Almacenamiento de refresh tokens en BD con flag `used`

## US-004: Logout

- **Titulo**: Cierre de sesion
- **Historia**: Como **Cliente**, quiero cerrar mi sesion, para proteger mi cuenta cuando dejo de usar la plataforma.
- **Prioridad**: Media
- **Dependencias**: US-002

**Criterios de Aceptacion**:
- [ ] GIVEN un usuario autenticado, WHEN solicita logout, THEN se invalida el refresh token actual.
- [ ] GIVEN un access token post-logout, WHEN se usa para una request, THEN sigue siendo valido hasta su expiracion natural (stateless).
- [ ] El cliente limpia los tokens del storage local.

**Notas Tecnicas**:
- Endpoint: `POST /api/auth/logout`
- Invalidar refresh token en BD (soft delete o flag)
- Frontend: limpiar Zustand auth store + localStorage

## US-005: Gestion de roles (RBAC)

- **Titulo**: Asignacion y verificacion de roles
- **Historia**: Como **Admin**, quiero asignar roles a los usuarios del sistema, para controlar el acceso a las distintas funcionalidades.
- **Prioridad**: Alta
- **Dependencias**: US-001

**Criterios de Aceptacion**:
- [ ] GIVEN un Admin autenticado, WHEN asigna un rol (ADMIN, STOCK, PEDIDOS, CLIENT) a un usuario, THEN el usuario obtiene los permisos correspondientes.
- [ ] GIVEN un usuario con rol CLIENT, WHEN intenta acceder a un endpoint de Admin, THEN recibe 403 Forbidden.
- [ ] Los 4 roles son: ADMIN, STOCK, PEDIDOS, CLIENT.
- [ ] Solo ADMIN puede modificar roles de otros usuarios.
- [ ] Un ADMIN no puede quitarse el rol ADMIN a si mismo si es el ultimo admin.

**Notas Tecnicas**:
- Endpoint: `PUT /api/admin/users/:id/role`
- Middleware de autorizacion: `@Roles('ADMIN')` o guard equivalente
- Decorador/middleware que extrae el rol del JWT y valida contra la ruta

## US-006: Proteccion de rutas por rol

- **Titulo**: Middleware de autorizacion por rol
- **Historia**: Como **Sistema**, quiero proteger cada endpoint segun el rol requerido, para garantizar que solo usuarios autorizados accedan a cada recurso.
- **Prioridad**: Alta
- **Dependencias**: US-005

**Criterios de Aceptacion**:
- [ ] GIVEN un request sin token, WHEN accede a una ruta protegida, THEN recibe 401.
- [ ] GIVEN un token valido con rol insuficiente, WHEN accede a una ruta restringida, THEN recibe 403.
- [ ] GIVEN un token expirado, WHEN accede a una ruta protegida, THEN recibe 401 con mensaje indicando expiracion.
- [ ] Las rutas publicas (catalogo, login, registro) no requieren autenticacion.

**Reglas de Negocio**: Mapeo de roles a rutas segun tabla de permisos.

**Notas Tecnicas**:
- Middleware/Guard global con lista blanca de rutas publicas
- Decorador de metadata para roles requeridos por endpoint
- Patron: extraer claims del JWT -> verificar rol contra metadata de la ruta

## US-073: Rate limiting en endpoints sensibles

- **Titulo**: Proteccion contra abuso en endpoints criticos
- **Historia**: Como **Sistema**, quiero limitar la tasa de requests en endpoints sensibles, para proteger el sistema contra ataques de fuerza bruta y abuso.
- **Prioridad**: Alta
- **Dependencias**: US-002

**Criterios de Aceptacion**:
- [ ] Login: maximo 5 intentos por IP en ventana de 15 minutos.
- [ ] Registro: maximo 3 registros por IP en ventana de 1 hora.
- [ ] Creacion de pedido: maximo 10 por usuario por hora.
- [ ] Al exceder el limite, respuesta 429 con header `Retry-After`.

**Notas Tecnicas**:
- Middleware de rate limiting con sliding window
- Almacenamiento: Redis (produccion) o Map in-memory (desarrollo)
- Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
