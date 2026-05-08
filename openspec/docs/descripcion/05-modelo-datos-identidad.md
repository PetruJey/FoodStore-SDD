# Modelo de Datos — Dominio 1: Identidad y Acceso

El modelo de datos de Food Store está organizado en tres dominios claramente diferenciados, todos diseñados en tercera forma normal (3NF) para garantizar la integridad referencial y minimizar la redundancia. A lo largo del modelo se aplican dos patrones transversales: el **soft delete** (borrado lógico mediante un campo `eliminado_en` de tipo timestamp nullable, que permite "eliminar" registros sin perderlos físicamente) y los **campos de auditoría** (`creado_en` y `actualizado_en` presentes en todas las tablas principales).

## Dominio 1 — Identidad y Acceso

Este dominio gestiona todo lo relacionado con la autenticación, autorización y datos personales de los usuarios.

La entidad central es **Usuario**, que almacena los datos de cada persona registrada en el sistema. Sus campos principales son: un identificador único autoincremental, el nombre completo, el email (que sirve como credencial de login y tiene una restricción de unicidad), el hash de la contraseña (nunca se almacena la contraseña en texto plano), un teléfono opcional, y los campos de auditoría y soft delete. El email se indexa para optimizar las búsquedas durante el login.

La entidad **Rol** define los perfiles de autorización disponibles en el sistema. Es una tabla catálogo que se carga mediante seed data y contiene cuatro registros fijos: ADMIN, STOCK, PEDIDOS y CLIENT. Cada rol tiene un identificador, un nombre único y una descripción.

La relación entre usuarios y roles se modela mediante la tabla intermedia **UsuarioRol**, que implementa una relación muchos-a-muchos. Un usuario puede tener múltiples roles simultáneamente (por ejemplo, un usuario podría ser tanto ADMIN como STOCK), y un rol puede estar asignado a múltiples usuarios. Esta tabla contiene el ID del usuario, el ID del rol, y una restricción de unicidad compuesta que impide asignar el mismo rol dos veces al mismo usuario.

La entidad **RefreshToken** almacena los tokens de renovación emitidos durante el login. Cada registro contiene el token en sí (una cadena UUID única), el ID del usuario al que pertenece, la fecha de expiración, y un campo `revocado_en` que se establece cuando el token es invalidado (ya sea por logout explícito o por rotación). La relación con Usuario es muchos-a-uno: un usuario puede tener múltiples refresh tokens activos (por ejemplo, desde diferentes dispositivos).

La entidad **DireccionEntrega** almacena las direcciones de envío de cada cliente. Un usuario puede tener múltiples direcciones registradas, y cada dirección incluye: calle, número, piso y departamento (opcionales), ciudad, código postal, y una referencia opcional para facilitar la entrega. También incluye un campo booleano `es_predeterminada` que indica cuál es la dirección por defecto del usuario. La relación con Usuario es muchos-a-uno.
