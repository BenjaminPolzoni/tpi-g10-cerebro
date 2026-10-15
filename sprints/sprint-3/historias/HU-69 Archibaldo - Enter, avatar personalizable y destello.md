---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-69
estado: New
responsable: "Sin asignar"
epica: "Correcciones de los profes"
sprint: "G10 - Sprint 3"
puntos: 5
prioridad: Could
en_taiga: true
ref: 8618
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8618
responsables_tareas: ["Ludmila Mailen Cejas", "Quinteros Tomás"]
tareas_cerradas: "0/4"
---

# HU-69: Archibaldo: Enter, avatar personalizable y destello

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Correcciones de los profes|Correcciones de los profes]] · Estado: **New** · Responsable de la historia: **Sin asignar** · Tareas: **0/4** · Sprint: **G10 - Sprint 3**
> Cargada en Taiga: [[taiga/historias/HU-69 Archibaldo - Enter, avatar personalizable y destello|HU-69]] ([abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8618)) · Épica en Taiga: [[epicas/EP-8631 Correcciones de los profes|EP-8631]] · Responsables de las tareas: [[sprints/sprint-3/12-responsables#Ludmila Mailen Cejas|Ludmila Mailen Cejas]] (3), [[sprints/sprint-3/12-responsables#Quinteros Tomás|Quinteros Tomás]] (1).

[G10] — HU-69 — Archibaldo: Enter, avatar personalizable y destello
---------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: hablar con Archibaldo con Enter y que un destello me guíe por el camino
*   **Para**: moverme por el mundo sin depender del mouse y saber a dónde ir

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Enter abre el diálogo solo con el NPC en rango. El destello marca el camino al próximo nodo disponible.
*   [ ] Validaciones: No aplica.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): El destello no baja los FPS del mundo.
*   [ ] Seguridad (roles, permisos, datos sensibles): Personalizar a Archibaldo: ADMIN, GESTOR o PROFESSOR dueño del curso.
*   [ ] Accesibilidad (WCAG/teclado/lectores): El diálogo toma el foco y se cierra con Escape (`generic-modal`).
*   [ ] Otros: Archibaldo es un avatar que personalizan el profesor y el gestor del curso, que también le pueden cambiar el nombre (P11).

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Enter abre el diálogo con el NPC en rango.
*   [ ] **CA2**: El foco queda en el diálogo y Escape lo cierra.
*   [ ] **CA3**: El profesor y el gestor del curso personalizan el avatar y el nombre de Archibaldo.
*   [ ] **CA4**: Destello sobre el camino al próximo nodo disponible.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Archibaldo y guía

**Escenario 1**  

*   **Dado**: el alumno junto a Archibaldo
*   **Cuando**: presiona Enter
*   **Entonces**: se abre el diálogo con el foco adentro

**Escenario 2**  

*   **Dado**: el alumno lejos de Archibaldo
*   **Cuando**: presiona Enter
*   **Entonces**: no pasa nada

**Escenario 3**  

*   **Dado**: un nodo disponible
*   **Cuando**: el alumno está en el mundo
*   **Entonces**: un destello marca el camino hacia él

* * *

Prototipo
---------

*   **Capturas**: Mundo 3D con Archibaldo.
*   **URL Figma**: No aplica.
*   **Storybook**: `generic-modal`.
*   **Mock API / Swagger**: No aplica.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 5
*   **Prioridad (MoSCoW / Numérica)**: Could

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 5 | Could |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Ninguno.
*   Módulos afectados: `world-3d.service`, `archipelago-3d.service`, `npc-dialogue`, configuración del curso en el back y pantalla del profesor y el gestor.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: Configuración de Archibaldo (avatar y nombre) por curso: columna o tabla nueva en el back (T-69.2).
*   Riesgos y mitigación (opcional): Ninguno abierto (P11 respondida).

## Tareas

> [!info] Espejo de Taiga (sync 2026-10-15). Cerradas: **0/4**. Historia en Taiga: [[taiga/historias/HU-69 Archibaldo - Enter, avatar personalizable y destello|HU-69]] · [abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8618)

- [ ] [#9219](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9219) **T-69.1 Hablar con Archibaldo con Enter** · Front · New · [[sprints/sprint-3/12-responsables#Ludmila Mailen Cejas|Ludmila Mailen Cejas]]
    - **Qué:** Enter abre `npc-dialogue` solo si el personaje está cerca del NPC; el foco queda en el diálogo y Escape lo cierra (con el modal del kit de HT-26).
    - **Dónde:** `world-3d.service`, `npc-dialogue`.
    - **Listo cuando:** se puede hablar con Archibaldo sin mouse.
- [ ] [#9220](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9220) **T-69.2 Avatar y nombre de Archibaldo configurables por curso** · Back + Front · New · [[sprints/sprint-3/12-responsables#Ludmila Mailen Cejas|Ludmila Mailen Cejas]]
    - **Qué:** el profesor y el gestor eligen el avatar (reutilizando el editor de avatares, que ya está hecho) y el nombre; se guarda por curso y el mundo los usa en vez de la skin del capitán pirata (`world-3d.service.ts:3109`).
    - **Listo cuando:** dos cursos muestran Archibaldos distintos.
- [ ] [#9221](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9221) **T-69.3 Destello que marca el camino al próximo nodo** · Front · New · [[sprints/sprint-3/12-responsables#Ludmila Mailen Cejas|Ludmila Mailen Cejas]]
    - **Qué:** efecto en el mundo 3D que guía hasta el próximo nodo disponible, sin bajar los FPS.
    - **Listo cuando:** el alumno sigue el destello y llega al nodo correcto.
- [ ] [#9357](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9357) **T-69.4 Wiki, OpenAPI y diagrama de secuencia** · New · [[sprints/sprint-3/12-responsables#Quinteros Tomás|Quinteros Tomás]]
    - Tarea de documentación agregada en Taiga por el equipo; no estaba en la propuesta.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

El NPC usa la skin del capitán pirata del kit (`world-3d.service.ts:3109`). El diálogo se abre con clic. No hay destello.

### Depende de

Nada: se puede empezar ya.

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|P11]] Archibaldo es un avatar personalizable por el profesor y el gestor, con nombre editable.
