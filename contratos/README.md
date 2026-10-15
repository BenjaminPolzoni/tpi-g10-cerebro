# Contratos Técnicos de Integración

Este directorio almacena los contratos canónicos de APIs REST (OpenAPI), mensajería asíncrona (AsyncAPI y contratos Kafka) y acuerdos de integración del microservicio `roadmap-service` (Grupo 10) con el resto de la plataforma.

## Índice de Contratos

| Archivo | Contraparte / Dominio | Descripción |
|---|---|---|
| [[roadmap-motor-gate-v1]] | Motor de Desafíos (Tema 02/09) | Contrato del Gate de elegibilidad de inicio de desafíos (`/eligibility`). |
| [[motor-desafios-evento-cierre]] | Motor de Desafíos (Tema 02/09) | Contrato del evento de cierre `CHALLENGE_COMPLETED` en `challenges.events`. |
| [[motor-desafios]] | Motor de Desafíos (Tema 02/09) | Especificación general de integración con el catálogo y pool de desafíos. |
| [[courses]] | Courses & Enrollment (Tema 03) | Integración con cohorte, secciones, sync y padrón de alumnos. |
| [[courses-grupos-t-10-1]] | Courses & Enrollment (Tema 03) | Acta T-10.1: comisiones, grupos y restricciones de sección/actividad. |
| [[accounting-roadmap-v1]] | Accounting / Inventario (Tema 08) | Disponibilidad de vidas (`lives-availability`), inventario (`equip-summary`) y cuentas por cohorte. |
| [[backoffice-par]] | Backoffice (Tema 12) | Consulta de parámetros globales PAR (curva de niveles PAR-09) y eventos de actualización. |
| [[CONTRATO_T10_BACKOFFICE]] | Backoffice (Tema 12) | Contrato extendido de integración de parámetros de progreso. |
| [[bus-notificaciones]] | Notificaciones / Bus Kafka | Estándar de eventos del bus, envelope de 5 campos y topics asignados. |
| [[roadmap-events-v1]] | Notificaciones / Plataforma | Especificación de eventos emitidos por Roadmap vía Transactional Outbox. |
| [[roadmap-service.asyncapi.yaml]] | Plataforma Kafka | Especificación AsyncAPI formal de los eventos consumidos y producidos por Roadmap. |
| [[reporte-users-contratos-y-endpoints]] | Users & Identity (Tema 01) | Endpoints de tokens M2M, perfiles de usuario y legajos. |
| [[08-comunicacion-gateway]] | API Gateway | Protocolo de ruteo, propagación de identidad y headers `X-*`. |
