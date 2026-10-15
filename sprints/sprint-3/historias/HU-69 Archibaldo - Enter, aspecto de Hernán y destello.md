---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-69
estado: Propuesta
responsable: ""
epica: "Correcciones de los profes"
sprint: "G10 - Sprint 3"
puntos: 5
prioridad: Could
en_taiga: false
---

# HU-69: Archibaldo: Enter, avatar personalizable y destello

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Correcciones de los profes|Correcciones de los profes]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga.

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
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): El diálogo toma el foco y se cierra con Escape (`generic-modal`).
*   [ ] Otros: Archibaldo es un avatar que personalizan el profesor y el gestor del curso, que también le pueden cambiar el nombre (P11). Ya no se copia a Hernán.

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
*   Módulos afectados: `world-3d.service`, `archipelago-3d.service`, `npc-dialogue`.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Ninguno abierto (P11 respondida).

## Tareas

- [ ] T-69.1 Interacción con Enter y foco
- [ ] T-69.2 Avatar y nombre de Archibaldo editables por profesor y gestor
- [ ] T-69.3 Destello del camino

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

El NPC usa la skin del capitán pirata del kit (`world-3d.service.ts:3109`). El diálogo se abre con clic. No hay destello.

### Depende de

Nada: se puede empezar ya.

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|P11]] Archibaldo es un avatar personalizable por el profesor y el gestor, con nombre editable.
