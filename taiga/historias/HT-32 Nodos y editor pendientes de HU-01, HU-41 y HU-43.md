---
tags: [tpi, g10, taiga, ht]
codigo: HT-32
ref: 9271
estado: "New"
responsable: "Sin asignar"
epicas: "[[epicas/EP-8632 Deuda del Sprint 2|EP-8632]]"
sprint: "G10 - Sprint 03"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/9271
---

# HT-32: Nodos y editor pendientes de HU-01, HU-41 y HU-43

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/9271) · Estado: **New** · Responsable: **Sin asignar** · Sprint: **G10 - Sprint 03**
> Épica: [[epicas/EP-8632 Deuda del Sprint 2|EP-8632]] · Tareas cerradas: **0/6**

[G10] — HT-32 — Nodos y editor pendientes de HU-01, HU-41 y HU-43
-----------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: que un nodo quede «desafío no disponible» cuando el Motor da de baja su desafío, que editar un nodo no le borre la política de vidas y que el ícono de desafío solo se acepte donde corresponde
*   **Para**: cumplir lo que les falta a HU-01, HU-41 y HU-43 sin reabrirlas

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Cada tarea lleva el código de la HU original y el CA que cierra; al terminarla se deja un comentario en la HU original de Taiga. La baja de un desafío no toca el progreso del alumno (DEC-005).
*   [ ] Validaciones: Reintentos entre 0 y el tope de PAR-13. Ícono de desafío solo en nodos de desafío o examen.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): Editar nodos: ADMIN, GESTOR o PROFESSOR dueño del curso.
*   [ ] Accesibilidad (WCAG/teclado/lectores): «Desafío no disponible» se muestra en texto.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1** (HU-01 CA8): Al recibir la baja de un desafío del Motor, el nodo queda «desafío no disponible», el profesor lo ve en el editor y el gate responde con un motivo claro, sin tocar el progreso.
*   [ ] **CA2** (HU-41 CA2): El nodo tiene reintentos validados contra PAR-13 y un PUT sin `lives_policy` no lo resetea a STANDARD.
*   [ ] **CA3** (HU-43): El ícono de desafío solo se acepta en nodos de desafío o examen; en `CONTENT` o `UNIT` devuelve 400.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Nodos y editor

**Escenario 1** (HU-01)

*   **Dado**: un nodo con un desafío
*   **Cuando**: el Motor publica la baja de ese desafío, una o dos veces
*   **Entonces**: el nodo queda marcado como «desafío no disponible» una sola vez y el progreso no cambia

**Escenario 2** (HU-41)

*   **Dado**: un nodo con política de vidas distinta de STANDARD
*   **Cuando**: el profesor le cambia solo el nombre
*   **Entonces**: la política de vidas no cambia

**Escenario 3** (HU-43)

*   **Dado**: un nodo `CONTENT`
*   **Cuando**: el profesor le pone un ícono de desafío
*   **Entonces**: recibe 400

* * *

Prototipo
---------

*   **Capturas**: Editor de nodo (reintentos, ícono, desafío no disponible).
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-input`, `generic-select`.
*   **Mock API / Swagger**: PATCH /api/roadmap/nodes/{nodeId} con `reintentos_permitidos`.

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

*   Servicios involucrados: Motor (evento de baja de desafío), Backoffice (PAR-13).
*   Módulos afectados: `RoadmapEventListener`, `GraphService`, `NodeController`, `roadmap-section-nodes`, `entity-editor-dialog`.
*   Otros equipos / aprobaciones: G09 (nombre del evento de baja).
*   Impacto en datos / migraciones: Columna de reintentos en el nodo (HU-41) y estado «desafío no disponible» del nodo (HU-01).
*   Riesgos y mitigación (opcional): Que no esté definido de dónde sale PAR-13; mitigación: usar el tope en caché de Backoffice y anotarlo en `acuerdos/backoffice`.


## Tareas

- [ ] #9293 T-32.1 HU-01 CA8 · Marcar como «desafío no disponible» el nodo cuyo desafío da de baja el Motor · New · Gabriela Camacho
- [ ] #9294 T-32.2 HU-01 CA8 · Que el profesor vea qué nodos quedaron sin desafío · New · Lorenzo Araujo
- [ ] #9295 T-32.3 HU-41 CA2 · Que guardar un nodo no le borre la política de vidas · New · Iker Alonso
- [ ] #9296 T-32.4 HU-41 CA2 · Configurar los reintentos permitidos de cada nodo · New · Lautaro Jesus Diego
- [ ] #9297 T-32.5 HU-43 · Aceptar el ícono de desafío solo en desafíos y exámenes · New · Ludmila Mailen Cejas
- [ ] #9343 T-32.6 Wiki, OpenAPI y diagrama de secuencia · New · Quinteros Tomás
