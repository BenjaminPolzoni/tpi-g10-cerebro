---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-59
estado: New
responsable: "Sin asignar"
epica: "Múltiples roadmaps por curso y grafo configurable"
sprint: "G10 - Sprint 3"
puntos: 5
prioridad: Must
en_taiga: true
ref: 8609
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8609
responsables_tareas: ["Fenoglio Santino", "Franco Maximiliano Amarilla"]
tareas_cerradas: "0/4"
---

# HU-59: Dependencias entre nodos con reglas combinadas

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Múltiples roadmaps por curso y grafo configurable|Múltiples roadmaps por curso y grafo configurable]] · Estado: **New** · Responsable de la historia: **Sin asignar** · Tareas: **0/4** · Sprint: **G10 - Sprint 3**
> Cargada en Taiga: [[taiga/historias/HU-59 Dependencias entre nodos con reglas combinadas|HU-59]] ([abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8609)) · Épica en Taiga: [[epicas/EP-8633 Múltiples roadmaps por curso y grafo configurable|EP-8633]] · Responsables de las tareas: [[sprints/sprint-3/12-responsables#Fenoglio Santino|Fenoglio Santino]] (3), [[sprints/sprint-3/12-responsables#Franco Maximiliano Amarilla|Franco Maximiliano Amarilla]] (1).

[G10] — HU-59 — Dependencias entre nodos con reglas combinadas
--------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: definir de qué nodos depende cada nodo, incluso con reglas combinadas como `A y (B o C)`
*   **Para**: modelar ejercicios que requieren combinaciones de teoría y práctica

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Las reglas se guardan como árbol (`Rule` con AND/OR anidables). Esta HU define la regla una sola vez: HU-58 la reusa para secciones (y agrega el XP mínimo) y HU-65 la asocia a `REQUIRES`. Pasa a Must el 2026-10-15 porque HT-20 (Must) depende de ella. La lectura obligatoria sigue contando como requisito.
*   [ ] Validaciones: No se puede guardar un ciclo; una regla vacía no se guarda.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): ADMIN, GESTOR o PROFESSOR dueño.
*   [ ] Accesibilidad (WCAG/teclado/lectores): El constructor de reglas se puede usar con teclado y lector.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El profesor arma una regla con AND, OR y anidamiento.
*   [ ] **CA2**: Se guarda como árbol en Neo4j.
*   [ ] **CA3**: Guardar un ciclo devuelve error.
*   [ ] **CA4**: El alumno ve qué le falta para desbloquear el nodo.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Reglas combinadas entre nodos

**Escenario 1**  

*   **Dado**: el nodo 3 requiere `1 y (2 o 4)`
*   **Cuando**: el alumno completa 1 y 4
*   **Entonces**: el nodo 3 se desbloquea

**Escenario 2**  

*   **Dado**: la misma regla
*   **Cuando**: el alumno completa solo 1
*   **Entonces**: ve «te falta: 2 o 4»

**Escenario 3**  

*   **Dado**: una regla que genera ciclo
*   **Cuando**: el profesor la guarda
*   **Entonces**: recibe error de ciclo

* * *

Prototipo
---------

*   **Capturas**: Constructor de reglas del nodo.
*   **URL Figma**: Pendiente.
*   **Storybook**: Pendiente.
*   **Mock API / Swagger**: PATCH /api/roadmap/nodes/{nodeId}/rules con árbol de reglas.

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

*   Servicios involucrados: Ninguno.
*   Módulos afectados: Reglas de nodo, `GateEvaluator`, `rules-wizard`.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: `Rule` en Neo4j.
*   Riesgos y mitigación (opcional): Complejidad de la UI; mitigación: empezar con un nivel de anidamiento (P7).

## Tareas

> [!info] Espejo de Taiga (sync 2026-10-15). Cerradas: **0/4**. Historia en Taiga: [[taiga/historias/HU-59 Dependencias entre nodos con reglas combinadas|HU-59]] · [abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8609)

- [ ] [#9155](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9155) **T-59.1 Guardar reglas combinadas como árbol** · Back · New · [[sprints/sprint-3/12-responsables#Fenoglio Santino|Fenoglio Santino]]
    - **Qué:** las reglas de nodo pasan a ser un árbol con AND/OR anidados (`A y (B o C)`). La lectura obligatoria sigue contando como requisito. Se rechazan ciclos y reglas vacías.
    - **Dónde:** módulo `graph`, `GraphValidator`.
    - **Listo cuando:** se guarda y se lee una regla anidada y hay tests de ciclos y reglas vacías.
- [ ] [#9156](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9156) **T-59.2 Armar reglas combinadas en el editor** · Front · New · [[sprints/sprint-3/12-responsables#Fenoglio Santino|Fenoglio Santino]]
    - **Qué:** extender `rules-wizard` para armar grupos AND/OR, empezando con un nivel de anidamiento. Usable con teclado y lector de pantalla.
    - **Listo cuando:** el profesor arma `A y (B o C)` sin escribir nada a mano.
- [ ] [#9157](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9157) **T-59.3 Mostrarle al alumno qué le falta** · Front · New · [[sprints/sprint-3/12-responsables#Fenoglio Santino|Fenoglio Santino]]
    - **Qué:** describir la regla en palabras («Requiere A y (B o C)») marcando lo que ya cumplió.
    - **Listo cuando:** el alumno entiende qué le falta para desbloquear el nodo.
- [ ] [#9349](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9349) **T-59.4 Wiki, OpenAPI y diagrama de secuencia** · New · [[sprints/sprint-3/12-responsables#Franco Maximiliano Amarilla|Franco Maximiliano Amarilla]]
    - Tarea de documentación agregada en Taiga por el equipo; no estaba en la propuesta.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Existen dependencias AND/OR entre nodos (V5/V7) con lectura obligatoria, pero un solo modo por nodo.

### Depende de

- [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps|HT-17]] Modelo 1 a N de curso a roadmaps
- [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial|HT-18]] Módulo graph en Neo4j y migración inicial

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|P7]] Sí hacen falta reglas combinadas, además de AND/OR + XP mínimo.
