---
tags: [tpi, g10, taiga, epica]
ref: 4232
estado: "New"
responsable: "Sin asignar"
avance: "3/3"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/4232
---

# EP-4232: Edición del roadmap por el profesor

> [!info] Generado desde Taiga (2026-10-14 20:45). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/4232) · Estado: **New** · Responsable: **Sin asignar** · HU cerradas: **3/3**

[G10] — Edición del roadmap por el profesor
-------------------------------------------

* * *

Objetivo
--------

Que el PROFESOR edite el roadmap nodo por nodo y personalice cómo se ve cada desafío, sobre el grafo ya creado en HU-01, sin que ningún alumno pierda progreso ni desbloqueos.

* * *

Suposiciones y Restricciones
----------------------------

*   Suposiciones: HU-01, HU-11 y HU-13 están Done; el backend expone la edición de nodos, la obligatoriedad y las reglas; las unidades vienen de Courses (HU-37) y no se crean acá.
*   Restricciones (legales/técnicas): edición permitida aun con el curso activo (RF-CUR-05). Los cambios rigen hacia adelante y no revierten desbloqueos (RF-CFG-06). Baja lógica (RF-NFR-01). Solo el PROFESSOR dueño del curso. 100 % escritorio (RF-NFR-05).

* * *

Criterios de Aceptación a nivel Épico
-------------------------------------

*   [ ] El profesor edita un nodo (referencia, obligatoriedad, reintentos, reglas, ícono) y el cambio se refleja en el gate y en el recorrido del alumno sin revertir desbloqueos.
*   [ ] KPIs iniciales: ningún KPI de producto aplica. El indicador propio es el tiempo de guardado de una edición, menos de 300 ms, visible en la próxima consulta del gate.
*   [ ] Sin regresiones críticas en E3: editar un nodo no altera ningún movimiento de XP existente ni revierte desbloqueos ya alcanzados.
*   [ ] Observabilidad y alertas: log de edición con autor, fecha, nodo, campos y cantidad de alumnos afectados.
*   [ ] Documentación publicada: la Wiki con los campos editables y los endpoints en OpenAPI.

* * *

Dependencias / Impactos
-----------------------

*   Servicios / APIs: Motor de Desafíos (catálogo de desafíos), Courses (contenido), API Gateway.
*   Módulos afectados: GraphService, evaluador del gate, editor del front (compartido con HU-37).
*   Otros equipos: sin bloqueante propio; el material de lectura depende de lo que defina Courses.
*   Impacto en datos / migraciones: campo icon\_key nullable en nodo (migración nueva, número a asignar tras V16) y los campos del editor que hoy solo viven en el front, según se decida (P-23, P-24).
*   Feature toggles / flags: ninguno propuesto.
*   Historias previstas: HU-41, HU-43. Alternativa a esta épica nueva: reabrir E1 (Estructura del roadmap como grafo de nodos), a decidir en el planning.


## Historias

| HU | Estado | Responsable | Sprint | Tareas |
|---|---|---|---|---|
| [[historias/HU-41 Editar un nodo del roadmap de forma individual\|HU-41]] Editar un nodo del roadmap de forma individual | Done | Stefano Zoffoli | G10 - Sprint 2 | 6/6 |
| [[historias/HU-43 Elegir el ícono de un desafío\|HU-43]] Elegir el ícono de un desafío | Done | Gabriela Camacho | G10 - Sprint 2 | 6/6 |
| [[historias/HU-47 Asignar a un nodo un desafío de mi pool del Motor\|HU-47]] Asignar a un nodo un desafío de mi pool del Motor | Done | Mateo Delgado Costa | Backlog | 5/14 |
