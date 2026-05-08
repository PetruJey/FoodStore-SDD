# EPIC 15 — Administracion de Usuarios

## US-053: Listar usuarios del sistema

- **Titulo**: Panel de usuarios
- **Historia**: Como **Admin**, quiero ver todos los usuarios registrados con su rol y estado, para gestionar el acceso al sistema.
- **Prioridad**: Alta
- **Dependencias**: US-005

**Criterios de Aceptacion**:
- [ ] GIVEN un Admin autenticado, WHEN accede al listado de usuarios, THEN ve: nombre, email, rol, fecha de registro, estado (activo/inactivo).
- [ ] Soporta busqueda por nombre o email.
- [ ] Soporta filtro por rol.
- [ ] Paginacion obligatoria.

**Notas Tecnicas**:
- Endpoint: `GET /api/admin/usuarios`
- Solo accesible con rol ADMIN

## US-054: Editar usuario (Admin)

- **Titulo**: Modificacion de datos de usuario
- **Historia**: Como **Admin**, quiero editar los datos y rol de cualquier usuario, para corregir informacion o ajustar permisos.
- **Prioridad**: Media
- **Dependencias**: US-053

**Criterios de Aceptacion**:
- [ ] GIVEN un Admin, WHEN edita el rol de un usuario, THEN el cambio se aplica inmediatamente (el proximo token que obtenga ese usuario tendra el nuevo rol).
- [ ] Un Admin no puede degradar al ultimo ADMIN del sistema.
- [ ] Se puede activar/desactivar usuarios.

**Notas Tecnicas**:
- Endpoint: `PUT /api/admin/usuarios/:id`
- Invalidar refresh tokens del usuario modificado para forzar re-login con nuevo rol

## US-055: Desactivar usuario

- **Titulo**: Baja logica de usuario
- **Historia**: Como **Admin**, quiero desactivar un usuario, para impedir su acceso sin eliminar sus datos historicos.
- **Prioridad**: Media
- **Dependencias**: US-053

**Criterios de Aceptacion**:
- [ ] GIVEN un usuario activo, WHEN el Admin lo desactiva, THEN no puede loguearse mas.
- [ ] Los pedidos historicos del usuario se mantienen intactos.
- [ ] Se invalidan todos los refresh tokens del usuario desactivado.

**Notas Tecnicas**:
- Campo `activo` booleano en `Usuario`
- Validar en login: si `activo=false`, retornar 403 "Cuenta desactivada"
- Endpoint: `PATCH /api/admin/usuarios/:id/estado`
