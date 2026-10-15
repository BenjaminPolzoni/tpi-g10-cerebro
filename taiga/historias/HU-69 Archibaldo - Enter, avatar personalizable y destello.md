---
tags: [tpi, g10, taiga, hu]
codigo: HU-69
ref: 8618
estado: "New"
responsable: "Sin asignar"
epicas: "[[epicas/EP-8631 Correcciones de los profes|EP-8631]]"
sprint: "G10 - Sprint 03"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8618
---

# HU-69: Archibaldo: Enter, avatar personalizable y destello

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8618) · Estado: **New** · Responsable: **Sin asignar** · Sprint: **G10 - Sprint 03**
> Épica: [[epicas/EP-8631 Correcciones de los profes|EP-8631]] · Tareas cerradas: **0/4**

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

- [ ] #9219 T-69.1 Hablar con Archibaldo con Enter · New · Ludmila Mailen Cejas
- [ ] #9220 T-69.2 Avatar y nombre de Archibaldo configurables por curso · New · Ludmila Mailen Cejas
- [ ] #9221 T-69.3 Destello que marca el camino al próximo nodo · New · Ludmila Mailen Cejas
- [ ] #9357 T-69.4 Wiki, OpenAPI y diagrama de secuencia · New · Quinteros Tomás
