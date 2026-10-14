---
tags: [tpi, g10, taiga, epica]
ref: 144
estado: "New"
responsable: "Gabriela Camacho"
avance: "7/7"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/144
---

# EP-144: Esqueleto del servicio Roadmap — TRANSVERSAL (v3)

> [!info] Generado desde Taiga (2026-10-14 20:45). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/144) · Estado: **New** · Responsable: **Gabriela Camacho** · HU cerradas: **7/7**

[G10] — Esqueleto del servicio Roadmap — TRANSVERSAL (v3)
---------------------------------------------------------

* * *

Objetivo
--------

Agrupar las historias técnicas transversales del servicio, que en el alcance v3 **no constituyen una épica de negocio**: HT-01 (esqueleto del servicio, modelo base y despliegue con un comando), HT-02 (semilla de datos y guion de demostración) y HT-03 (acordar y simular los contratos de Inventario y de Courses).

* * *

Suposiciones y Restricciones
----------------------------

*   Suposiciones: las historias técnicas se identifican como Transversales en el backlog, no cuelgan de ninguna épica G10-E1 a G10-E8. HT-03 es habilitante: sin los contratos acordados y simulados, el gate no tiene contra qué probarse y HU-04, HU-06, HU-11 y HU-15 no pueden desarrollarse desde el día uno.
*   Restricciones (legales/técnicas): los contratos con otros equipos se acuerdan por escrito y se simulan, no se inventan. A Notificaciones se le pide topic de resultados, topic de eventos propios, key, producer id, DLQ y reintentos (P-09). El consumo del bus usa group-id roadmap-service, JsonDeserializer con trusted.packages del dominio y auto-offset-reset earliest, absorbiendo los replays por idempotencia.

* * *

Criterios de Aceptación a nivel Épico
-------------------------------------

*   [ ] El servicio se levanta con un comando, con su modelo base creado y la semilla de datos cargada, y el guion de demostración corre de punta a punta contra los contratos simulados.
*   [ ] KPIs iniciales: ningún KPI de producto aplica. El indicador propio es que un integrante nuevo levanta el entorno completo sin asistencia.
*   [ ] Sin regresiones críticas: el despliegue con un comando sigue funcionando después de cada cambio de modelo.
*   [ ] Observabilidad y alertas: health check del servicio y del consumidor de Kafka, con la DLQ monitoreada según P-09.
*   [ ] Documentación publicada: página de Wiki con el procedimiento de despliegue, la semilla de datos y los contratos simulados de Inventario y Courses.

* * *

Dependencias / Impactos
-----------------------

*   Servicios / APIs: event-bus (bootstrap event-bus:29092 vía KAFKA\_BOOTSTRAP), API Gateway, más los contratos simulados de Inventario, Courses y Motor de Desafíos.
*   Módulos afectados: esqueleto del servicio, modelo de datos base, semilla, despliegue, consumidor Kafka.
*   Otros equipos: Notificaciones debe confirmar topic, key, producer id, DLQ y reintentos (P-09). Inventario y Courses deben acordar sus contratos por escrito, pedido para el día 3 del Sprint 1.
*   Impacto en datos / migraciones: creación del esquema base y carga de la semilla de demostración. Sin datos productivos que migrar.
*   Feature toggles / flags: no aplica. Es infraestructura del servicio, no funcionalidad de negocio.


## Historias

| HU | Estado | Responsable | Sprint | Tareas |
|---|---|---|---|---|
| [[historias/HT-01 Esqueleto del servicio, modelo base y despliegue con un comando\|HT-01]] Esqueleto del servicio, modelo base y despliegue con un comando | Done | Lautaro Jesus Diego | G10 - Sprint 1 | 17/17 |
| [[historias/HT-02 Semilla de datos y guion de demostración\|HT-02]] Semilla de datos y guion de demostración | Done | Stefano Zoffoli | G10 - Sprint 1 | 2/2 |
| [[historias/HT-03 Acordar y simular contratos de Inventario y Courses (más solicitud al bus)\|HT-03]] Acordar y simular contratos de Inventario y Courses (más solicitud al bus) | Done | Sin asignar | G10 - Sprint 1 | 7/7 |
| [[historias/US-3572 Servicio roadmap-service operativo y descubrible\|US-3572]] Servicio roadmap-service operativo y descubrible | Done | Mateo Delgado Costa | G10 - Sprint 1 | 1/1 |
| [[historias/HT-06 Recorrido simulado MVP e integración con el catálogo del Motor\|HT-06]] Recorrido simulado MVP e integración con el catálogo del Motor | Done | Iker Alonso | G10 - Sprint 1 | 8/8 |
| [[historias/HT-08 Optimizar los modelos GLB del mundo 3D\|HT-08]] Optimizar los modelos GLB del mundo 3D | Done | Baltasar Rodriguez Teruel | G10 - Sprint 2 | 9/9 |
| [[historias/HT-09 Eliminar simulaciones y datos de ejemplo del microservicio\|HT-09]] Eliminar simulaciones y datos de ejemplo del microservicio | Done | Stefano Zoffoli | G10 - Sprint 2 | 7/7 |
