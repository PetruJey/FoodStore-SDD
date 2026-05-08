# Modelo de Datos — Dominio 2: Catálogo de Productos

## Dominio 2 — Catálogo de Productos

Este dominio abarca la gestión del catálogo, incluyendo categorías, productos, ingredientes y sus relaciones.

La entidad **Categoria** implementa un sistema jerárquico de categorías. Cada categoría tiene un identificador, un nombre, una descripción, una imagen opcional, y crucialmente un campo `padre_id` que es una clave foránea autoreferencial apuntando a otra categoría. Este diseño permite construir árboles de categorías de profundidad arbitraria — por ejemplo, "Alimentos" → "Lácteos" → "Quesos" → "Quesos duros". Para consultar el árbol completo de una categoría (incluyendo todos sus descendientes), se utilizan **Common Table Expressions (CTE) recursivas** de PostgreSQL, lo que permite obtener toda la jerarquía en una sola query eficiente sin necesidad de múltiples round-trips a la base de datos.

La entidad **Producto** es el corazón del catálogo. Cada producto tiene: un identificador, un nombre, una descripción detallada, una URL de imagen, el precio unitario (almacenado como tipo numérico de precisión fija para evitar errores de punto flotante), la cantidad en stock (`stock_cantidad` como entero), un campo booleano `disponible` que permite desactivar un producto sin eliminarlo, y los campos de auditoría y soft delete. El campo `stock_cantidad` se decrementa atómicamente cuando se confirma un pedido y se incrementa si un pedido es cancelado, garantizando la consistencia del inventario.

La entidad **Ingrediente** registra los componentes de cada producto. Además de un nombre y una descripción, incluye el campo booleano `es_alergeno` que indica si el ingrediente es un alérgeno común (como gluten, lactosa, frutos secos, maní, etc.). Esta información es crítica para cumplir con regulaciones alimentarias y permitir que los clientes con restricciones dietarias tomen decisiones informadas.

Las relaciones entre productos y categorías se modelan mediante la tabla intermedia **ProductoCategoria**, que implementa una relación muchos-a-muchos. Un producto puede pertenecer a múltiples categorías (por ejemplo, una pizza podría estar en "Comidas preparadas" y en "Ofertas"), y una categoría puede contener múltiples productos.

De manera análoga, la tabla **ProductoIngrediente** conecta productos con ingredientes en una relación muchos-a-muchos. Esto permite que un ingrediente como "Harina de trigo" esté asociado a múltiples productos, y que un producto tenga una lista completa de sus ingredientes.

La entidad **FormaPago** es una tabla catálogo que define los métodos de pago aceptados por la tienda. Se carga mediante seed data y contiene registros como "Tarjeta de crédito", "Tarjeta de débito", y potencialmente "Efectivo al recibir". Cada forma de pago tiene un identificador, un nombre y un booleano `activo` que permite habilitar o deshabilitar métodos de pago sin eliminarlos.
