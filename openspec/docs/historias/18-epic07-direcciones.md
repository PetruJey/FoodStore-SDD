# EPIC 07 — Gestion de Direcciones de Entrega

## US-024: Crear direccion de entrega

- **Titulo**: Alta de direccion de entrega
- **Historia**: Como **Cliente**, quiero agregar direcciones de entrega a mi perfil, para seleccionarlas al realizar un pedido.
- **Prioridad**: Alta
- **Dependencias**: US-002

**Criterios de Aceptacion**:
- [ ] GIVEN un cliente autenticado, WHEN agrega una direccion con calle, numero, piso/depto (opcional), ciudad, codigo postal, THEN la direccion se asocia a su cuenta.
- [ ] Si es la primera direccion, se marca como predeterminada automaticamente.
- [ ] Un cliente puede tener multiples direcciones.

**Notas Tecnicas**:
- Endpoint: `POST /api/direcciones`
- Tabla: `Direccion` con FK a `Usuario`
- Campo `esPredeterminada` booleano

## US-025: Listar direcciones del cliente

- **Titulo**: Consulta de direcciones propias
- **Historia**: Como **Cliente**, quiero ver todas mis direcciones guardadas, para gestionar donde recibo mis pedidos.
- **Prioridad**: Alta
- **Dependencias**: US-024

**Criterios de Aceptacion**:
- [ ] GIVEN un cliente autenticado, WHEN solicita sus direcciones, THEN recibe solo las direcciones asociadas a su cuenta.
- [ ] La direccion predeterminada se indica claramente.

**Notas Tecnicas**:
- Endpoint: `GET /api/direcciones`
- Filtrado automatico por `userId` extraido del JWT

## US-026: Editar direccion de entrega

- **Titulo**: Modificacion de direccion
- **Historia**: Como **Cliente**, quiero editar una direccion existente, para corregir o actualizar mis datos de entrega.
- **Prioridad**: Media
- **Dependencias**: US-024

**Criterios de Aceptacion**:
- [ ] GIVEN una direccion propia, WHEN el cliente la modifica, THEN los cambios se persisten.
- [ ] Un cliente no puede editar direcciones de otro usuario.

**Notas Tecnicas**:
- Endpoint: `PUT /api/direcciones/:id`
- Validar ownership: `direccion.userId === jwt.userId`

## US-027: Eliminar direccion de entrega

- **Titulo**: Baja de direccion
- **Historia**: Como **Cliente**, quiero eliminar una direccion que ya no uso, para mantener limpio mi listado de direcciones.
- **Prioridad**: Baja
- **Dependencias**: US-024

**Criterios de Aceptacion**:
- [ ] GIVEN una direccion propia sin pedidos activos asociados, WHEN solicita eliminarla, THEN se elimina (logica o fisica segun politica).
- [ ] Si la direccion eliminada era la predeterminada, se debe asignar otra o dejar sin predeterminada.

**Notas Tecnicas**:
- Endpoint: `DELETE /api/direcciones/:id`

## US-028: Establecer direccion predeterminada

- **Titulo**: Seleccion de direccion predeterminada
- **Historia**: Como **Cliente**, quiero marcar una direccion como predeterminada, para que se preseleccione al crear un pedido.
- **Prioridad**: Media
- **Dependencias**: US-024

**Criterios de Aceptacion**:
- [ ] GIVEN un cliente con multiples direcciones, WHEN marca una como predeterminada, THEN la anterior predeterminada pierde ese estado y la nueva lo obtiene.
- [ ] Solo una direccion puede ser predeterminada a la vez.

**Notas Tecnicas**:
- Endpoint: `PATCH /api/direcciones/:id/predeterminada`
- Transaccion: quitar flag de la anterior, setear en la nueva
