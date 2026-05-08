# EPIC 04 — Gestion de Ingredientes y Alergenos

## US-011: Crear ingrediente

- **Titulo**: Alta de ingrediente
- **Historia**: Como **Gestor de Stock**, quiero registrar ingredientes indicando si son alergenos, para informar correctamente a los clientes sobre la composicion de los productos.
- **Prioridad**: Alta
- **Dependencias**: US-006

**Criterios de Aceptacion**:
- [ ] GIVEN un Gestor de Stock autenticado, WHEN crea un ingrediente con nombre y flag de alergeno, THEN el ingrediente queda disponible para asociar a productos.
- [ ] El campo `esAlergeno` es booleano, obligatorio.
- [ ] El nombre del ingrediente es unico, no vacio.

**Notas Tecnicas**:
- Endpoint: `POST /api/ingredientes`
- Tabla: `Ingrediente` con `id`, `nombre`, `esAlergeno`

## US-012: Listar ingredientes

- **Titulo**: Consulta de ingredientes
- **Historia**: Como **Gestor de Stock**, quiero ver todos los ingredientes registrados, para gestionar su asociacion con productos.
- **Prioridad**: Alta
- **Dependencias**: US-011

**Criterios de Aceptacion**:
- [ ] GIVEN ingredientes existentes, WHEN se solicita el listado, THEN se retornan todos los ingredientes con su flag de alergeno.
- [ ] Se puede filtrar por `esAlergeno=true` para ver solo alergenos.
- [ ] Soporta paginacion.

**Notas Tecnicas**:
- Endpoint: `GET /api/ingredientes`
- Query params: `?esAlergeno=true&page=1&limit=20`

## US-013: Editar ingrediente

- **Titulo**: Modificacion de ingrediente
- **Historia**: Como **Gestor de Stock**, quiero editar un ingrediente existente, para corregir datos o actualizar su clasificacion como alergeno.
- **Prioridad**: Media
- **Dependencias**: US-011

**Criterios de Aceptacion**:
- [ ] GIVEN un ingrediente existente, WHEN se modifica nombre o flag de alergeno, THEN los cambios se persisten.
- [ ] El nuevo nombre no puede coincidir con otro ingrediente existente.

**Notas Tecnicas**:
- Endpoint: `PUT /api/ingredientes/:id`

## US-014: Eliminar ingrediente (soft delete)

- **Titulo**: Baja logica de ingrediente
- **Historia**: Como **Gestor de Stock**, quiero dar de baja un ingrediente, para que no se pueda asociar a nuevos productos sin perder los registros historicos.
- **Prioridad**: Baja
- **Dependencias**: US-011

**Criterios de Aceptacion**:
- [ ] GIVEN un ingrediente, WHEN se elimina logicamente, THEN deja de aparecer para nuevas asociaciones pero se mantiene en productos existentes.
- [ ] Soft delete con campo `deletedAt`.

**Notas Tecnicas**:
- Endpoint: `DELETE /api/ingredientes/:id`
