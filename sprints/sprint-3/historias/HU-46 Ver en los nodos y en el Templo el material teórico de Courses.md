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

> [!warning] 2026-10-15: el Templo no existe más (P13)
> No se rehace. Queda redefinir el CA de HU-46 en Taiga para que cubra solo el material en los nodos, que ya funciona.

[G10] — HU-46 — Ver en los nodos y en el Templo el material teórico de Courses
------------------------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: ver desde los nodos el material teórico de mi curso
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
*   [ ] Otros: El Templo no existe más (P13): se redefine el criterio de aceptación de HU-46 en Taiga.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: ~~Página Templo (`/student/materials`) con el material agrupado por unidad.~~ Descartado: el Templo no existe más (P13).
*   [ ] **CA2**: En una unidad bloqueada el material aparece sin poder abrirse.
*   [ ] **CA3**: Abrir un material desbloqueado lo muestra en el visor.
*   [ ] **CA4**: El CA de HU-46 queda redefinido en Taiga, sin el Templo.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Material teórico en los nodos

**Escenario 1**  

*   **Dado**: un alumno con 2 unidades desbloqueadas
*   **Cuando**: abre sus nodos de contenido
*   **Entonces**: ve el material de ambas

**Escenario 2**  

*   **Dado**: una unidad bloqueada
*   **Cuando**: el alumno la mira en el mapa
*   **Entonces**: ve el material listado sin poder abrirlo

**Escenario 3**  

*   **Dado**: un material desbloqueado
*   **Cuando**: lo abre
*   **Entonces**: se muestra en el visor

* * *

Prototipo
---------

*   **Capturas**: Material dentro del nodo.
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
*   Módulos afectados: `UnitMaterialService`.
*   Otros equipos / aprobaciones: G01 (URLs del material).
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Que el PO no lo quiera; mitigación: preguntar antes (P13).

## Tareas

- [x] T-46.6 Confirmar con el PO (P13: el Templo no existe más)
- [ ] ~~T-46.7 Página Templo con la UI-KIT~~ (descartada)
- [ ] T-46.10 Redefinir el CA de HU-46 en Taiga
- [ ] T-46.8 Estados bloqueado y desbloqueado
- [ ] T-46.9 Tests

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Se borró la página Templo (`student/materials`). El material de los nodos sí se ve.

### Depende de

Nada: se puede empezar ya.

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|P13]] El Templo no existe más: no se rehace.
