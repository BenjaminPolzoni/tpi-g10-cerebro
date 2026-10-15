---
tags: [tpi, g10, taiga, ht]
codigo: HT-16
ref: 8599
estado: "New"
responsable: "Sin asignar"
epicas: "[[epicas/EP-8633 Múltiples roadmaps por curso y grafo configurable|EP-8633]]"
sprint: "G10 - Sprint 03"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8599
---

# HT-16: Validar la infra de Neo4j y modelar las relaciones

> [!info] Generado desde Taiga (2026-10-15 16:54). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8599) · Estado: **New** · Responsable: **Sin asignar** · Sprint: **G10 - Sprint 03**
> Épica: [[epicas/EP-8633 Múltiples roadmaps por curso y grafo configurable|EP-8633]] · Tareas cerradas: **0/4**

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

*   [ ] Reglas de negocio: Neo4j está decidido por los profes (DEC-016). El spike no elige base: valida infra y modelo. Neo4j Community (GPLv3) en Docker. Neo4j es solo para roadmap-service y guarda solo los grafos (curso, sección, unidad, etc.); no se migra toda la base. Lo sumamos nosotros a la plataforma (G1).
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
*   [ ] **CA2**: Neo4j sumado por G10 a la plataforma y a la demo, accesible solo para roadmap-service (G1), registrado en `acuerdos/`.
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

*   **Dado**: la prueba de concepto con el modelo de `04-base-de-grafos`
*   **Cuando**: se guarda una sección con dos nodos unidos por `REQUIRES` y se vuelve a leer
*   **Entonces**: se recuperan los nodos, la relación y su tipo con los mismos `id`

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
*   Otros equipos / aprobaciones: Avisar a quien mantiene la plataforma; Neo4j lo sumamos nosotros (G1).
*   Impacto en datos / migraciones: Sin migración (solo prueba).
*   Riesgos y mitigación (opcional): Que la plataforma no tenga recursos para Neo4j; mitigación: acordarlo la primera semana.


## Tareas

- [ ] #8826 T-16.1 Levantar Neo4j en el compose local · New · Iker Alonso
- [ ] #8828 T-16.2 Sumar Neo4j a la plataforma y a la demo · New · Iker Alonso
- [ ] #8834 T-16.3 Probar Spring Data Neo4j con un test en el CI · New · Iker Alonso
- [ ] #8844 T-16.4 Escribir el modelo del grafo · New · Iker Alonso
