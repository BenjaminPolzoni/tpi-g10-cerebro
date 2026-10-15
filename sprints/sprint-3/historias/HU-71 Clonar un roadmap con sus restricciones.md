---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-71
estado: New
responsable: "Sin asignar"
epica: "Múltiples roadmaps por curso y grafo configurable"
sprint: "G10 - Sprint 3"
puntos: 8
prioridad: Should
en_taiga: true
ref: 8619
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8619
responsables_tareas: ["Baltasar Rodriguez Teruel", "Quinteros Tomás"]
tareas_cerradas: "0/4"
---

# HU-71: Clonar un roadmap con sus restricciones

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Múltiples roadmaps por curso y grafo configurable|Múltiples roadmaps por curso y grafo configurable]] · Estado: **New** · Responsable de la historia: **Sin asignar** · Tareas: **0/4** · Sprint: **G10 - Sprint 3**
> Cargada en Taiga: [[taiga/historias/HU-71 Clonar un roadmap con sus restricciones|HU-71]] ([abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8619)) · Épica en Taiga: [[epicas/EP-8633 Múltiples roadmaps por curso y grafo configurable|EP-8633]] · Responsables de las tareas: [[sprints/sprint-3/12-responsables#Baltasar Rodriguez Teruel|Baltasar Rodriguez Teruel]] (3), [[sprints/sprint-3/12-responsables#Quinteros Tomás|Quinteros Tomás]] (1). Sale de la respuesta a G4 (2026-10-15).

[G10] — HU-71 — Clonar un roadmap con sus restricciones
-------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR / GESTOR
*   **Quiero**: clonar un roadmap con su estructura, sus reglas y sus restricciones para otra comisión del curso o para otro curso
*   **Para**: reusar un recorrido ya armado sin rehacerlo a mano

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: La copia lleva secciones, subsecciones, nodos (con `START`/`END`), relaciones con tipo, reglas de desbloqueo, restricciones y la configuración del roadmap (DEC-017). Todos los ids de la copia son nuevos: el `node_id` es único global también después de clonar (G8). No se copia el progreso de los alumnos.
*   [ ] Validaciones: Nombre obligatorio y único dentro del curso destino. El destino tiene que ser un curso o una comisión activos.
*   [ ] Datos obligatorios: Roadmap de origen, curso destino y nombre de la copia. La comisión destino es opcional.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): ADMIN, GESTOR o PROFESSOR dueño del curso de origen y del de destino.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Diálogo de clonado con componentes del kit, usable con teclado.
*   [ ] Otros: Si falla la escritura en Neo4j, no queda una copia a medias (la copia parcial se da de baja lógica). Con un roadmap que usa secciones de Courses y se clona a otro curso, falta definir qué pasa con ese vínculo (P17).

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El profesor clona un roadmap a otra comisión del mismo curso o a otro curso.
*   [ ] **CA2**: La copia tiene la misma estructura, relaciones, reglas, restricciones y configuración que el original.
*   [ ] **CA3**: Todos los ids de la copia son nuevos y no chocan con los del original.
*   [ ] **CA4**: La copia arranca sin progreso de alumnos.
*   [ ] **CA5**: Sin permiso sobre el curso de destino, la operación devuelve 403.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Clonar un roadmap

**Escenario 1**  

*   **Dado**: un roadmap con 2 secciones, reglas `requires` y una restricción por fecha
*   **Cuando**: el profesor lo clona para la comisión 2w2
*   **Entonces**: la comisión 2w2 tiene un roadmap igual, con las mismas reglas y la misma restricción

**Escenario 2**  

*   **Dado**: un roadmap clonado
*   **Cuando**: el Motor manda el cierre de un intento con el `id_node` de la copia
*   **Entonces**: el progreso se registra en la copia y no en el original

**Escenario 3**  

*   **Dado**: un profesor que no es dueño del curso de destino
*   **Cuando**: intenta clonar un roadmap hacia ese curso
*   **Entonces**: recibe 403 y no se crea nada

* * *

Prototipo
---------

*   **Capturas**: Acción «Clonar» en la pantalla de roadmaps del curso (HU-57).
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-modal`, `generic-select`, `generic-input`.
*   **Mock API / Swagger**: POST /api/roadmap/roadmaps/{roadmapId}/clone con `target_course_id`, `target_group_id` (opcional) y `name`.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 8
*   **Prioridad (MoSCoW / Numérica)**: Should

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 8 | Should |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Courses (validar el curso y la comisión de destino).
*   Módulos afectados: Módulo `graph` (copia del subgrafo), roadmaps del curso, pantalla del profesor.
*   Otros equipos / aprobaciones: G01, solo si se clona a otro curso un roadmap con secciones de Courses (P17).
*   Impacto en datos / migraciones: Sin migración. La copia es un subgrafo nuevo en Neo4j.
*   Riesgos y mitigación (opcional): Copiar en dos bases sin transacción común; mitigación: escribir primero en Neo4j y dar de baja lógica la copia si algo falla (DEC-016).

## Tareas

> [!info] Espejo de Taiga (sync 2026-10-15). Cerradas: **0/4**. Historia en Taiga: [[taiga/historias/HU-71 Clonar un roadmap con sus restricciones|HU-71]] · [abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8619)

- [ ] [#9169](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9169) **T-71.1 Copiar un roadmap con ids nuevos** · Back · New · [[sprints/sprint-3/12-responsables#Baltasar Rodriguez Teruel|Baltasar Rodriguez Teruel]]
    - **Qué:** copia del subgrafo completo (secciones, subsecciones, nodos con inicio y fin, relaciones, reglas, restricciones y configuración) generando ids nuevos (G8) y sin progreso de alumnos. Si algo falla, lo copiado se da de baja lógica.
    - **Dónde:** módulo `graph`.
    - **Listo cuando:** la copia es igual al original salvo los ids, y un evento del Motor sobre la copia suma en la copia.
- [ ] [#9170](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9170) **T-71.2 Endpoint de clonado con permisos** · Back · New · [[sprints/sprint-3/12-responsables#Baltasar Rodriguez Teruel|Baltasar Rodriguez Teruel]]
    - **Qué:** `POST /roadmaps/{roadmapId}/clone` con `target_course_id`, `target_group_id` (opcional) y `name`. Solo el dueño de los dos cursos; nombre único en el curso destino.
    - **Listo cuando:** sin permiso devuelve 403 y no crea nada. Hay tests.
- [ ] [#9171](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9171) **T-71.3 Acción «Clonar» en la pantalla del profesor** · Front · New · [[sprints/sprint-3/12-responsables#Baltasar Rodriguez Teruel|Baltasar Rodriguez Teruel]]
    - **Qué:** en la pantalla de roadmaps (HU-57), un diálogo para elegir curso y comisión destino y el nombre de la copia.
    - **Listo cuando:** el profesor clona un roadmap a otra comisión sin ayuda.
- [ ] [#9354](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9354) **T-71.4 Wiki, OpenAPI y diagrama de secuencia** · New · [[sprints/sprint-3/12-responsables#Quinteros Tomás|Quinteros Tomás]]
    - Tarea de documentación agregada en Taiga por el equipo; no estaba en la propuesta.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

No existe el clonado. Un curso tiene un único roadmap.

### Depende de

- [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial|HT-18]] Módulo graph en Neo4j y migración inicial
- [[sprints/sprint-3/historias/HU-57 Habilitar y gestionar varios roadmaps por curso|HU-57]] Habilitar y gestionar varios roadmaps por curso

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|G4]] El profesor define las restricciones de cada roadmap y puede clonarlo con ellas para otro grupo o curso.
- ✅ [[sprints/sprint-3/08-dudas|G8]] `node_id` único global; clonar genera ids nuevos.

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P17]] Clonar a otro curso un roadmap que usa secciones de Courses: ¿se vuelven a vincular con las secciones del curso destino o pasan a ser propias?
