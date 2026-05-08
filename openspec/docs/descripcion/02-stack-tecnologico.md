# Stack Tecnológico

## Frontend

El frontend de Food Store está construido sobre **React** con **TypeScript**, utilizando **Vite** como bundler y servidor de desarrollo. La elección de Vite responde a su velocidad superior en comparación con alternativas como Webpack o Create React App, gracias a su uso de ES modules nativos durante el desarrollo y Rollup para las builds de producción.

Para la gestión del estado del servidor — es decir, los datos que provienen del backend como productos, pedidos y usuarios — se utiliza **TanStack Query** (anteriormente conocido como React Query). Esta librería maneja automáticamente el caching, la revalidación, el refetching en segundo plano, la paginación y los estados de carga y error. Esto permite que los componentes se suscriban a queries declarativas sin necesidad de escribir lógica imperativa de fetching.

La gestión de formularios se delega a **TanStack Form**, que proporciona validación declarativa, manejo de estado de campos individuales y soporte para esquemas de validación complejos. Esta librería se integra naturalmente con el ecosistema TanStack y permite construir formularios tipados de extremo a extremo gracias a TypeScript.

Para el estado puramente del cliente — como el carrito de compras, el estado de autenticación y preferencias de la interfaz — se emplea **Zustand**. Esta librería destaca por su API minimalista, su excelente rendimiento (ya que permite suscripciones granulares a porciones específicas del store) y su capacidad de persistir estado en localStorage mediante middleware.

Las peticiones HTTP al backend se realizan a través de **Axios**, configurado con interceptores que automáticamente adjuntan el token JWT a cada request y manejan la renovación transparente del token cuando éste expira.

La visualización de datos y métricas del panel de administración utiliza **recharts**, una librería de gráficos construida sobre componentes React y D3. Permite renderizar gráficos de barras, líneas, tortas y áreas de forma declarativa.

El sistema de estilos está basado en **Tailwind CSS**, un framework de utilidades que permite construir interfaces directamente en el markup sin necesidad de escribir hojas de estilo separadas. Tailwind se integra con Vite a través de PostCSS y ofrece purging automático de clases no utilizadas en producción.

Para la integración con MercadoPago en el lado del cliente, se utiliza el **SDK de MercadoPago para JavaScript** (MercadoPago.js), que permite la tokenización segura de tarjetas directamente en el navegador sin que los datos sensibles pasen por el servidor de Food Store, cumpliendo así con los requisitos de PCI DSS SAQ-A.

## Backend

El backend está construido con **FastAPI**, un framework moderno de Python que ofrece alto rendimiento gracias a su naturaleza asíncrona basada en ASGI, validación automática de datos mediante Pydantic, y generación automática de documentación OpenAPI (Swagger UI y ReDoc).

El ORM elegido es **SQLModel**, una librería creada por el mismo autor de FastAPI (Sebastián Ramírez) que combina la potencia de SQLAlchemy con la validación de Pydantic en un solo modelo. Esto significa que los modelos de base de datos y los schemas de validación comparten una base común, reduciendo la duplicación de código y los errores de sincronización.

La base de datos es **PostgreSQL**, seleccionada por su robustez, soporte avanzado de tipos de datos (como arrays de enteros para la personalización de pedidos), soporte para Common Table Expressions (CTE) recursivas necesarias para las categorías jerárquicas, y su ecosistema maduro de herramientas.

Las migraciones de base de datos se gestionan con **Alembic**, la herramienta estándar del ecosistema SQLAlchemy. Alembic permite generar migraciones automáticas a partir de cambios en los modelos, aplicarlas de forma incremental, y revertirlas cuando sea necesario. Cada migración se versiona como un script Python que describe los cambios DDL.

El hashing de contraseñas se realiza mediante **Passlib** con el algoritmo **bcrypt**. Passlib proporciona una interfaz unificada para múltiples algoritmos de hashing y maneja automáticamente la generación de salts, la verificación de hashes y la migración transparente entre algoritmos.

El rate limiting se implementa con **slowapi**, una librería que integra el rate limiting directamente en FastAPI a través de middleware. Se utiliza principalmente para proteger el endpoint de login contra ataques de fuerza bruta, limitando los intentos a 5 cada 15 minutos por dirección IP.

La generación y verificación de tokens JWT se realiza con **python-jose** (o **PyJWT** según la configuración), que proporciona las funciones criptográficas necesarias para firmar y validar tokens con el algoritmo HS256.

Para la integración con MercadoPago en el backend, se utiliza el **SDK oficial de MercadoPago para Python**, que proporciona clientes tipados para la API de Orders (checkout), gestión de pagos y procesamiento de webhooks.
