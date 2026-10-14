---
tags: [tpi, g10, taiga, hu]
codigo: HU-38
ref: 4240
estado: "Done"
responsable: "Benjamin Polzoni"
epica: "[G10] — Niveles por curso"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4240
---

# HU-38: Ver mi nivel en el curso y cuánto me falta para el siguiente

> [!info] Generado desde Taiga (2026-10-14 18:47). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4240) · Estado: **Done** · Responsable: **Benjamin Polzoni** · Sprint: **G10 - Sprint 2**

[G10] — HU-38 — Ver mi nivel en el curso y cuánto me falta para el siguiente
----------------------------------------------------------------------------


* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: ver mi nivel en el curso y cuánto XP me falta para el siguiente
*   **Para**: tener una meta concreta mientras avanzo


* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: El nivel se calcula desde student_course.total_xp con umbrales configurables (parámetro externo, no fijo en código). En el último nivel se muestra «nivel máximo».
*   [ ] Otros: Reemplaza el cálculo local de node-level.ts en el front. El evento COURSE_LEVEL_UP queda para HU-39. Dependencias / impactos: Relacionadas: HU-03 (XP, Done), HU-39 (evento). Preguntas abiertas: —


* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El alumno ve su nivel y el XP que le falta.
*   [ ] **CA2**: Con XP justo en un umbral ve el nivel nuevo.
*   [ ] **CA3**: En el último nivel ve «nivel máximo».


* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Nivel derivado del XP

**Escenario 1**  

*   **Dado**: un alumno con 450 XP y umbral de nivel 2 en 500
*   **Cuando**: abre su HUD
*   **Entonces**: ve nivel 1 y «faltan 50 XP»

**Escenario 2**  

*   **Dado**: un alumno con 500 XP
*   **Cuando**: abre su HUD
*   **Entonces**: ve nivel 2

**Escenario 3**  

*   **Dado**: un alumno en el último nivel
*   **Cuando**: abre su HUD
*   **Entonces**: ve «nivel máximo»

* * *
Prototipo
---------

*   **Capturas**: Pendiente.
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente.
*   **Mock API / Swagger**: GET /api/roadmap/courses/{courseId}/students/me/level (propuesta).


## Tareas

- [x] #4285 T-38.1 Regla de nivel desde total_xp con umbrales configurables · Closed · Benjamin Polzoni
- [x] #4286 T-38.2 Endpoint de nivel del alumno · Closed · Benjamin Polzoni
- [x] #4287 T-38.3 HUD con el nivel del backend (reemplaza node-level.ts) · Closed · Benjamin Polzoni
- [x] #4288 T-38.4 BDD niveles (umbral exacto y último nivel) · Closed · Benjamin Polzoni
- [x] #5387 T-38.5 Wiki, OpenAPI y diagrama de secuencia · Closed · Quinteros Tomás
