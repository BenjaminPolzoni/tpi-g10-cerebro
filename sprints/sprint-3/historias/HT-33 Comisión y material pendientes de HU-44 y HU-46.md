---
tags: [tpi, g10, sprint-3, ht]
codigo: HT-33
estado: New
responsable: "Sin asignar"
epica: "Deuda del Sprint 2"
sprint: "G10 - Sprint 3"
puntos: 8
prioridad: Must
prioridad_sprint: 1
en_taiga: true
ref: 9272
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/9272
responsables_tareas: ["Lorenzo Araujo", "Lautaro Jesus Diego", "Ludmila Mailen Cejas", "Quinteros Tomás"]
tareas_cerradas: "0/6"
---

# HT-33: Comisión y material pendientes de HU-44 y HU-46

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Deuda del Sprint 2|Deuda del Sprint 2]] · Estado: **New** · Responsable de la historia: **Sin asignar** · Tareas: **0/6** · Sprint: **G10 - Sprint 3**
> Cargada en Taiga: [[taiga/historias/HT-33 Comisión y material pendientes de HU-44 y HU-46|HT-33]] ([abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/9272)) · Épica en Taiga: [[epicas/EP-8632 Deuda del Sprint 2|EP-8632]] · Responsables de las tareas: [[sprints/sprint-3/12-responsables#Lorenzo Araujo|Lorenzo Araujo]] (2), [[sprints/sprint-3/12-responsables#Quinteros Tomás|Quinteros Tomás]] (2), [[sprints/sprint-3/12-responsables#Lautaro Jesus Diego|Lautaro Jesus Diego]] (1), [[sprints/sprint-3/12-responsables#Ludmila Mailen Cejas|Ludmila Mailen Cejas]] (1). Sale de dividir por tema la HT de criterios pendientes (2026-10-15): ver [[sprints/sprint-3/historias/HT-30 Insignias pendientes de HU-20 y HU-21|HT-30]]. Las HU originales quedan en Done en su sprint; cada tarea dice a qué HU y a qué CA corresponde.

> [!important] Prioridad 1 del sprint (2026-10-15)
> Va después de las insignias (HT-30). Son criterios que ya se dieron por terminados y no se cumplen.

[G10] — HT-33 — Comisión y material pendientes de HU-44 y HU-46
---------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: que el alumno elija la comisión dentro del roadmap y vea el motivo del bloqueo por comisión, y que el material se abra dentro de la página
*   **Para**: cumplir lo que les falta a HU-44 y HU-46 sin reabrirlas

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Cada tarea lleva el código de la HU original y el CA que cierra; al terminarla se deja un comentario en la HU original de Taiga. Esta HT es la dueña del filtro por comisión dentro de un roadmap; asignar roadmaps a grupos es HU-61. HU-46 ya no lleva el Templo (P13).
*   [ ] Validaciones: Cada CA cerrado tiene su test.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): El alumno solo elige entre sus propias comisiones.
*   [ ] Accesibilidad (WCAG/teclado/lectores): El motivo `group_restricted` se muestra en texto; el visor se cierra con Escape.
*   [ ] Otros: Requiere `ROADMAP_BY_GROUP_ENABLED` encendido en la demo.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1** (HU-44 CA1 a CA4): El alumno con más de una comisión elige la comisión en el roadmap, ve lo habilitado para ella y el motivo `group_restricted` en texto, con `ROADMAP_BY_GROUP_ENABLED` encendido en la demo.
*   [ ] **CA2** (HU-46 CA3): El material desbloqueado se abre en un visor embebido, y el CA de HU-46 queda redefinido en Taiga sin el Templo.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Comisión y material

**Escenario 1** (HU-44)

*   **Dado**: un alumno inscripto en 2W1 y 2W2
*   **Cuando**: elige 2W2 en el roadmap
*   **Entonces**: ve las unidades de 2W2 con el mismo XP

**Escenario 2** (HU-44)

*   **Dado**: un nodo habilitado solo para otra comisión
*   **Cuando**: el alumno intenta entrar
*   **Entonces**: ve en texto que el nodo es de otra comisión (`group_restricted`)

**Escenario 3** (HU-46)

*   **Dado**: un material desbloqueado
*   **Cuando**: el alumno lo abre
*   **Entonces**: lo ve en un visor dentro del roadmap, con la opción de abrirlo en otra pestaña

* * *

Prototipo
---------

*   **Capturas**: Selector de comisión; visor de material.
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-select`, `generic-modal`.
*   **Mock API / Swagger**: No aplica (usa endpoints existentes).

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

*   Servicios involucrados: Courses (comisiones y URLs del material).
*   Módulos afectados: Roadmap del alumno, `GroupSelectionService`, `material-access`.
*   Otros equipos / aprobaciones: G01 (URLs del material).
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Que el flag no esté encendido en la demo; mitigación: T-33.3 lo enciende y prueba.

## Tareas

> [!info] Espejo de Taiga (sync 2026-10-15). Cerradas: **0/6**. Historia en Taiga: [[taiga/historias/HT-33 Comisión y material pendientes de HU-44 y HU-46|HT-33]] · [abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/9272)

- [ ] [#9298](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9298) **T-33.1 HU-44 CA2 · Elegir la comisión en el roadmap del alumno** · Front · New · [[sprints/sprint-3/12-responsables#Lorenzo Araujo|Lorenzo Araujo]]
    - **Qué:** si el alumno está en más de una comisión, un `generic-select` para elegir cuál ver; usa la selección de comisión que ya existe en el back (`GroupSelectionService`).
    - **Listo cuando:** un alumno de 2W1 y 2W2 elige 2W2 y ve sus unidades con el mismo XP. Hay test.
- [ ] [#9299](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9299) **T-33.2 HU-44 CA3 · Explicar con texto el bloqueo por comisión (group_restricted)** · Front · New · [[sprints/sprint-3/12-responsables#Lorenzo Araujo|Lorenzo Araujo]]
    - **Qué:** sumar el texto del motivo `group_restricted` en `roadmapLabels.blockReason`.
    - **Listo cuando:** el alumno ve por qué no puede entrar a un nodo de otra comisión.
- [ ] [#9300](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9300) **T-33.3 HU-44 CA1, CA3 y CA4 · Encender el filtro por comisión en la demo y probarlo** · Infra · New · [[sprints/sprint-3/12-responsables#Lautaro Jesus Diego|Lautaro Jesus Diego]]
    - **Qué:** activar `ROADMAP_BY_GROUP_ENABLED` (`app.features.roadmap-by-group.enabled`) en el entorno de demo y probar los cuatro CA con un alumno en 2W1 y 2W2.
    - **Listo cuando:** los cuatro CA andan de punta a punta en la demo.
**HU-46 CA3: visor embebido** ([us/5375](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/5375))
- [ ] [#9301](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9301) **T-33.4 HU-46 CA3 · Abrir el material dentro de la página** · Front · New · [[sprints/sprint-3/12-responsables#Ludmila Mailen Cejas|Ludmila Mailen Cejas]]
    - **Qué:** hoy `material-access` abre la URL firmada en una pestaña nueva. Mostrar PDF y video en un visor dentro de la página (por ejemplo en un `generic-modal`), con la opción de abrir en pestaña nueva como respaldo.
    - **Listo cuando:** el alumno lee el material sin salir del roadmap. Hay test.
- [ ] [#9302](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9302) **T-33.5 HU-46 CA1 · Redefinir el CA de HU-46 en Taiga sin el Templo** · Equipo · New · [[sprints/sprint-3/12-responsables#Quinteros Tomás|Quinteros Tomás]]
    - **Qué:** editar HU-46 (us/5375) en Taiga para sacar el CA1 del Templo, que no existe más (P13).
    - **Listo cuando:** la HU en Taiga ya no menciona el Templo.
- [ ] [#9344](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9344) **T-33.6 Wiki, OpenAPI y diagrama de secuencia** · New · [[sprints/sprint-3/12-responsables#Quinteros Tomás|Quinteros Tomás]]
    - Tarea de documentación agregada en Taiga por el equipo; no estaba en la propuesta.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Verificado contra `origin/develop` (back `fc1917e`, front `67cbad4a`) el 2026-10-15.

| HU original | Sprint | CA que falta | Estado hoy |
|---|---|---|---|
| [[taiga/historias/HU-44 Ver el roadmap de cada una de mis comisiones\|HU-44]] | 2 | ❌ CA2 y ⚠️ CA1, CA3, CA4 | No hay selector en el front; lo demás depende de `ROADMAP_BY_GROUP_ENABLED`, que está en false |
| [[taiga/historias/HU-46 Ver en los nodos y en el Templo el material teórico de Courses\|HU-46]] | 2 | ❌ CA1 (Templo, descartado por P13) y ❌ CA3: visor embebido | El material se abre en una pestaña nueva |

### Depende de

Nada: se puede empezar ya.

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|P5]] El profesor configura si un roadmap va por comisión (HU-44).
- ✅ [[sprints/sprint-3/08-dudas|P13]] El Templo no existe más (HU-46).
