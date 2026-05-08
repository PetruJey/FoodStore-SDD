# Máquina de Estados del Pedido

El ciclo de vida de un pedido en Food Store se modela como una máquina de estados finitos (FSM) con seis estados y transiciones estrictamente controladas. Este diseño garantiza que un pedido solo pueda avanzar por caminos válidos y que cualquier intento de transición inválida sea rechazado por el sistema.

Los seis estados y sus significados son:

**PENDIENTE** es el estado inicial de todo pedido recién creado. En este estado, el pedido ha sido registrado en el sistema pero aún no se ha recibido confirmación de pago. El pedido permanece en este estado hasta que MercadoPago notifica que el pago fue aprobado, o hasta que el cliente o un gestor lo cancela.

**CONFIRMADO** es el estado al que transiciona un pedido cuando el pago asociado es aprobado por MercadoPago. En este momento, el sistema decrementa automáticamente el stock de cada producto incluido en el pedido. Este estado indica que el pedido es válido, pagado, y está listo para ser procesado por el equipo de preparación.

**EN_PREPARACIÓN** indica que el equipo de cocina o preparación está trabajando activamente en el pedido. La transición a este estado es realizada por un usuario con rol PEDIDOS (Gestor de Pedidos) y marca el inicio del proceso operativo.

**EN_CAMINO** indica que el pedido ha sido despachado y está en tránsito hacia la dirección de entrega del cliente. Esta transición también es realizada por el Gestor de Pedidos.

**ENTREGADO** es un estado terminal que indica que el pedido fue recibido exitosamente por el cliente. Una vez en este estado, no se permiten más transiciones. Es el final feliz del flujo.

**CANCELADO** es el otro estado terminal, pero representa la finalización no exitosa del pedido. Un pedido puede ser cancelado desde múltiples estados previos, pero no desde todos. Una vez cancelado, si el pedido ya había sido confirmado (es decir, el stock ya se había decrementado), el sistema debe restaurar el stock de los productos afectados.

Las transiciones válidas son:

- PENDIENTE → CONFIRMADO (automática, cuando el pago es aprobado)
- CONFIRMADO → EN_PREPARACIÓN (manual, por Gestor de Pedidos)
- EN_PREPARACIÓN → EN_CAMINO (manual, por Gestor de Pedidos)
- EN_CAMINO → ENTREGADO (manual, por Gestor de Pedidos)
- PENDIENTE → CANCELADO (manual, por Cliente, Gestor de Pedidos o Admin)
- CONFIRMADO → CANCELADO (manual, por Gestor de Pedidos o Admin, con restauración de stock)
- EN_PREPARACIÓN → CANCELADO (manual, por Admin únicamente, con restauración de stock)

Las reglas de negocio asociadas a la máquina de estados son:

**RN-01**: Un pedido solo puede avanzar al siguiente estado en la secuencia definida. No se permiten saltos (por ejemplo, de PENDIENTE directamente a EN_CAMINO) ni retrocesos (por ejemplo, de EN_PREPARACIÓN a CONFIRMADO). La única excepción es la transición a CANCELADO, que puede ocurrir desde estados no terminales.

**RN-02**: La transición de PENDIENTE a CONFIRMADO es exclusivamente automática y se dispara cuando el sistema recibe una notificación IPN de MercadoPago indicando que el pago fue aprobado (`mp_status = "approved"`). Ningún usuario puede ejecutar esta transición manualmente.

**RN-03**: Cuando un pedido alcanza el estado CONFIRMADO, el sistema debe decrementar atómicamente el `stock_cantidad` de cada producto incluido en el pedido. Esta operación debe ser transaccional — si el decremento de cualquier producto falla (por ejemplo, porque no hay stock suficiente), toda la operación debe revertirse y el pedido debe permanecer en PENDIENTE.

**RN-04**: Cuando un pedido que ya fue confirmado es cancelado, el sistema debe restaurar el stock de todos los productos afectados. Esta restauración es el proceso inverso de RN-03 y también debe ser atómica.

**RN-05**: Los estados ENTREGADO y CANCELADO son terminales. Una vez que un pedido alcanza cualquiera de estos estados, no se permite ninguna transición adicional. Cualquier intento de modificar el estado de un pedido terminal debe ser rechazado con un error descriptivo.
