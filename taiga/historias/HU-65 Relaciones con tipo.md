---
tags: [tpi, g10, taiga, hu]
codigo: HU-65
ref: 8614
estado: "New"
responsable: "Sin asignar"
epicas: "[[epicas/EP-8631 Correcciones de los profes|EP-8631]]"
sprint: "G10 - Sprint 03"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8614
---

# HU-65: Relaciones con tipo

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8614) · Estado: **New** · Responsable: **Sin asignar** · Sprint: **G10 - Sprint 03**
> Épica: [[epicas/EP-8631 Correcciones de los profes|EP-8631]] · Tareas cerradas: **0/4**

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

*   [ ] Reglas de negocio: Catálogo de 5 tipos (P4, DEC-018): `REQUIRES`, `RECOMMENDS`, `BELONGS_TO`, `RELATED_TO` y `PART_OF`. Solo `REQUIRES` afecta el desbloqueo; su condición es la regla AND/OR de HU-59 y el XP mínimo de HU-58, que acá no se redefinen. `RECOMMENDS` se muestra pero no bloquea. Cada tipo tiene nombre visible y visibilidad configurable.
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
*   [ ] **CA5**: Una relación `REQUIRES` alimenta las reglas de HU-58 y HU-59 (no define una condición propia).

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
*   Riesgos y mitigación (opcional): Ninguno abierto (P4 respondida el 2026-10-15).


## Tareas

- [ ] #9193 T-65.1 Catálogo de los 5 tipos de relación · New · Iker Alonso
- [ ] #9195 T-65.2 Ver el nombre de cada relación y ocultar tipos · New · Mateo Delgado Costa
- [ ] #9197 T-65.3 Elegir el tipo al crear una relación · New · Mateo Delgado Costa
- [ ] #9353 T-65.4 Wiki, OpenAPI y diagrama de secuencia · New · Quinteros Tomás
