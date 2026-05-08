# EPIC 03 — Gestion de Categorias

## US-007: Crear categoria

- **Titulo**: Alta de categoria de productos
- **Historia**: Como **Gestor de Stock**, quiero crear categorias para organizar los productos, para que los clientes encuentren lo que buscan mas facilmente.
- **Prioridad**: Alta
- **Dependencias**: US-006

**Criterios de Aceptacion**:
- [ ] GIVEN un Gestor de Stock autenticado, WHEN crea una categoria con nombre y opcionalmente una categoria padre, THEN la categoria se almacena y esta disponible en el catalogo.
- [ ] GIVEN un nombre de categoria duplicado en el mismo nivel, WHEN intenta crearla, THEN el sistema rechaza con error de validacion.
- [ ] La categoria puede ser raiz (sin padre) o subcategoria (con `parentId`).
- [ ] El nombre es obligatorio, no vacio, maximo 100 caracteres.

**Notas Tecnicas**:
- Endpoint: `POST /api/categorias`
- Tabla: `Categoria` con `id`, `nombre`, `parentId` (self-referencing FK)
- Consultas jerarquicas con CTE recursivo (Common Table Expression)

## US-008: Listar categorias jerarquicas

- **Titulo**: Visualizacion del arbol de categorias
- **Historia**: Como **Cliente**, quiero ver las categorias organizadas en forma jerarquica, para navegar el catalogo de manera intuitiva.
- **Prioridad**: Alta
- **Dependencias**: US-007

**Criterios de Aceptacion**:
- [ ] GIVEN categorias existentes con relaciones padre-hijo, WHEN se solicita el listado, THEN se retorna un arbol anidado con categorias y subcategorias.
- [ ] Las categorias sin padre aparecen como nodos raiz.
- [ ] Cada nodo incluye: id, nombre, subcategorias (recursivo).
- [ ] La respuesta es publica (no requiere autenticacion).

**Notas Tecnicas**:
- Endpoint: `GET /api/categorias` (publico)
- Query con CTE recursivo para armar el arbol
- Cachear respuesta si el volumen lo justifica

## US-009: Editar categoria

- **Titulo**: Modificacion de categoria existente
- **Historia**: Como **Gestor de Stock**, quiero editar el nombre o la jerarquia de una categoria, para mantener el catalogo organizado correctamente.
- **Prioridad**: Media
- **Dependencias**: US-007

**Criterios de Aceptacion**:
- [ ] GIVEN una categoria existente, WHEN se modifica su nombre o parentId, THEN los cambios se persisten y se reflejan en el catalogo.
- [ ] GIVEN un cambio de parentId que generaria un ciclo (A padre de B, B padre de A), WHEN se intenta, THEN el sistema rechaza con error.
- [ ] No se puede asignar una categoria como padre de si misma.

**Notas Tecnicas**:
- Endpoint: `PUT /api/categorias/:id`
- Validacion de ciclos con CTE antes de persistir

## US-010: Eliminar categoria (soft delete)

- **Titulo**: Baja logica de categoria
- **Historia**: Como **Gestor de Stock**, quiero dar de baja una categoria que ya no se usa, para mantener el catalogo limpio sin perder datos historicos.
- **Prioridad**: Media
- **Dependencias**: US-007

**Criterios de Aceptacion**:
- [ ] GIVEN una categoria sin productos activos asociados, WHEN se solicita su eliminacion, THEN se marca como eliminada (soft delete) y deja de aparecer en el catalogo publico.
- [ ] GIVEN una categoria con productos activos, WHEN se intenta eliminar, THEN el sistema rechaza indicando que debe reasignar los productos primero.
- [ ] Las subcategorias de una categoria eliminada deben reasignarse o eliminarse previamente.

**Notas Tecnicas**:
- Endpoint: `DELETE /api/categorias/:id`
- Campo `deletedAt` (timestamp nullable) para soft delete
- Filtro global en queries publicas: `WHERE deletedAt IS NULL`
