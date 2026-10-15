---
tags: [tpi, g10, sprint-3, historia, hu]
id: C02
tipo: HU
epica: "EP-S3-2"
capa: "Back + Front"
esfuerzo: L
puntos: 8
prioridad: Must
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [M03]
---

# C02: Relaciones con tipo

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-2 Correcciones de los profes|EP-S3-2]] · **HU** · Capa: **Back + Front** · **8 pts** · **Must** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HU-xx — Relaciones con tipo** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: PROFESOR
- **Quiero**: relacionar nodos y unidades con tipos de relación, ver el nombre de cada relación y elegir cuáles se muestran
- **Para**: que el mapa muestre cómo se conectan los temas, no solo qué bloquea a qué

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Catálogo de tipos: `REQUIRES`, `BELONGS_TO`, `RELATED_TO` y un cuarto a definir (P4). Solo `REQUIRES` afecta el desbloqueo. Cada tipo tiene nombre visible y visibilidad configurable.
- [ ] Seguridad (roles, permisos, datos sensibles): ADMIN, GESTOR o PROFESSOR dueño.
- [ ] Accesibilidad (WCAG/teclado/lectores): La relación se distingue por texto y forma de línea, no solo por color.

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: Catálogo de tipos de relación con nombre y visibilidad.
- [ ] **CA2**: La arista muestra el nombre del tipo.
- [ ] **CA3**: El profesor oculta un tipo y deja de verse en el mapa.
- [ ] **CA4**: Solo `REQUIRES` cambia el desbloqueo.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Relaciones con tipo

**Escenario 1**

- **Dado**: dos nodos
- **Cuando**: el profesor los une con `RELATED_TO`
- **Entonces**: la arista dice «Relacionado con» y no bloquea nada

**Escenario 2**

- **Dado**: el tipo `BELONGS_TO` oculto
- **Cuando**: el alumno abre el mapa
- **Entonces**: no ve esas aristas

**Escenario 3**

- **Dado**: una relación `REQUIRES`
- **Cuando**: el alumno no completó el origen
- **Entonces**: el destino sigue bloqueado

* * *

## Prototipo

- **Capturas**: Aristas con etiqueta en el grafo.
- **URL Figma**: Pendiente.
- **Storybook**: `generic-node-graph`.
- **Mock API / Swagger**: Tipos de relación en `/roadmaps/{id}/graph`.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 8
- **Prioridad (MoSCoW / Numérica)**: Must

* * *

## Dependencias / Impactos

- Servicios involucrados: Ninguno.
- Módulos afectados: Módulo graph, vista de grafo, mapa del alumno.
- Otros equipos / aprobaciones: Ninguno.
- Impacto en datos / migraciones: Relaciones con tipo en Neo4j.
- Riesgos y mitigación (opcional): Depende de P4.

## Tareas

- [ ] T-C02.1 Catálogo de tipos en el módulo graph
- [ ] T-C02.2 Etiqueta y visibilidad en el front
- [ ] T-C02.3 Tests

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

Solo existe la relación "prerrequisito" con modo AND/OR.

### Depende de

- [[sprints/sprint-3/historias/M03 Módulo graph en Neo4j y migración inicial|M03]] Módulo graph en Neo4j y migración inicial

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P4]]
