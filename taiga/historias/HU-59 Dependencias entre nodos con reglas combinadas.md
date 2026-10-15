---
tags: [tpi, g10, taiga, hu]
codigo: HU-59
ref: 8609
estado: "New"
responsable: "Sin asignar"
epicas: "[[epicas/EP-8633 Múltiples roadmaps por curso y grafo configurable|EP-8633]]"
sprint: "G10 - Sprint 03"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8609
---

# HU-59: Dependencias entre nodos con reglas combinadas

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8609) · Estado: **New** · Responsable: **Sin asignar** · Sprint: **G10 - Sprint 03**
> Épica: [[epicas/EP-8633 Múltiples roadmaps por curso y grafo configurable|EP-8633]] · Tareas cerradas: **0/4**

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

- [ ] #9155 T-59.1 Guardar reglas combinadas como árbol · New · Fenoglio Santino
- [ ] #9156 T-59.2 Armar reglas combinadas en el editor · New · Fenoglio Santino
- [ ] #9157 T-59.3 Mostrarle al alumno qué le falta · New · Fenoglio Santino
- [ ] #9349 T-59.4 Wiki, OpenAPI y diagrama de secuencia · New · Franco Maximiliano Amarilla
