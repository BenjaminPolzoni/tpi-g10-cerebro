---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-46
estado: Propuesta
responsable: ""
epica: "Deuda del Sprint 2"
sprint: "G10 - Sprint 3"
puntos: 5
prioridad: Should
en_taiga: true
---

# HU-46: Ver en los nodos y en el Templo el material teórico de Courses

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Deuda del Sprint 2|Deuda del Sprint 2]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Ya existe en Taiga: [[taiga/historias/HU-46 Ver en los nodos y en el Templo el material teórico de Courses|HU-46]] (épica EP-593). En el Sprint 3 se **reabre** con lo que falta.

[G10] — HU-46 — Ver en los nodos y en el Templo el material teórico de Courses
------------------------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: ver en el Templo todo el material teórico de mi curso agrupado por unidad
*   **Para**: repasar sin recorrer el mapa nodo por nodo

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: El material lo guarda Courses en Garage y Roadmap lo pide (D-03); Roadmap no guarda archivos. En una unidad bloqueada el material se lista pero no se puede abrir.
*   [ ] Validaciones: No aplica.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): Solo el alumno matriculado.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Lista navegable con teclado; los ítems bloqueados indican el motivo en texto.
*   [ ] Otros: Si el PO prefiere no rehacerlo, se redefine el criterio de aceptación de HU-46 en Taiga (P13).

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Página Templo (`/student/materials`) con el material agrupado por unidad.
*   [ ] **CA2**: En una unidad bloqueada el material aparece sin poder abrirse.
*   [ ] **CA3**: Abrir un material desbloqueado lo muestra en el visor.
*   [ ] **CA4**: O el CA de HU-46 queda redefinido en Taiga.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Templo de materiales

**Escenario 1**  

*   **Dado**: un alumno con 2 unidades desbloqueadas
*   **Cuando**: abre el Templo
*   **Entonces**: ve el material de ambas agrupado por unidad

**Escenario 2**  

*   **Dado**: una unidad bloqueada
*   **Cuando**: el alumno la mira en el Templo
*   **Entonces**: ve el material listado sin poder abrirlo

**Escenario 3**  

*   **Dado**: un material desbloqueado
*   **Cuando**: lo abre
*   **Entonces**: se muestra en el visor

* * *

Prototipo
---------

*   **Capturas**: Templo del mundo (antes `materials-page`).
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-course-outline`.
*   **Mock API / Swagger**: GET /api/roadmap/courses/{courseId}/materials.

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

*   Servicios involucrados: Courses (material en Garage).
*   Módulos afectados: Página Templo (front), `UnitMaterialService`.
*   Otros equipos / aprobaciones: G01 (URLs del material).
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Que el PO no lo quiera; mitigación: preguntar antes (P13).

## Tareas

- [ ] T-46.6 Confirmar con el PO (P13)
- [ ] T-46.7 Página Templo con la UI-KIT
- [ ] T-46.8 Estados bloqueado y desbloqueado
- [ ] T-46.9 Tests

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Se borró la página Templo (`student/materials`). El material de los nodos sí se ve.

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P13]]
