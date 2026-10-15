---
tags: [tpi, g10, taiga, hu]
codigo: HU-57
ref: 8607
estado: "New"
responsable: "Sin asignar"
epicas: "[[epicas/EP-8633 Múltiples roadmaps por curso y grafo configurable|EP-8633]]"
sprint: "G10 - Sprint 03"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8607
---

# HU-57: Habilitar y gestionar varios roadmaps por curso

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8607) · Estado: **New** · Responsable: **Sin asignar** · Sprint: **G10 - Sprint 03**
> Épica: [[epicas/EP-8633 Múltiples roadmaps por curso y grafo configurable|EP-8633]] · Tareas cerradas: **0/4**

[G10] — HU-57 — Habilitar y gestionar varios roadmaps por curso
---------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: GESTOR / PROFESOR
*   **Quiero**: habilitar varios roadmaps en un curso y crearlos, renombrarlos y archivarlos
*   **Para**: organizar el curso en recorridos distintos

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Flag por curso `multiple_roadmaps_allowed`. Con el flag apagado no se puede crear un segundo roadmap. Archivar es baja lógica y conserva el progreso.
*   [ ] Validaciones: Nombre obligatorio y único dentro del curso.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): ADMIN, GESTOR o PROFESSOR dueño del curso.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Pantalla con componentes del kit.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El profesor dueño o el gestor activa varios roadmaps en un curso.
*   [ ] **CA2**: Con el flag apagado, crear un segundo roadmap devuelve 409.
*   [ ] **CA3**: Crear, renombrar y archivar un roadmap.
*   [ ] **CA4**: Archivar no borra el progreso de los alumnos.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Varios roadmaps por curso

**Escenario 1**

*   **Dado**: un curso con el flag apagado
*   **Cuando**: el profesor intenta crear un segundo roadmap
*   **Entonces**: recibe un error claro

**Escenario 2**

*   **Dado**: un curso con el flag encendido
*   **Cuando**: el profesor crea «Roadmap práctico»
*   **Entonces**: aparece en la lista del curso

**Escenario 3**

*   **Dado**: un roadmap con alumnos avanzados
*   **Cuando**: el profesor lo archiva
*   **Entonces**: deja de verse y el progreso se conserva

* * *

Prototipo
---------

*   **Capturas**: Lista de roadmaps del curso.
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-table`, `generic-modal`.
*   **Mock API / Swagger**: POST/PATCH /api/roadmap/courses/{courseId}/roadmaps.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 5
*   **Prioridad (MoSCoW / Numérica)**: Should

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 5 | Should |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Ninguno.
*   Módulos afectados: Controller y servicio de roadmaps, pantalla del profesor.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: Columna `multiple_roadmaps_allowed`.
*   Riesgos y mitigación (opcional): Ninguno abierto (P1 respondida el 2026-10-15).


## Tareas

- [ ] #9148 T-57.1 Habilitar varios roadmaps en un curso · New · Baltasar Rodriguez Teruel
- [ ] #9149 T-57.2 Crear, renombrar y archivar roadmaps · New · Baltasar Rodriguez Teruel
- [ ] #9150 T-57.3 Pantalla de roadmaps del curso para el profesor · New · Baltasar Rodriguez Teruel
- [ ] #9347 T-57.4 Wiki, OpenAPI y diagrama de secuencia · New · Quinteros Tomás
