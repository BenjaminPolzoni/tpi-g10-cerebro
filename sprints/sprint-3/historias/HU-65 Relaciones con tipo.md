---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-65
estado: Propuesta
responsable: ""
epica: "Correcciones de los profes"
sprint: "G10 - Sprint 3"
puntos: 8
prioridad: Must
en_taiga: false
---

# HU-65: Relaciones con tipo

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Correcciones de los profes|Correcciones de los profes]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga.

[G10] — HU-65 — Relaciones con tipo
-----------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: relacionar nodos y unidades con tipos de relación, ver el nombre de cada relación y elegir cuáles se muestran
*   **Para**: que el mapa muestre cómo se conectan los temas, no solo qué bloquea a qué

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Catálogo de tipos: `REQUIRES`, `BELONGS_TO`, `RELATED_TO` y un cuarto a definir (P4). Solo `REQUIRES` afecta el desbloqueo. Cada tipo tiene nombre visible y visibilidad configurable.
*   [ ] Validaciones: No aplica.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): ADMIN, GESTOR o PROFESSOR dueño.
*   [ ] Accesibilidad (WCAG/teclado/lectores): La relación se distingue por texto y forma de línea, no solo por color.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Catálogo de tipos de relación con nombre y visibilidad.
*   [ ] **CA2**: La arista muestra el nombre del tipo.
*   [ ] **CA3**: El profesor oculta un tipo y deja de verse en el mapa.
*   [ ] **CA4**: Solo `REQUIRES` cambia el desbloqueo.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Relaciones con tipo

**Escenario 1**  

*   **Dado**: dos nodos
*   **Cuando**: el profesor los une con `RELATED_TO`
*   **Entonces**: la arista dice «Relacionado con» y no bloquea nada

**Escenario 2**  

*   **Dado**: el tipo `BELONGS_TO` oculto
*   **Cuando**: el alumno abre el mapa
*   **Entonces**: no ve esas aristas

**Escenario 3**  

*   **Dado**: una relación `REQUIRES`
*   **Cuando**: el alumno no completó el origen
*   **Entonces**: el destino sigue bloqueado

* * *

Prototipo
---------

*   **Capturas**: Aristas con etiqueta en el grafo.
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-node-graph`.
*   **Mock API / Swagger**: Tipos de relación en `/roadmaps/{id}/graph`.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 8
*   **Prioridad (MoSCoW / Numérica)**: Must

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 8 | Must |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Ninguno.
*   Módulos afectados: Módulo graph, vista de grafo, mapa del alumno.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: Relaciones con tipo en Neo4j.
*   Riesgos y mitigación (opcional): Depende de P4.

## Tareas

- [ ] T-65.1 Catálogo de tipos en el módulo graph
- [ ] T-65.2 Etiqueta y visibilidad en el front
- [ ] T-65.3 Tests

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Solo existe la relación "prerrequisito" con modo AND/OR.

### Depende de

- [[sprints/sprint-3/historias/HT-18 Módulo graph en Neo4j y migración inicial|HT-18]] Módulo graph en Neo4j y migración inicial

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P4]]
