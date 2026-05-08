# Autenticación — Flujo JWT

Food Store implementa un sistema de autenticación basado en JSON Web Tokens (JWT) con un esquema de doble token: un **access token** de corta duración y un **refresh token** de larga duración.

El **access token** tiene una duración de 30 minutos y se utiliza para autenticar cada petición al backend. Su payload contiene el ID del usuario, su email y sus roles. Se firma con el algoritmo HS256 usando una clave secreta configurada en las variables de entorno. Este token se envía en el header `Authorization: Bearer <token>` de cada petición HTTP.

El **refresh token** tiene una duración de 7 días y se utiliza exclusivamente para obtener un nuevo access token cuando el actual expira. Se genera como un UUID v4 y se almacena en la base de datos en la tabla RefreshToken, asociado al usuario. A diferencia del access token, el refresh token no contiene información del usuario — es simplemente un identificador opaco que el servidor valida contra la base de datos.

El flujo completo de autenticación funciona de la siguiente manera:

Cuando el usuario inicia sesión, envía su email y contraseña al endpoint de login. El backend verifica las credenciales contra la base de datos (comparando el hash bcrypt), y si son válidas, genera ambos tokens. El access token se devuelve en el cuerpo de la respuesta junto con el refresh token y los datos básicos del usuario. El frontend almacena ambos tokens en el **authStore de Zustand**, que a su vez los persiste en localStorage mediante el middleware de persistencia.

Para cada petición subsiguiente, el **interceptor de Axios** automáticamente adjunta el access token al header Authorization. Cuando el access token expira (el servidor responde con 401), el interceptor automáticamente envía el refresh token al endpoint de renovación, obtiene un nuevo par de tokens, actualiza el authStore, y reintenta la petición original de forma transparente para el usuario. Este proceso ocurre sin que el usuario perciba ninguna interrupción.

El endpoint de renovación implementa **rotación de refresh tokens**: cada vez que se usa un refresh token para obtener uno nuevo, el token anterior se marca como revocado (se establece el campo `revocado_en`) y se emite uno completamente nuevo. Esto limita la ventana de exposición si un refresh token es comprometido.

El logout se implementa marcando el refresh token actual como revocado en la base de datos y limpiando el authStore en el frontend. No es necesario invalidar el access token explícitamente — dado su corta duración de 30 minutos, simplemente se deja expirar.

En el backend, la autenticación se implementa mediante la dependencia de FastAPI `get_current_user`. Esta función se inyecta en cualquier endpoint que requiera autenticación, decodifica el access token del header Authorization, verifica su firma y expiración, y devuelve el objeto Usuario correspondiente. Si el token es inválido o está expirado, la dependencia lanza una excepción HTTP 401 automáticamente.
