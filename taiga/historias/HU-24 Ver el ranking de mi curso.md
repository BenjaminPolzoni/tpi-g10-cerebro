---
tags: [tpi, g10, taiga, hu]
codigo: HU-24
ref: 4241
estado: "Done"
responsable: "Lorenzo Araujo"
epicas: "[[epicas/EP-61 Ranking y cierre académico|EP-61]]"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4241
---

# HU-24: Ver el ranking de mi curso

> [!info] Generado desde Taiga (2026-10-14 20:44). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4241) · Estado: **Done** · Responsable: **Lorenzo Araujo** · Sprint: **G10 - Sprint 2**
> Épica: [[epicas/EP-61 Ranking y cierre académico|EP-61]] · Tareas cerradas: **6/6**

[G10] — HU-24 — Ver el ranking de mi curso
------------------------------------------


* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: ver mi posición en el ranking de mi cohorte por XP
*   **Para**: saber cómo voy respecto de mis compañeros


* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: El ranking es por cohorte. Orden por total_xp descendente con desempate de HU-25. El alumno ve top 3, últimos 3, cortes P90/P10 anónimos y su fila identificada; PROFESSOR y ADMIN ven a todos identificados. Percentiles solo con 10 o más inscriptos.
*   [ ] Seguridad (roles, permisos, datos sensibles): El anonimato se resuelve en el servidor (RF-RNK-03), nunca en el front.
*   [ ] Otros: Portar ranking.rules.ts a Java con los mismos casos de prueba. Dependencias / impactos: Servicios: G07 — Users (perfiles por lote). Relacionadas: HU-25, HU-45, HU-21. Preguntas abiertas: P-19, P-28.


* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El alumno ve su posición dentro de su cohorte.
*   [ ] **CA2**: El alumno nunca recibe nombres de otros fuera de lo permitido.
*   [ ] **CA3**: El profesor ve el ranking identificado.
*   [ ] **CA4**: Con menos de 10 inscriptos no se muestran percentiles.
*   [ ] **CA5**: El front usa el backend (HttpRankingAdapter) y no la semilla.


* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Ranking del curso con anonimato

**Escenario 1**  

*   **Dado**: una cohorte con 12 alumnos
*   **Cuando**: un alumno abre el ranking
*   **Entonces**: ve su fila, top 3, últimos 3 y cortes anónimos

**Escenario 2**  

*   **Dado**: la misma cohorte
*   **Cuando**: el profesor abre el ranking
*   **Entonces**: ve a los 12 identificados

**Escenario 3**  

*   **Dado**: una cohorte con 8 alumnos
*   **Cuando**: se abre el ranking
*   **Entonces**: no se muestran percentiles

* * *
Prototipo
---------

*   **Capturas**: Pendiente.
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente.
*   **Mock API / Swagger**: GET /api/roadmap/courses/{courseId}/ranking (convención del back); ranking-page existente.


## Tareas

- [x] #4289 T-24.1 GET .../ranking con respuesta por rol · Closed · Lorenzo Araujo
- [x] #4290 T-24.2 Consulta ordenada por total_xp con percentiles y zonas (port de ranking.rules.ts) · Closed · Lorenzo Araujo
- [x] #4291 T-24.3 Perfiles de G07 con fallback «Estudiante #NN» · Closed · Lorenzo Araujo
- [x] #4292 T-24.4 HttpRankingAdapter y quitar InMemoryRoadmapAdapter de ranking.routes.ts · Closed · Lorenzo Araujo
- [x] #4293 T-24.5 Tests de anonimato en el servidor y BDD · Closed · Lorenzo Araujo
- [x] #5388 T-24.6 Wiki, OpenAPI y diagrama de secuencia · Closed · Quinteros Tomás
