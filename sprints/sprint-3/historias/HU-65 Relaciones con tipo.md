---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-65
estado: New
responsable: "Sin asignar"
epica: "Correcciones de los profes"
sprint: "G10 - Sprint 3"
puntos: 8
prioridad: Must
en_taiga: true
ref: 8614
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8614
responsables_tareas: ["Iker Alonso", "Mateo Delgado Costa", "Quinteros Tomás"]
tareas_cerradas: "1/5"
---

# HU-65: Relaciones con tipo

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Correcciones de los profes|Correcciones de los profes]] · Estado: **New** · Responsable de la historia: **Sin asignar** · Tareas: **1/5** · Sprint: **G10 - Sprint 3**
> Cargada en Taiga: [[taiga/historias/HU-65 Relaciones con tipo|HU-65]] ([abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8614)) · Épica en Taiga: [[epicas/EP-8631 Correcciones de los profes|EP-8631]] · Responsables de las tareas: [[sprints/sprint-3/12-responsables#Mateo Delgado Costa|Mateo Delgado Costa]] (2), [[sprints/sprint-3/12-responsables#Iker Alonso|Iker Alonso]] (2), [[sprints/sprint-3/12-responsables#Quinteros Tomás|Quinteros Tomás]] (1).

[G10] — HU-65 — Relaciones con tipo
-----------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: relacionar nodos y unidades con tipos de relación, ver el nombre de cada relación y elegir cuáles se muestran
*   **Para**: que el mapa muestre cómo se conectan los temas, no solo qué bloquea a qué

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Catálogo de 5 tipos (P4, DEC-018): `REQUIRES`, `RECOMMENDS`, `BELONGS_TO`, `RELATED_TO` y `PART_OF`. Solo `REQUIRES` afecta el desbloqueo; su condición es la regla AND/OR de HU-59 y el XP mínimo de HU-58, que acá no se redefinen. `RECOMMENDS` se muestra pero no bloquea. Cada tipo tiene nombre visible y visibilidad configurable.
*   [ ] Validaciones: No aplica.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): ADMIN, GESTOR o PROFESSOR dueño.
*   [ ] Accesibilidad (WCAG/teclado/lectores): La relación se distingue por texto y forma de línea, no solo por color.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Catálogo de tipos de relación con nombre y visibilidad.
*   [ ] **CA2**: La arista muestra el nombre del tipo.
*   [ ] **CA3**: El profesor oculta un tipo y deja de verse en el mapa.
*   [ ] **CA4**: Solo `REQUIRES` cambia el desbloqueo.
*   [ ] **CA5**: Una relación `REQUIRES` alimenta las reglas de HU-58 y HU-59 (no define una condición propia).

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Relaciones con tipo

**Escenario 1**  

*   **Dado**: dos nodos
*   **Cuando**: el profesor los une con `RELATED_TO`
*   **Entonces**: la arista dice «Relacionado con» y no bloquea nada

**Escenario 2**  

*   **Dado**: el tipo `BELONGS_TO` oculto
*   **Cuando**: el alumno abre el mapa
*   **Entonces**: no ve esas aristas

**Escenario 3**  

*   **Dado**: una relación `REQUIRES`
*   **Cuando**: el alumno no completó el origen
*   **Entonces**: el destino sigue bloqueado

* * *

Prototipo
---------

*   **Capturas**: Aristas con etiqueta en el grafo.
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-node-graph`.
*   **Mock API / Swagger**: Tipos de relación en `/roadmaps/{id}/graph`.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 8
*   **Prioridad (MoSCoW / Numérica)**: Must

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 8 | Must |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Ninguno.
*   Módulos afectados: Módulo graph, vista de grafo, mapa del alumno.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: Tipo de relación y visibilidad por tipo en Postgres (`node_prerequisite`, `section_prerequisite`, T-65.5), proyectados a Neo4j (DEC-021).
*   Riesgos y mitigación (opcional): Ninguno abierto (P4 respondida el 2026-10-15).

## Tareas

> [!info] Espejo de Taiga (sync 2026-10-15). Cerradas: **1/5**. Historia en Taiga: [[taiga/historias/HU-65 Relaciones con tipo|HU-65]] · [abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8614)

- [x] [#9193](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9193) **T-65.1 Catálogo de los 5 tipos de relación** · Back · Closed · [[sprints/sprint-3/12-responsables#Iker Alonso|Iker Alonso]]
    - **Qué:** `requires`, `recommends`, `belongs_to`, `related_to` y `part_of` (DEC-018), cada uno con `label` y `visible`. Solo `requires` afecta el desbloqueo, usando las reglas de HU-58 y HU-59.
    - **Dónde:** módulo `graph`.
    - **Listo cuando:** hay tests de que solo `requires` cambia el desbloqueo.
- [ ] [#9195](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9195) **T-65.2 Ver el nombre de cada relación y ocultar tipos** · Front · New · [[sprints/sprint-3/12-responsables#Mateo Delgado Costa|Mateo Delgado Costa]]
    - **Qué:** la arista muestra el nombre del tipo y se distingue por texto y forma de línea (no solo color); el profesor puede ocultar un tipo en el mapa.
    - **Listo cuando:** ocultar un tipo lo saca del mapa del alumno.
- [ ] [#9197](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9197) **T-65.3 Elegir el tipo al crear una relación** · Front · New · [[sprints/sprint-3/12-responsables#Mateo Delgado Costa|Mateo Delgado Costa]]
    - **Qué:** al crear una relación (desde el editor o arrastrando, HU-62) se elige el tipo; en `requires` la condición se arma con el editor de reglas de HU-58/HU-59.
    - **Listo cuando:** el profesor crea una relación de cada tipo.
- [ ] [#9353](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9353) **T-65.4 Wiki, OpenAPI y diagrama de secuencia** · New · [[sprints/sprint-3/12-responsables#Quinteros Tomás|Quinteros Tomás]]
    - Tarea de documentación agregada en Taiga por el equipo; no estaba en la propuesta.
- [ ] [#10591](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/10591) **T-65.5 Guardar el tipo de relación en Postgres y aceptarlo en la API** · Back · New · [[sprints/sprint-3/12-responsables#Iker Alonso|Iker Alonso]]
    - **Qué:** migración que agrega `relation_type` a `node_prerequisite` y `section_prerequisite` (valores del catálogo de T-65.1, por defecto `REQUIRES`) y la visibilidad por tipo. Los endpoints de prerrequisitos aceptan y devuelven el tipo, y rechazan con 400 los tipos fuera del catálogo. Solo `REQUIRES` cuenta para el desbloqueo.
    - **Por qué:** Postgres es la fuente de verdad y Neo4j se proyecta desde ahí ([[decisiones/DEC-021-postgres-fuente-de-verdad-neo4j-proyeccion|DEC-021]]). Sin el tipo en Postgres, el proyector no puede copiarlo.
    - **Listo cuando:** las relaciones existentes quedan como `REQUIRES`, se puede crear una relación de cada tipo por la API, y hay tests de que solo `REQUIRES` cambia el desbloqueo.
    - **Bloquea:** T-18.2, T-65.2 y T-65.3. Agregada el 2026-10-17 por el cambio de diseño de DEC-021.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Solo existe la relación "prerrequisito" con modo AND/OR. El catálogo de los 5 tipos (`RelationType`, T-65.1) existe solo en el módulo `graph` de Neo4j; en Postgres las tablas de prerrequisitos no tienen tipo, y eso lo resuelve T-65.5.

> [!tip] Para T-65.2 y T-65.3 (front)
> El tipo se elige y se lee por los endpoints de prerrequisitos que ya existen (`POST /nodes/{nodeId}/prerequisites` y los de sección), que con T-65.5 aceptan y devuelven `relation_type`. No hay una ruta aparte que escriba en Neo4j (DEC-021).

### Depende de

- [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial|HT-18]] Módulo graph en Neo4j y migración inicial
- [[decisiones/DEC-021-postgres-fuente-de-verdad-neo4j-proyeccion|DEC-021]] Postgres es la fuente de verdad y Neo4j es una proyección
- [[sprints/sprint-3/historias/HU-59 Dependencias entre nodos con reglas combinadas|HU-59]] Dependencias entre nodos con reglas combinadas (para la condición de `REQUIRES`)

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|P4]] 5 tipos: `requires`, `recommends`, `belongs_to`, `related_to` y `part_of`.
