# EPIC 02 — Navegacion y Layout Base

## US-075: Navegacion por rol

- **Titulo**: Menu adaptado al rol del usuario
- **Historia**: Como **usuario del sistema**, quiero ver solo las opciones de menu correspondientes a mi rol, para tener una interfaz limpia y enfocada en mis tareas.
- **Prioridad**: Alta
- **Dependencias**: US-006

**Criterios de Aceptacion**:
- [ ] GIVEN un usuario con rol CLIENT, WHEN ve el menu, THEN ve: Catalogo, Mi Carrito, Mis Pedidos, Mi Perfil, Mis Direcciones.
- [ ] GIVEN un usuario con rol STOCK, WHEN ve el menu, THEN ve: Productos, Categorias, Ingredientes, Stock.
- [ ] GIVEN un usuario con rol PEDIDOS, WHEN ve el menu, THEN ve: Panel de Pedidos.
- [ ] GIVEN un usuario con rol ADMIN, WHEN ve el menu, THEN ve: todas las opciones de todos los roles + Usuarios + Metricas + Configuracion.
- [ ] Un usuario no autenticado ve: Catalogo, Login, Registrarse.

**Notas Tecnicas**:
- Componente: `Navigation` / `Sidebar`
- Guard de rutas en frontend basado en rol del JWT decodificado
- Lazy loading de modulos por rol

## US-076: Proteccion de rutas en frontend

- **Titulo**: Guards de navegacion por autenticacion y rol
- **Historia**: Como **Sistema**, quiero proteger las rutas del frontend segun autenticacion y rol, para evitar que usuarios accedan a vistas no autorizadas.
- **Prioridad**: Alta
- **Dependencias**: US-075

**Criterios de Aceptacion**:
- [ ] GIVEN un usuario no autenticado, WHEN intenta acceder a una ruta protegida, THEN es redirigido al login.
- [ ] GIVEN un usuario autenticado sin el rol requerido, WHEN intenta acceder a una ruta restringida, THEN ve pantalla 403 o es redirigido.
- [ ] Las rutas publicas (catalogo, login, registro) son accesibles sin autenticacion.

**Notas Tecnicas**:
- Route guards (React Router / Angular Guards)
- HOC `withAuth(Component, requiredRoles)` o equivalente
- Zustand auth store como source of truth del estado de autenticacion

## US-066: Manejo de token expirado en frontend

- **Titulo**: Renovacion transparente de sesion
- **Historia**: Como **Sistema**, quiero interceptar respuestas 401 en el frontend y renovar el token automaticamente, para que el cliente no pierda su sesion por expiracion del access token.
- **Prioridad**: Alta
- **Dependencias**: US-003

**Criterios de Aceptacion**:
- [ ] GIVEN un access token expirado, WHEN el frontend recibe 401, THEN automaticamente llama al endpoint de refresh y reintenta la request original.
- [ ] GIVEN un refresh token tambien expirado, WHEN el refresh falla, THEN se redirige al usuario al login.
- [ ] El proceso es transparente para el usuario (no ve errores intermitentes).
- [ ] Si hay multiples requests concurrentes y el token expira, se encolan las requests y se resuelven todas tras el refresh (queue de requests).

**Notas Tecnicas**:
- Axios/fetch interceptor que detecta 401
- Singleton de refresh en progreso para evitar multiples refresh simultaneos
- Cola de requests pendientes que se resuelven post-refresh

## US-067: Manejo de errores global en frontend

- **Titulo**: Gestion centralizada de errores HTTP
- **Historia**: Como **Cliente**, quiero ver mensajes de error claros cuando algo falla, para entender que paso y que puedo hacer.
- **Prioridad**: Media
- **Dependencias**: US-002

**Criterios de Aceptacion**:
- [ ] GIVEN un error 400 (validacion), WHEN ocurre, THEN se muestran los errores de campo especificos.
- [ ] GIVEN un error 403, WHEN ocurre, THEN se muestra "No tenes permisos para esta accion".
- [ ] GIVEN un error 404, WHEN ocurre, THEN se muestra "Recurso no encontrado".
- [ ] GIVEN un error 429, WHEN ocurre, THEN se muestra "Demasiadas solicitudes, espera un momento".
- [ ] GIVEN un error 500, WHEN ocurre, THEN se muestra "Error interno, intenta de nuevo mas tarde".

**Notas Tecnicas**:
- Error boundary global en React/Angular
- Interceptor de Axios/HttpClient para mapear codigos a mensajes
- Toast/notification system para errores no bloqueantes
