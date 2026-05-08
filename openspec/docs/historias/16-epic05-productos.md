# EPIC 05 — Gestion de Productos y Catalogo

## US-015: Crear producto

- **Titulo**: Alta de producto en el catalogo
- **Historia**: Como **Gestor de Stock**, quiero dar de alta un producto con su precio, stock, imagen y descripcion, para que los clientes puedan verlo y comprarlo.
- **Prioridad**: Alta
- **Dependencias**: US-007, US-011

**Criterios de Aceptacion**:
- [ ] GIVEN un Gestor de Stock autenticado, WHEN crea un producto con nombre, descripcion, precio, stock, imagen y disponibilidad, THEN el producto se persiste y aparece en el catalogo.
- [ ] El precio se almacena con precision fija (DECIMAL/NUMERIC, no float).
- [ ] El stock es un entero >= 0.
- [ ] La disponibilidad (`disponible`) es booleano, default `true`.
- [ ] Todos los campos obligatorios se validan en backend.

**Notas Tecnicas**:
- Endpoint: `POST /api/productos`
- Precio: `DECIMAL(10,2)` o `NUMERIC` con precision fija
- Imagen: URL o upload a storage (S3/local)

## US-016: Asociar producto a categorias

- **Titulo**: Clasificacion de producto en categorias
- **Historia**: Como **Gestor de Stock**, quiero asociar un producto a una o mas categorias, para que aparezca en las secciones correctas del catalogo.
- **Prioridad**: Alta
- **Dependencias**: US-015, US-007

**Criterios de Aceptacion**:
- [ ] GIVEN un producto existente, WHEN se le asignan categorias, THEN aparece al navegar esas categorias.
- [ ] Un producto puede pertenecer a multiples categorias (M2M).
- [ ] Al quitar una categoria de un producto, deja de aparecer en esa seccion.

**Notas Tecnicas**:
- Tabla pivote: `ProductoCategoria` con `productoId` + `categoriaId`
- Endpoint: `PUT /api/productos/:id/categorias` (body: array de categoryIds)

## US-017: Asociar ingredientes a producto

- **Titulo**: Definicion de composicion del producto
- **Historia**: Como **Gestor de Stock**, quiero asociar ingredientes a un producto, para que los clientes conozcan su composicion y alergenos.
- **Prioridad**: Alta
- **Dependencias**: US-015, US-011

**Criterios de Aceptacion**:
- [ ] GIVEN un producto existente, WHEN se le asignan ingredientes, THEN se muestran en el detalle del producto.
- [ ] Los ingredientes marcados como alergeno se destacan visualmente en el frontend.
- [ ] Relacion M2M entre Producto e Ingrediente.

**Notas Tecnicas**:
- Tabla pivote: `ProductoIngrediente` con `productoId` + `ingredienteId`
- Endpoint: `PUT /api/productos/:id/ingredientes` (body: array de ingredientIds)

## US-018: Listar productos del catalogo (publico)

- **Titulo**: Navegacion del catalogo de productos
- **Historia**: Como **Cliente**, quiero ver los productos disponibles con su precio, imagen y disponibilidad, para decidir que comprar.
- **Prioridad**: Alta
- **Dependencias**: US-015

**Criterios de Aceptacion**:
- [ ] GIVEN productos existentes y disponibles, WHEN se accede al catalogo, THEN se muestran solo los productos con `disponible=true` y `deletedAt IS NULL`.
- [ ] Cada producto muestra: nombre, precio, imagen, disponibilidad.
- [ ] Soporta paginacion con `page` y `limit`.
- [ ] Soporta filtro por categoria.
- [ ] Soporta busqueda por nombre (ILIKE o full-text).
- [ ] El endpoint es publico.

**Notas Tecnicas**:
- Endpoint: `GET /api/productos` (publico)
- Query params: `?categoria=5&busqueda=pizza&page=1&limit=20`
- Incluir conteo total para paginacion en frontend

## US-019: Ver detalle de producto

- **Titulo**: Detalle completo de un producto
- **Historia**: Como **Cliente**, quiero ver el detalle completo de un producto incluyendo ingredientes y alergenos, para tomar una decision de compra informada.
- **Prioridad**: Alta
- **Dependencias**: US-017

**Criterios de Aceptacion**:
- [ ] GIVEN un producto existente y disponible, WHEN se consulta su detalle, THEN se retorna: nombre, descripcion, precio, imagen, stock > 0 (sin revelar cantidad exacta), categorias, ingredientes con flag de alergeno.
- [ ] GIVEN un producto no disponible o eliminado, WHEN se consulta, THEN retorna 404.
- [ ] El endpoint es publico.

**Notas Tecnicas**:
- Endpoint: `GET /api/productos/:id` (publico)
- Join con `ProductoIngrediente` -> `Ingrediente` y `ProductoCategoria` -> `Categoria`

## US-020: Editar producto

- **Titulo**: Modificacion de producto
- **Historia**: Como **Gestor de Stock**, quiero editar los datos de un producto existente, para mantener la informacion del catalogo actualizada.
- **Prioridad**: Alta
- **Dependencias**: US-015

**Criterios de Aceptacion**:
- [ ] GIVEN un producto existente, WHEN se modifican sus campos (nombre, descripcion, precio, imagen, disponibilidad), THEN los cambios se persisten.
- [ ] El precio se valida: debe ser > 0 y con maximo 2 decimales.
- [ ] No se permite stock negativo.

**Notas Tecnicas**:
- Endpoint: `PUT /api/productos/:id`

## US-021: Gestionar stock de producto

- **Titulo**: Actualizacion de stock
- **Historia**: Como **Gestor de Stock**, quiero actualizar la cantidad en stock de un producto, para reflejar entradas y salidas de mercaderia.
- **Prioridad**: Alta
- **Dependencias**: US-015

**Criterios de Aceptacion**:
- [ ] GIVEN un producto existente, WHEN se actualiza el stock con una cantidad, THEN el nuevo stock se persiste.
- [ ] El stock resultante nunca puede ser negativo.
- [ ] Se puede hacer incremento (`+N`) o seteo absoluto segun endpoint.

**Notas Tecnicas**:
- Endpoint: `PATCH /api/productos/:id/stock` (body: `{ cantidad: number }`)
- Operacion atomica para evitar race conditions (UPDATE con WHERE)

## US-022: Eliminar producto (soft delete)

- **Titulo**: Baja logica de producto
- **Historia**: Como **Gestor de Stock**, quiero dar de baja un producto, para que no aparezca en el catalogo sin perder los datos historicos asociados a pedidos.
- **Prioridad**: Media
- **Dependencias**: US-015

**Criterios de Aceptacion**:
- [ ] GIVEN un producto existente, WHEN se elimina logicamente, THEN deja de aparecer en el catalogo publico.
- [ ] Los pedidos historicos que referencian este producto mantienen su informacion (snapshot).
- [ ] Soft delete con `deletedAt`.

**Notas Tecnicas**:
- Endpoint: `DELETE /api/productos/:id`

## US-023: Filtrar productos por alergenos

- **Titulo**: Filtrado de productos que contienen alergenos
- **Historia**: Como **Cliente**, quiero filtrar productos que contengan determinados alergenos, para evitar alimentos que me generen reacciones alergicas.
- **Prioridad**: Media
- **Dependencias**: US-017

**Criterios de Aceptacion**:
- [ ] GIVEN el catalogo de productos, WHEN filtro excluyendo alergenos especificos (por ingredienteId), THEN solo veo productos que NO contienen esos ingredientes.
- [ ] El filtro acepta multiples ingredientes alergenos a excluir.

**Notas Tecnicas**:
- Endpoint: `GET /api/productos?excluirAlergenos=1,3,7`
- Query con `NOT EXISTS (SELECT ... FROM ProductoIngrediente WHERE ingredienteId IN (...))`
