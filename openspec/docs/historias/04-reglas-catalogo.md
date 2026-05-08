# Reglas de Negocio — Catalogo de Productos

| ID | Regla | Historias Asociadas |
| --- | --- | --- |
| RN-CA01 | Las categorías soportan jerarquía de profundidad arbitraria mediante FK autoreferencial (padre_id) | US-007, US-008 |
| RN-CA02 | No se permite asignar una categoría como padre de sí misma ni generar ciclos en la jerarquía | US-009 |
| RN-CA03 | No se puede eliminar una categoría que tenga productos activos asociados | US-010 |
| RN-CA04 | El precio del producto se almacena como NUMERIC de precisión fija (nunca float/double) | US-015, US-020 |
| RN-CA05 | El stock es un entero >= 0; nunca puede ser negativo | US-015, US-021 |
| RN-CA06 | Un producto puede pertenecer a múltiples categorías (M2M vía ProductoCategoria) | US-016 |
| RN-CA07 | Un producto puede tener múltiples ingredientes (M2M vía ProductoIngrediente); cada ingrediente tiene flag es_alergeno | US-017 |
| RN-CA08 | El catálogo público solo muestra productos con disponible=true y eliminado_en IS NULL | US-018 |
| RN-CA09 | El soft delete marca eliminado_en con timestamp; NUNCA se borra físicamente (preserva integridad referencial) | US-010, US-014, US-022, US-055 |
| RN-CA10 | Los endpoints de admin pueden incluir parámetro incluir_eliminados para ver registros borrados lógicamente | US-064 |
