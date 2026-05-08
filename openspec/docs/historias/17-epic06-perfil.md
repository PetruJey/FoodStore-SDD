# EPIC 06 — Gestion del Perfil del Cliente

## US-061: Ver perfil propio

- **Titulo**: Visualizacion del perfil del cliente
- **Historia**: Como **Cliente**, quiero ver los datos de mi perfil, para verificar que mi informacion sea correcta.
- **Prioridad**: Media
- **Dependencias**: US-002

**Criterios de Aceptacion**:
- [ ] GIVEN un cliente autenticado, WHEN accede a su perfil, THEN ve: nombre, email, telefono, fecha de registro.
- [ ] No puede ver datos de otros usuarios.

**Notas Tecnicas**:
- Endpoint: `GET /api/perfil`
- Datos extraidos del JWT userId

## US-062: Editar perfil propio

- **Titulo**: Modificacion de datos personales
- **Historia**: Como **Cliente**, quiero editar mis datos personales (nombre, telefono), para mantener mi informacion actualizada.
- **Prioridad**: Media
- **Dependencias**: US-061

**Criterios de Aceptacion**:
- [ ] GIVEN un cliente autenticado, WHEN modifica su nombre o telefono, THEN los cambios se persisten.
- [ ] El email NO se puede cambiar (es el identificador).
- [ ] Validacion de formato de telefono.

**Notas Tecnicas**:
- Endpoint: `PUT /api/perfil`

## US-063: Cambiar contrasena

- **Titulo**: Cambio de contrasena
- **Historia**: Como **Cliente**, quiero cambiar mi contrasena, para mantener la seguridad de mi cuenta.
- **Prioridad**: Media
- **Dependencias**: US-002

**Criterios de Aceptacion**:
- [ ] GIVEN un cliente autenticado, WHEN envia su contrasena actual y la nueva, THEN si la actual es correcta se actualiza la contrasena.
- [ ] GIVEN contrasena actual incorrecta, WHEN intenta cambiarla, THEN se rechaza con error.
- [ ] La nueva contrasena debe cumplir los mismos requisitos que en el registro (minimo 8 caracteres).
- [ ] Se invalidan todos los refresh tokens existentes (forzar re-login).

**Notas Tecnicas**:
- Endpoint: `PUT /api/perfil/password`
- Body: `{ passwordActual, passwordNueva }`
- Verificar con `bcrypt.compare` antes de hashear la nueva
