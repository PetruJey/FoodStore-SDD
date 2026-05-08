# Visión General

Food Store es un sistema de comercio electrónico diseñado específicamente para la venta de productos alimenticios. Su propósito fundamental es ofrecer una plataforma completa que permita a los clientes explorar un catálogo de productos, gestionar un carrito de compras, realizar pedidos y pagar de forma segura a través de MercadoPago. Al mismo tiempo, el sistema brinda herramientas de administración para controlar el inventario, procesar pedidos y obtener métricas del negocio.

El sistema contempla cinco actores principales que interactúan con la plataforma de maneras distintas y complementarias:

- **Cliente**: Es el usuario final de la tienda. Puede registrarse, iniciar sesión, navegar el catálogo de productos, agregar ítems a su carrito, crear pedidos, seleccionar una dirección de entrega, realizar pagos mediante MercadoPago y consultar el historial de sus pedidos. El cliente tiene visibilidad únicamente sobre sus propios datos y operaciones.

- **Administrador (Admin)**: Posee control total sobre el sistema. Puede gestionar usuarios (crear, editar, desactivar), asignar roles, administrar el catálogo completo de productos y categorías, supervisar todos los pedidos sin importar su estado, acceder al panel de métricas y configurar parámetros globales del sistema como formas de pago y estados de pedido.

- **Gestor de Stock**: Es el responsable de mantener actualizado el inventario. Puede consultar y modificar las cantidades disponibles de cada producto, marcar productos como disponibles o no disponibles, y gestionar los ingredientes asociados a cada producto incluyendo la identificación de alérgenos. Su alcance está limitado exclusivamente a las operaciones de catálogo e inventario.

- **Gestor de Pedidos**: Se encarga del flujo operativo de los pedidos. Puede visualizar todos los pedidos del sistema, avanzar su estado a través de la máquina de estados definida (por ejemplo, de CONFIRMADO a EN_PREPARACIÓN, o de EN_PREPARACIÓN a EN_CAMINO), y cancelar pedidos cuando las reglas de negocio lo permitan. No tiene acceso a la gestión de productos ni de usuarios.

- **Sistema**: Representa los procesos automatizados que operan sin intervención humana. El actor Sistema se encarga de recibir y procesar las notificaciones IPN (Instant Payment Notification) de MercadoPago, actualizar el estado de los pagos en la base de datos, y disparar las transiciones automáticas de estado en los pedidos cuando un pago es aprobado. También gestiona la expiración y rotación de tokens de autenticación.

Los objetivos principales del sistema son: proporcionar una experiencia de compra fluida y segura para el cliente, garantizar la trazabilidad completa de cada pedido desde su creación hasta su entrega, mantener la integridad del inventario en todo momento, integrar de forma robusta el procesamiento de pagos con MercadoPago, y ofrecer un modelo de autorización granular basado en roles que permita segregar responsabilidades operativas.
