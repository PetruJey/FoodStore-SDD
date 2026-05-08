# EPIC 18 — Configuracion del Sistema

## US-060: Configuracion del sistema

- **Titulo**: Panel de configuracion general
- **Historia**: Como **Admin**, quiero gestionar configuraciones generales del sistema, para ajustar parametros operativos sin tocar codigo.
- **Prioridad**: Baja
- **Dependencias**: US-006

**Criterios de Aceptacion**:
- [ ] GIVEN un Admin, WHEN accede a la configuracion, THEN puede ver y modificar parametros como: horarios de atencion, zona de entrega, mensajes del sistema.
- [ ] Los cambios se aplican inmediatamente sin reiniciar el sistema.
- [ ] Se registra quien modifico que y cuando.

**Notas Tecnicas**:
- Endpoint: `GET/PUT /api/admin/configuracion`
- Tabla key-value: `Configuracion` con `clave`, `valor`, `updatedBy`, `updatedAt`
