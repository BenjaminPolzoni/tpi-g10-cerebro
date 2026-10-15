---
tags: [tpi, g10, taiga, ht]
codigo: HT-30
ref: 9269
estado: "New"
responsable: "Sin asignar"
epicas: "[[epicas/EP-8632 Deuda del Sprint 2|EP-8632]]"
sprint: "G10 - Sprint 03"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/9269
---

# HT-30: Insignias pendientes de HU-20 y HU-21

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/9269) · Estado: **New** · Responsable: **Sin asignar** · Sprint: **G10 - Sprint 03**
> Épica: [[epicas/EP-8632 Deuda del Sprint 2|EP-8632]] · Tareas cerradas: **0/6**

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

- [ ] #9282 T-30.1 HU-20 · Editar las insignias del curso desde el front · New · Lorenzo Araujo
- [ ] #9283 T-30.2 HU-20 · Dar de baja una insignia del curso · New · Lautaro Jesus Diego
- [ ] #9284 T-30.3 HU-21 CA1 · Otorgar la insignia «sección sin perder vidas» (SECTION_NO_LIVES_LOST) · New · Lautaro Jesus Diego
- [ ] #9285 T-30.4 HU-21 CA1 · Otorgar la insignia «nodo sin reintentos» (NODE_NO_RETRIES) · New · Lautaro Jesus Diego
- [ ] #9286 T-30.5 HU-21 CA1 · Otorgar la insignia «recuperó una vida» (LIFE_RECOVERED) · New · Lautaro Jesus Diego
- [ ] #9341 T-30.6 Wiki, OpenAPI y diagrama de secuencia · New · Franco Maximiliano Amarilla
