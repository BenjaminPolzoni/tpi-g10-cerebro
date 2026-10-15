---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-58
estado: New
responsable: "Sin asignar"
epica: "Múltiples roadmaps por curso y grafo configurable"
sprint: "G10 - Sprint 3"
puntos: 5
prioridad: Must
en_taiga: true
ref: 8608
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8608
responsables_tareas: ["Fenoglio Santino", "Lorenzo Araujo", "Franco Maximiliano Amarilla"]
tareas_cerradas: "0/5"
---

# HU-58: Dependencias entre secciones

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Múltiples roadmaps por curso y grafo configurable|Múltiples roadmaps por curso y grafo configurable]] · Estado: **New** · Responsable de la historia: **Sin asignar** · Tareas: **0/5** · Sprint: **G10 - Sprint 3**
> Cargada en Taiga: [[taiga/historias/HU-58 Dependencias entre secciones|HU-58]] ([abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8608)) · Épica en Taiga: [[epicas/EP-8633 Múltiples roadmaps por curso y grafo configurable|EP-8633]] · Responsables de las tareas: [[sprints/sprint-3/12-responsables#Fenoglio Santino|Fenoglio Santino]] (3), [[sprints/sprint-3/12-responsables#Lorenzo Araujo|Lorenzo Araujo]] (1), [[sprints/sprint-3/12-responsables#Franco Maximiliano Amarilla|Franco Maximiliano Amarilla]] (1).

[G10] — HU-58 — Dependencias entre secciones
--------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: definir de qué secciones depende cada sección (AND/OR), con un XP mínimo opcional y un atajo para «todas las anteriores»
*   **Para**: armar el recorrido del curso como en el ejemplo de los profes

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Ya existen las dependencias AND/OR entre secciones (V25). La regla AND/OR (árbol `Rule`) se define en HU-59; esta HU la aplica a secciones y es la dueña del XP mínimo. Vuelve el XP mínimo por sección (se borró en V8, DEC-011). «Todas las anteriores» es un atajo de la UI que guarda un AND. Las dependencias también se definen entre subsecciones (P6).
*   [ ] Validaciones: No se puede guardar un ciclo. XP mínimo ≥ 0.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): ADMIN, GESTOR o PROFESSOR dueño.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Selector de secciones usable con teclado.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Elegir las secciones requeridas con la regla AND/OR de HU-59.
*   [ ] **CA2**: XP mínimo opcional por sección.
*   [ ] **CA3**: Atajo «todas las anteriores».
*   [ ] **CA4**: Guardar un ciclo devuelve error.
*   [ ] **CA5**: El alumno ve por qué una sección está bloqueada.
*   [ ] **CA6**: Las dependencias se pueden definir también entre subsecciones.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Dependencias entre secciones

**Escenario 1**  

*   **Dado**: las secciones 1 y 2
*   **Cuando**: el profesor hace que la 3 dependa de ambas con AND
*   **Entonces**: la 3 se desbloquea solo con 1 y 2 completas

**Escenario 2**  

*   **Dado**: la sección 4 depende de la 2 con XP ≥ 500
*   **Cuando**: un alumno completa la 2 con 300 XP
*   **Entonces**: la 4 sigue bloqueada y ve «te faltan 200 XP»

**Escenario 3**  

*   **Dado**: la sección 1 depende de la 3
*   **Cuando**: el profesor hace que la 3 dependa de la 1
*   **Entonces**: recibe error de ciclo

* * *

Prototipo
---------

*   **Capturas**: Editor de reglas de sección.
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-select`, `generic-input`.
*   **Mock API / Swagger**: PATCH /api/roadmap/sections/{sectionId}/rules.

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
*   Módulos afectados: Reglas de sección, `GateEvaluator`, `rules-wizard`.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: XP mínimo en Neo4j (`Rule.minXp`).
*   Riesgos y mitigación (opcional): Depende de HT-18 y P6.

## Tareas

> [!info] Espejo de Taiga (sync 2026-10-15). Cerradas: **0/5**. Historia en Taiga: [[taiga/historias/HU-58 Dependencias entre secciones|HU-58]] · [abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8608)

- [ ] [#9151](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9151) **T-58.1 Volver a tener XP mínimo por sección** · Back · New · [[sprints/sprint-3/12-responsables#Fenoglio Santino|Fenoglio Santino]]
    - **Qué:** XP mínimo opcional en las reglas de sección del módulo `graph`, validado como mayor o igual a 0. Vuelve lo que se quitó en V8 (actualizar DEC-011).
    - **Listo cuando:** se guarda, se lee y el gate lo evalúa (HT-20).
- [ ] [#9152](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9152) **T-58.2 Dependencias entre subsecciones y sin ciclos** · Back · New · [[sprints/sprint-3/12-responsables#Fenoglio Santino|Fenoglio Santino]]
    - **Qué:** las reglas aceptan subsecciones como requisito (P6) y al guardar se rechaza cualquier ciclo.
    - **Dónde:** `GraphValidator`, `SectionPrerequisiteService`.
    - **Listo cuando:** guardar un ciclo devuelve error con un mensaje claro. Hay tests.
- [ ] [#9153](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9153) **T-58.3 Editor de reglas de sección con XP mínimo y «todas las anteriores»** · Front · New · [[sprints/sprint-3/12-responsables#Fenoglio Santino|Fenoglio Santino]]
    - **Qué:** en `rules-wizard` (modo unidad): elegir secciones o subsecciones requeridas, AND/OR, XP mínimo y un atajo que guarda un AND con todas las anteriores. Usable con teclado.
    - **Listo cuando:** el profesor arma el ejemplo de los profes desde la pantalla.
- [ ] [#9154](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9154) **T-58.4 Explicarle al alumno por qué una sección está bloqueada** · Front · New · [[sprints/sprint-3/12-responsables#Lorenzo Araujo|Lorenzo Araujo]]
    - **Qué:** el motivo dice qué secciones faltan o cuánto XP le falta.
    - **Listo cuando:** el motivo aparece en el mapa y en la lista del alumno.
- [ ] [#9348](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9348) **T-58.5 Wiki, OpenAPI y diagrama de secuencia** · New · [[sprints/sprint-3/12-responsables#Franco Maximiliano Amarilla|Franco Maximiliano Amarilla]]
    - Tarea de documentación agregada en Taiga por el equipo; no estaba en la propuesta.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Ya existen las dependencias AND/OR entre secciones (V25). El XP mínimo por sección se borró en V8 (DEC-011).

### Depende de

- [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps|HT-17]] Modelo 1 a N de curso a roadmaps
- [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial|HT-18]] Módulo graph en Neo4j y migración inicial
- [[sprints/sprint-3/historias/HU-59 Dependencias entre nodos con reglas combinadas|HU-59]] Dependencias entre nodos con reglas combinadas (la regla AND/OR)

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|P6]] Dependencias entre subsecciones.
