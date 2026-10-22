---
tags: [tpi, g10, sprint-3, ht]
codigo: HT-16
estado: New
responsable: "Sin asignar"
epica: "Múltiples roadmaps por curso y grafo configurable"
sprint: "G10 - Sprint 3"
puntos: 3
prioridad: Must
en_taiga: true
ref: 8599
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8599
responsables_tareas: ["Iker Alonso"]
tareas_cerradas: "0/4"
---

# HT-16: Validar la infra de Neo4j y modelar las relaciones

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Múltiples roadmaps por curso y grafo configurable|Múltiples roadmaps por curso y grafo configurable]] · Estado: **New** · Responsable de la historia: **Sin asignar** · Tareas: **0/4** · Sprint: **G10 - Sprint 3**
> Cargada en Taiga: [[taiga/historias/HT-16 Validar la infra de Neo4j y modelar las relaciones|HT-16]] ([abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8599)) · Épica en Taiga: [[epicas/EP-8633 Múltiples roadmaps por curso y grafo configurable|EP-8633]] · Responsables de las tareas: [[sprints/sprint-3/12-responsables#Iker Alonso|Iker Alonso]] (4).

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

> [!info] Espejo de Taiga (sync 2026-10-15). Cerradas: **0/4**. Historia en Taiga: [[taiga/historias/HT-16 Validar la infra de Neo4j y modelar las relaciones|HT-16]] · [abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8599)

- [x] [#8826](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/8826) **T-16.1 Levantar Neo4j en el compose local** · Infra · Hecha (#222, mergeada el 16/10; falta cerrar en Taiga) · [[sprints/sprint-3/12-responsables#Iker Alonso|Iker Alonso]]
    - **Qué:** sumar el servicio `neo4j` (Community, imagen oficial) al compose local del back, con volumen persistente, usuario y clave por variables de entorno y healthcheck.
    - **Dónde:** compose de desarrollo de `tpi-roadmap`.
    - **Listo cuando:** `docker compose up` lo levanta, el navegador de Neo4j responde en localhost y los datos sobreviven a un reinicio.
- [ ] [#8828](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/8828) **T-16.2 Sumar Neo4j a la plataforma y a la demo** · Infra · New · [[sprints/sprint-3/12-responsables#Iker Alonso|Iker Alonso]]
    - **Qué:** agregar Neo4j a `tpi-system-compose` y a los entornos (mesh y demo) de forma que solo lo alcance roadmap-service. Lo hacemos nosotros y solo lo usa nuestro micro (G1). Avisar a quien mantiene la plataforma.
    - **Listo cuando:** roadmap-service se conecta a Neo4j en el entorno integrado, ningún otro servicio lo ve, y queda anotado en `acuerdos/plataforma-gateway-kafka`.
- [x] [#8834](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/8834) **T-16.3 Probar Spring Data Neo4j con un test en el CI** · Back · Hecha (#237, mergeada el 16/10; falta cerrar en Taiga) · [[sprints/sprint-3/12-responsables#Iker Alonso|Iker Alonso]]
    - **Qué:** sumar `spring-boot-starter-data-neo4j`, mapear un ejemplo mínimo (una sección con dos nodos unidos por `REQUIRES`) y escribir un test de integración con Testcontainers que lo guarde y lo lea.
    - **Listo cuando:** el test corre en verde en el CI sin Neo4j instalado en la máquina.
- [x] [#8844](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/8844) **T-16.4 Escribir el modelo del grafo** · Docs · Hecha (#220, mergeada el 15/10; falta cerrar en Taiga) · [[sprints/sprint-3/12-responsables#Iker Alonso|Iker Alonso]]
    - **Qué:** documentar en `04-base-de-grafos` las etiquetas (roadmap, sección, nodo con los tipos fijos de DEC-018), las 5 relaciones con sus propiedades (`label`, `visible`, modo AND/OR y XP mínimo en `requires`), dónde van `START`/`END` y qué se queda en Postgres.
    - **Listo cuando:** el equipo lo revisó y HT-18 puede arrancar sin dudas de modelo.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Neo4j está decidido (DEC-016) pero no existe en el compose ni en la mesh.

### Depende de

Nada: se puede empezar ya.

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|G1]] Neo4j lo sumamos nosotros al compose y a los entornos; solo lo usa nuestro micro y guarda solo los grafos.
- ✅ [[sprints/sprint-3/08-dudas|P1]] Cada roadmap es un mapa distinto del mismo curso.
- ✅ [[sprints/sprint-3/08-dudas|P4]] 5 tipos: `requires`, `recommends`, `belongs_to`, `related_to` y `part_of` (DEC-018).
