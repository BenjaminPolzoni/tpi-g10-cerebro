---
tags: [tpi, g10, sprint-3, ht]
codigo: HT-30
estado: New
responsable: "Sin asignar"
epica: "Deuda del Sprint 2"
sprint: "G10 - Sprint 3"
puntos: 8
prioridad: Must
prioridad_sprint: 1
en_taiga: true
ref: 9269
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/9269
responsables_tareas: ["Lorenzo Araujo", "Lautaro Jesus Diego", "Franco Maximiliano Amarilla"]
tareas_cerradas: "0/6"
---

# HT-30: Insignias pendientes de HU-20 y HU-21

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Deuda del Sprint 2|Deuda del Sprint 2]] · Estado: **New** · Responsable de la historia: **Sin asignar** · Tareas: **0/6** · Sprint: **G10 - Sprint 3**
> Cargada en Taiga: [[taiga/historias/HT-30 Insignias pendientes de HU-20 y HU-21|HT-30]] ([abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/9269)) · Épica en Taiga: [[epicas/EP-8632 Deuda del Sprint 2|EP-8632]] · Responsables de las tareas: [[sprints/sprint-3/12-responsables#Lautaro Jesus Diego|Lautaro Jesus Diego]] (4), [[sprints/sprint-3/12-responsables#Lorenzo Araujo|Lorenzo Araujo]] (1), [[sprints/sprint-3/12-responsables#Franco Maximiliano Amarilla|Franco Maximiliano Amarilla]] (1). El 2026-10-15 la HT de criterios pendientes (34 pts) se dividió en cuatro por tema: **HT-30 insignias**, [[sprints/sprint-3/historias/HT-31 Gate y vidas pendientes de HU-15, HU-16 y HU-48|HT-31 gate y vidas]], [[sprints/sprint-3/historias/HT-32 Nodos y editor pendientes de HU-01, HU-41 y HU-43|HT-32 nodos y editor]] y [[sprints/sprint-3/historias/HT-33 Comisión y material pendientes de HU-44 y HU-46|HT-33 comisión y material]]. Las HU originales quedan en Done en su sprint; cada tarea dice a qué HU y a qué CA corresponde.

> [!important] Prioridad 1 del sprint (2026-10-15)
> Va primero de las cuatro, junto con la otra prioridad 1: HT-26 (UI-KIT). Son criterios que ya se dieron por terminados y no se cumplen.

[G10] — HT-30 — Insignias pendientes de HU-20 y HU-21
-----------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: cumplir lo que les falta a HU-20 (editar y dar de baja insignias) y a HU-21 (los tres criterios que nunca se otorgan)
*   **Para**: que las insignias hagan lo que se dio por terminado, sin reabrir esas HU

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Cada tarea lleva el código de la HU original y el CA que cierra; al terminarla se deja un comentario en la HU original de Taiga. Insignias del sistema y del curso (DEC-006); baja lógica sin borrar lo otorgado (DEC-005). Cada insignia se otorga una sola vez por alumno.
*   [ ] Validaciones: Cada CA cerrado tiene su test.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): Editar y dar de baja insignias: ADMIN, GESTOR o PROFESSOR dueño del curso. Las insignias del sistema no se editan.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Las acciones de editar y dar de baja se usan con teclado.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1** (HU-20): El profesor edita y da de baja insignias de su curso desde el front; las ya otorgadas se conservan y las del sistema no muestran esas acciones.
*   [ ] **CA2** (HU-21 CA1): `SECTION_NO_LIVES_LOST`, `NODE_NO_RETRIES` y `LIFE_RECOVERED` se otorgan una sola vez y publican `BADGE_AWARDED`.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Insignias pendientes

**Escenario 1** (HU-21)

*   **Dado**: un alumno que completó una sección sin perder vidas
*   **Cuando**: se cierra el último nodo de la sección
*   **Entonces**: recibe `SECTION_NO_LIVES_LOST` una sola vez y se publica `BADGE_AWARDED`

**Escenario 2** (HU-21)

*   **Dado**: un alumno que recuperó una vida
*   **Cuando**: llega dos veces el mismo evento de Accounting
*   **Entonces**: tiene `LIFE_RECOVERED` una sola vez

**Escenario 3** (HU-20)

*   **Dado**: una insignia del curso ya otorgada a un alumno
*   **Cuando**: el profesor la da de baja
*   **Entonces**: no se puede otorgar más y el alumno la sigue viendo en su perfil

* * *

Prototipo
---------

*   **Capturas**: Catálogo de insignias con editar y dar de baja.
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-modal`, `generic-button`.
*   **Mock API / Swagger**: API de `BadgeCatalogController` (edición y baja).

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 8
*   **Prioridad (MoSCoW / Numérica)**: Must · 1 (máxima del sprint)

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 8 | Must · 1 (máxima del sprint) |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Accounting (vidas perdidas, `LIVES_*`), Motor (evento de cierre del nodo).
*   Módulos afectados: Insignias (`BadgeEvaluator`, `BadgeCriteriaChecks`, `BadgeCatalogController`), listeners de eventos, `badges-catalog-page`.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: Sin migración (la baja lógica usa el campo existente, o una columna nueva si no existe).
*   Riesgos y mitigación (opcional): Duplicar insignias por eventos repetidos; mitigación: otorgamiento idempotente y tests con el evento repetido.

## Tareas

> [!info] Espejo de Taiga (sync 2026-10-15). Cerradas: **0/6**. Historia en Taiga: [[taiga/historias/HT-30 Insignias pendientes de HU-20 y HU-21|HT-30]] · [abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/9269)

- [ ] [#9282](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9282) **T-30.1 HU-20 · Editar las insignias del curso desde el front** · Front · New · [[sprints/sprint-3/12-responsables#Lorenzo Araujo|Lorenzo Araujo]]
    - **Qué:** acción «Editar» en las insignias del curso (nombre, descripción e ícono) usando la API de `BadgeCatalogController`. Las insignias del sistema no muestran la acción (DEC-006).
    - **Dónde:** `badges-catalog-page`.
    - **Listo cuando:** el profesor dueño edita una insignia y el cambio se ve al recargar. Hay test.
- [ ] [#9283](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9283) **T-30.2 HU-20 · Dar de baja una insignia del curso** · Back + Front · New · [[sprints/sprint-3/12-responsables#Lautaro Jesus Diego|Lautaro Jesus Diego]]
    - **Qué:** baja lógica de una insignia del curso (DEC-005); si `BadgeCatalogController` no tiene el endpoint, crearlo. Las insignias ya otorgadas se siguen viendo; un profesor que no es dueño recibe 403.
    - **Listo cuando:** la insignia dada de baja no se puede otorgar más, la ya otorgada sigue en el perfil del alumno y hay tests.
⭐ **HU-21 CA1: tres criterios que nunca se otorgan** ([us/4244](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4244))
- [ ] [#9284](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9284) **T-30.3 HU-21 CA1 · Otorgar la insignia «sección sin perder vidas» (SECTION_NO_LIVES_LOST)** · Back · New · [[sprints/sprint-3/12-responsables#Lautaro Jesus Diego|Lautaro Jesus Diego]]
    - **Qué:** al completar una sección, consultar las vidas perdidas del alumno en esa sección (`LostLivesClient` de Accounting) y otorgar la insignia una sola vez.
    - **Dónde:** `BadgeEvaluator`, `BadgeCriteriaChecks`.
    - **Listo cuando:** se otorga una vez, publica `BADGE_AWARDED` por el outbox y hay test.
- [ ] [#9285](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9285) **T-30.4 HU-21 CA1 · Otorgar la insignia «nodo sin reintentos» (NODE_NO_RETRIES)** · Back · New · [[sprints/sprint-3/12-responsables#Lautaro Jesus Diego|Lautaro Jesus Diego]]
    - **Qué:** al cerrar un nodo aprobado en el primer intento (dato del evento de cierre del Motor), otorgar la insignia.
    - **Dónde:** `BadgeEvaluator`, `RoadmapEventListener`.
    - **Listo cuando:** se otorga solo si no hubo reintentos, una sola vez, con test.
- [ ] [#9286](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9286) **T-30.5 HU-21 CA1 · Otorgar la insignia «recuperó una vida» (LIFE_RECOVERED)** · Back · New · [[sprints/sprint-3/12-responsables#Lautaro Jesus Diego|Lautaro Jesus Diego]]
    - **Qué:** consumir `LIVES_EXHAUSTED` / `LIVES_AVAILABLE` de Accounting (E8) y otorgar la insignia cuando el alumno recupera una vida.
    - **Dónde:** `AccountingEventsListener`, `BadgeEvaluator`.
    - **Listo cuando:** el evento repetido no duplica la insignia y hay test.
- [ ] [#9341](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9341) **T-30.6 Wiki, OpenAPI y diagrama de secuencia** · New · [[sprints/sprint-3/12-responsables#Franco Maximiliano Amarilla|Franco Maximiliano Amarilla]]
    - Tarea de documentación agregada en Taiga por el equipo; no estaba en la propuesta.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Verificado contra `origin/develop` (back `fc1917e`, front `67cbad4a`) el 2026-10-15.

| HU original | Sprint | CA que falta | Estado hoy |
|---|---|---|---|
| [[taiga/historias/HU-20 Definir el catálogo de insignias del curso\|HU-20]] | 2 | Sin CA pendiente: falta editar y dar de baja en el front | El front no lo permite |
| [[taiga/historias/HU-21 Otorgar insignias automáticamente\|HU-21]] | 2 | ❌ CA1: cumplir un criterio otorga la insignia | Tres criterios no tienen evaluador |

### Depende de

Nada: se puede empezar ya.

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|E2]] Los tres criterios de insignia se implementan (HU-21).
- ✅ [[sprints/sprint-3/08-dudas|E8]] Hay que consumir `LIVES_EXHAUSTED` / `LIVES_AVAILABLE` (HU-21).
