---
tags: [tpi, g10, taiga, ht]
codigo: HT-33
ref: 9272
estado: "New"
responsable: "Sin asignar"
epicas: "[[epicas/EP-8632 Deuda del Sprint 2|EP-8632]]"
sprint: "G10 - Sprint 03"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/9272
---

# HT-33: Comisión y material pendientes de HU-44 y HU-46

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/9272) · Estado: **New** · Responsable: **Sin asignar** · Sprint: **G10 - Sprint 03**
> Épica: [[epicas/EP-8632 Deuda del Sprint 2|EP-8632]] · Tareas cerradas: **0/6**

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

- [ ] #9298 T-33.1 HU-44 CA2 · Elegir la comisión en el roadmap del alumno · New · Lorenzo Araujo
- [ ] #9299 T-33.2 HU-44 CA3 · Explicar con texto el bloqueo por comisión (group_restricted) · New · Lorenzo Araujo
- [ ] #9300 T-33.3 HU-44 CA1, CA3 y CA4 · Encender el filtro por comisión en la demo y probarlo · New · Lautaro Jesus Diego
- [ ] #9301 T-33.4 HU-46 CA3 · Abrir el material dentro de la página · New · Ludmila Mailen Cejas
- [ ] #9302 T-33.5 HU-46 CA1 · Redefinir el CA de HU-46 en Taiga sin el Templo · New · Quinteros Tomás
- [ ] #9344 T-33.6 Wiki, OpenAPI y diagrama de secuencia · New · Quinteros Tomás
