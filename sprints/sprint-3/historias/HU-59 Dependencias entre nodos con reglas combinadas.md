---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-59
estado: Propuesta
responsable: ""
epica: "Múltiples roadmaps por curso y grafo configurable"
sprint: "G10 - Sprint 3"
puntos: 5
prioridad: Should
en_taiga: false
---

# HU-59: Dependencias entre nodos con reglas combinadas

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Múltiples roadmaps por curso y grafo configurable|Múltiples roadmaps por curso y grafo configurable]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga.

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

*   [ ] Reglas de negocio: Las reglas se guardan como árbol (`Rule` con AND/OR anidables). La lectura obligatoria sigue contando como requisito.
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
*   **Prioridad (MoSCoW / Numérica)**: Should

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 5 | Should |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Ninguno.
*   Módulos afectados: Reglas de nodo, `GateEvaluator`, `rules-wizard`.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: `Rule` en Neo4j.
*   Riesgos y mitigación (opcional): Complejidad de la UI; mitigación: empezar con un nivel de anidamiento (P7).

## Tareas

- [ ] **T-59.1 Guardar reglas combinadas como árbol** · Back
    - **Qué:** las reglas de nodo pasan a ser un árbol con AND/OR anidados (`A y (B o C)`). La lectura obligatoria sigue contando como requisito. Se rechazan ciclos y reglas vacías.
    - **Dónde:** módulo `graph`, `GraphValidator`.
    - **Listo cuando:** se guarda y se lee una regla anidada y hay tests de ciclos y reglas vacías.
- [ ] **T-59.2 Armar reglas combinadas en el editor** · Front
    - **Qué:** extender `rules-wizard` para armar grupos AND/OR, empezando con un nivel de anidamiento. Usable con teclado y lector de pantalla.
    - **Listo cuando:** el profesor arma `A y (B o C)` sin escribir nada a mano.
- [ ] **T-59.3 Mostrarle al alumno qué le falta** · Front
    - **Qué:** describir la regla en palabras («Requiere A y (B o C)») marcando lo que ya cumplió.
    - **Listo cuando:** el alumno entiende qué le falta para desbloquear el nodo.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Existen dependencias AND/OR entre nodos (V5/V7) con lectura obligatoria, pero un solo modo por nodo.

### Depende de

- [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps|HT-17]] Modelo 1 a N de curso a roadmaps
- [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial|HT-18]] Módulo graph en Neo4j y migración inicial

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|P7]] Sí hacen falta reglas combinadas, además de AND/OR + XP mínimo.
