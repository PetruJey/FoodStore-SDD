# Reglas de Negocio — Autenticacion y Seguridad

| ID | Regla | Historias Asociadas |
| --- | --- | --- |
| RN-AU01 | La contraseña NUNCA se almacena en texto plano; se hashea con bcrypt (cost factor >= 10) con salt automático | US-001, US-063 |
| RN-AU02 | El access token JWT tiene duración de 30 minutos, contiene userId, email y roles, firmado con HS256 | US-002, US-003 |
| RN-AU03 | El refresh token tiene duración de 7 días, es un UUID v4 opaco almacenado en BD | US-002, US-003 |
| RN-AU04 | Al usar un refresh token se aplica rotación: el anterior se revoca y se emite uno nuevo | US-003 |
| RN-AU05 | Si se detecta reuso de un refresh token ya utilizado (replay attack), se revocan TODOS los tokens del usuario | US-003 |
| RN-AU06 | Rate limiting en login: máximo 5 intentos por IP en ventana de 15 minutos; excedido retorna HTTP 429 | US-002, US-073 |
| RN-AU07 | Al registrarse se asigna automáticamente el rol CLIENT; el rol NO viene del request | US-001 |
| RN-AU08 | La respuesta de login NO debe diferenciar "email no existe" de "contraseña incorrecta" (seguridad) | US-002 |
| RN-AU09 | Los datos sensibles de tarjetas NUNCA pasan por el servidor de Food Store (PCI DSS SAQ-A) | US-045 |
| RN-AU10 | El archivo .env con secrets NUNCA se commitea al repositorio | US-000 |
