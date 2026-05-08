# EPIC 17 — Panel de Metricas y Dashboard

## US-056: Dashboard de metricas generales

- **Titulo**: Panel de metricas del sistema
- **Historia**: Como **Admin**, quiero ver metricas generales del sistema (ventas, pedidos, usuarios), para tomar decisiones informadas sobre el negocio.
- **Prioridad**: Media
- **Dependencias**: US-035, US-053

**Criterios de Aceptacion**:
- [ ] GIVEN un Admin autenticado, WHEN accede al dashboard, THEN ve: total de ventas del periodo, cantidad de pedidos por estado, cantidad de usuarios registrados, productos mas vendidos.
- [ ] Soporta filtro por rango de fechas.
- [ ] Los datos se actualizan al cambiar el filtro.

**Notas Tecnicas**:
- Endpoint: `GET /api/admin/metricas/resumen`
- Queries de agregacion: `SUM`, `COUNT`, `GROUP BY`
- Frontend: recharts para visualizaciones

## US-057: Grafico de ventas por periodo

- **Titulo**: Visualizacion de evolucion de ventas
- **Historia**: Como **Admin**, quiero ver un grafico de evolucion de ventas por dia/semana/mes, para entender las tendencias del negocio.
- **Prioridad**: Media
- **Dependencias**: US-056

**Criterios de Aceptacion**:
- [ ] GIVEN datos de ventas, WHEN selecciono un periodo y granularidad (dia/semana/mes), THEN veo un grafico de lineas con la evolucion de ventas.
- [ ] El grafico muestra monto total y cantidad de pedidos.

**Notas Tecnicas**:
- Endpoint: `GET /api/admin/metricas/ventas?desde=...&hasta=...&granularidad=dia`
- Frontend: `<LineChart>` de recharts
- Query con `DATE_TRUNC` para agrupar por granularidad

## US-058: Top productos mas vendidos

- **Titulo**: Ranking de productos
- **Historia**: Como **Admin**, quiero ver el ranking de productos mas vendidos, para entender que productos tienen mayor demanda.
- **Prioridad**: Media
- **Dependencias**: US-056

**Criterios de Aceptacion**:
- [ ] GIVEN pedidos entregados, WHEN consulto el ranking, THEN veo los top N productos ordenados por cantidad vendida.
- [ ] Soporta filtro por rango de fechas.
- [ ] Muestra: nombre del producto, cantidad total vendida, ingreso total generado.

**Notas Tecnicas**:
- Endpoint: `GET /api/admin/metricas/productos-top?top=10&desde=...&hasta=...`
- Frontend: `<BarChart>` de recharts

## US-059: Metricas de pedidos por estado

- **Titulo**: Distribucion de pedidos por estado
- **Historia**: Como **Admin**, quiero ver la distribucion de pedidos por estado, para identificar cuellos de botella en el proceso.
- **Prioridad**: Media
- **Dependencias**: US-056

**Criterios de Aceptacion**:
- [ ] GIVEN pedidos existentes, WHEN consulto la distribucion, THEN veo un grafico de torta/barras con la cantidad de pedidos en cada estado.
- [ ] Soporta filtro por rango de fechas.

**Notas Tecnicas**:
- Endpoint: `GET /api/admin/metricas/pedidos-por-estado`
- Frontend: `<PieChart>` de recharts
