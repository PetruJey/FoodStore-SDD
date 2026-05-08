# Reglas de Negocio — Carrito de Compras

| ID | Regla | Historias Asociadas |
| --- | --- | --- |
| RN-CR01 | El carrito es client-side only (Zustand + localStorage); no existe en el backend | US-029 a US-034 |
| RN-CR02 | El carrito persiste al cerrar el navegador, refresh de página, y logout/login | US-029 |
| RN-CR03 | Si un producto ya está en el carrito y se agrega de nuevo, se incrementa la cantidad (no se duplica) | US-029 |
| RN-CR04 | Solo se pueden excluir ingredientes que el producto efectivamente tiene asociados | US-030 |
| RN-CR05 | La personalización (exclusión de ingredientes) se almacena como array de IDs de ingredientes | US-030, US-035 |
