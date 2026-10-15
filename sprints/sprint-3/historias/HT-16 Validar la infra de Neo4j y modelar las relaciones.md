---
tags: [tpi, g10, sprint-3, ht]
codigo: HT-16
estado: Propuesta
responsable: ""
epica: "Múltiples roadmaps por curso y grafo configurable"
sprint: "G10 - Sprint 3"
puntos: 3
prioridad: Must
en_taiga: false
---

# HT-16: Validar la infra de Neo4j y modelar las relaciones

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Múltiples roadmaps por curso y grafo configurable|Múltiples roadmaps por curso y grafo configurable]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga.

[G10] — HT-16 — Validar la infra de Neo4j y modelar las relaciones
------------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: validar que Neo4j corre en la plataforma y dejar escrito el modelo de nodos y relaciones
*   **Para**: arrancar la migración sin sorpresas de infra ni de modelo

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Neo4j está decidido por los profes (DEC-016). El spike no elige base: valida infra y modelo. Neo4j Community (GPLv3) en Docker. Neo4j es solo para roadmap-service y guarda solo los grafos (curso, sección, unidad, etc.); no se migra toda la base (G1).
*   [ ] Validaciones: La prueba de concepto corre en el CI con Testcontainers.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): No aplica.
*   [ ] Otros: El modelo incluye N roadmaps por curso (DEC-017), START/END por roadmap y por unidad/sección (HU-64), los 5 tipos de relación (HU-65) y los tipos de nodo fijos (DEC-018).

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Neo4j levantado en el compose local con volumen persistente.
*   [ ] **CA2**: Acordado con plataforma quién lo suma a la mesh y a la demo (G1), registrado en `acuerdos/`.
*   [ ] **CA3**: Prueba de concepto con Spring Data Neo4j y Testcontainers en el CI.
*   [ ] **CA4**: Modelo de nodos y relaciones escrito en `04-base-de-grafos`.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Spike de Neo4j

**Escenario 1**  

*   **Dado**: un clon limpio del back
*   **Cuando**: se corre `docker compose up`
*   **Entonces**: Neo4j levanta junto con Postgres

**Escenario 2**  

*   **Dado**: la prueba de concepto
*   **Cuando**: corre el CI
*   **Entonces**: el test con Testcontainers de Neo4j pasa

**Escenario 3**  

*   **Dado**: el modelo escrito
*   **Cuando**: el equipo lo revisa
*   **Entonces**: cubre roadmaps, secciones, nodos, reglas, START/END y tipos de relación

* * *

Prototipo
---------

*   **Capturas**: No aplica (sin pantalla).
*   **URL Figma**: No aplica.
*   **Storybook**: No aplica.
*   **Mock API / Swagger**: No aplica.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 3
*   **Prioridad (MoSCoW / Numérica)**: Must

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 3 | Must |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Plataforma (`tpi-system-compose`, mesh).
*   Módulos afectados: Infra del back, CI.
*   Otros equipos / aprobaciones: Quien mantiene la plataforma (G1).
*   Impacto en datos / migraciones: Sin migración (solo prueba).
*   Riesgos y mitigación (opcional): Que la plataforma no tenga recursos para Neo4j; mitigación: acordarlo la primera semana.

## Tareas

- [ ] T-16.1 Neo4j en el compose local
- [ ] T-16.2 Acordar Neo4j con plataforma (G1)
- [ ] T-16.3 Prueba de concepto con Spring Data Neo4j + Testcontainers
- [ ] T-16.4 Modelo escrito en 04

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Neo4j está decidido (DEC-016) pero no existe en el compose ni en la mesh.

### Depende de

Nada: se puede empezar ya.

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|G1]] Neo4j es solo para nuestro micro y guarda solo los grafos. Sigue por coordinar quién lo suma al compose (T-16.2).
- ✅ [[sprints/sprint-3/08-dudas|P1]] Cada roadmap es un mapa distinto del mismo curso.
- ✅ [[sprints/sprint-3/08-dudas|P4]] 5 tipos: `requires`, `recommends`, `belongs_to`, `related_to` y `part_of` (DEC-018).
