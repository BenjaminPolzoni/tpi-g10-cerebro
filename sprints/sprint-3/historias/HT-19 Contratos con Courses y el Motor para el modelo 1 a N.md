---
tags: [tpi, g10, sprint-3, ht]
codigo: HT-19
estado: Propuesta
responsable: ""
epica: "Múltiples roadmaps por curso y grafo configurable"
sprint: "G10 - Sprint 3"
puntos: 5
prioridad: Must
en_taiga: false
---

# HT-19: Contratos con Courses y el Motor para el modelo 1 a N

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Múltiples roadmaps por curso y grafo configurable|Múltiples roadmaps por curso y grafo configurable]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga.

[G10] — HT-19 — Contratos con Courses y el Motor para el modelo 1 a N
---------------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: adaptar los contratos con Courses y con el Motor al modelo de varios roadmaps por curso
*   **Para**: que las integraciones sigan funcionando cuando un curso tenga N roadmaps

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Hoy cada sección se sincroniza con una sección de Courses (HU-36) y el Motor manda `id_course` + `id_node`.
*   [ ] Validaciones: No aplica.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): No aplica.
*   [ ] Otros: Los acuerdos se registran en `acuerdos/` y los contratos en `tpi-roadmap/docs/contracts/`.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Contrato con G01 para N roadmaps: el profesor elige por roadmap secciones de Courses o propias (P3) y define las restricciones de cada roadmap, que se copian al clonarlo (G4).
*   [ ] **CA2**: `node_id` único global, también en los roadmaps clonados (G8, confirmado el 2026-10-15).
*   [ ] **CA3**: Código y contratos actualizados.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Contratos para N roadmaps

**Escenario 1**  

*   **Dado**: un curso con 2 roadmaps
*   **Cuando**: Courses publica una sección nueva
*   **Entonces**: llega al roadmap acordado

**Escenario 2**  

*   **Dado**: un nodo del roadmap 2
*   **Cuando**: el Motor manda el resultado con `id_node`
*   **Entonces**: se registra en el roadmap correcto

**Escenario 3**  

*   **Dado**: el acuerdo con G01
*   **Cuando**: se registra
*   **Entonces**: queda en `acuerdos/courses-g01`

* * *

Prototipo
---------

*   **Capturas**: No aplica (sin pantalla).
*   **URL Figma**: No aplica.
*   **Storybook**: No aplica.
*   **Mock API / Swagger**: No aplica.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 5
*   **Prioridad (MoSCoW / Numérica)**: Must

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 5 | Must |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Courses, Motor.
*   Módulos afectados: Sync de secciones, listener del Motor.
*   Otros equipos / aprobaciones: G01, G09.
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Que G01 tarde en acordar; mitigación: proponer el mapeo por escrito la primera semana.

## Tareas

- [ ] **T-19.1 Proponerle a Courses (G01) cómo se usan sus secciones con varios roadmaps** · Coordinación
    - **Qué:** escribir y mandar a G01: cada roadmap elige si usa secciones de Courses o propias (P3); el sync de secciones (HU-36) solo toca los roadmaps que usan secciones de Courses; las restricciones se definen por roadmap y se copian al clonar (G4).
    - **Listo cuando:** G01 respondió y el acuerdo está en `acuerdos/courses-g01`.
- [x] **T-19.2 Confirmar con el Motor (G09) que `node_id` alcanza** · Coordinación
    - Hecho el 2026-10-15 (G8): `node_id` es único global, también después de clonar.
- [ ] **T-19.3 Sincronizar secciones solo en los roadmaps que las usan** · Back
    - **Qué:** que el sync de secciones de Courses actúe solo sobre los roadmaps marcados para usar secciones de Courses, según el acuerdo de T-19.1.
    - **Dónde:** `CourseSectionSyncService`, `CourseSectionsReconciliationService`.
    - **Listo cuando:** en un curso con un roadmap de secciones de Courses y otro de secciones propias, el sync solo cambia el primero. Hay test.
- [ ] **T-19.4 Ubicar el roadmap correcto en los eventos del Motor** · Back
    - **Qué:** `RoadmapEventListener` encuentra el roadmap a partir del `id_node` en vez de suponer un roadmap por curso.
    - **Listo cuando:** el cierre de un intento de un nodo del segundo roadmap suma en ese roadmap. Hay test.
- [ ] **T-19.5 Actualizar los contratos escritos** · Docs
    - **Qué:** `docs/contracts/courses.md` y `motor-desafios-evento-cierre.md` describen el modelo de varios roadmaps por curso.
    - **Listo cuando:** los dos contratos coinciden con el código.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Cada sección del roadmap se sincroniza con una sección de Courses (HU-36). El Motor manda `id_course` + `id_node`.

### Depende de

- [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps|HT-17]] Modelo 1 a N de curso a roadmaps

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|P3]] Secciones de Courses o propias: lo configura el profesor.
- ✅ [[sprints/sprint-3/08-dudas|G4]] El profesor define las restricciones de cada roadmap y puede clonarlo con ellas para otro grupo o curso.
- ✅ [[sprints/sprint-3/08-dudas|G8]] Sí: `node_id` único global; clonar genera ids nuevos.
