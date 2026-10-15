---
tags: [tpi, g10, sprint-3, historia, spike]
id: M01
tipo: Spike
epica: "EP-S3-1"
capa: "Back + Infra"
esfuerzo: S
puntos: 3
prioridad: Must
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: []
---

# M01: Validar la infra de Neo4j y modelar las relaciones

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-1 Múltiples roadmaps por curso y grafo configurable|EP-S3-1]] · **Spike** · Capa: **Back + Infra** · **3 pts** · **Must** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HT-xx — Validar la infra de Neo4j y modelar las relaciones** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: EQUIPO DE DESARROLLO
- **Quiero**: validar que Neo4j corre en la plataforma y dejar escrito el modelo de nodos y relaciones
- **Para**: arrancar la migración sin sorpresas de infra ni de modelo

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Neo4j está decidido por los profes (DEC-016). El spike no elige base: valida infra y modelo. Neo4j Community (GPLv3) en Docker.
- [ ] Validaciones: La prueba de concepto corre en el CI con Testcontainers.
- [ ] Otros: El modelo incluye START/END (C01) y tipos de relación (C02); los huecos dependen de P1 y P4.

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: Neo4j levantado en el compose local con volumen persistente.
- [ ] **CA2**: Acordado con plataforma quién lo suma a la mesh y a la demo (G1), registrado en `acuerdos/`.
- [ ] **CA3**: Prueba de concepto con Spring Data Neo4j y Testcontainers en el CI.
- [ ] **CA4**: Modelo de nodos y relaciones escrito en `04-base-de-grafos`.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Spike de Neo4j

**Escenario 1**

- **Dado**: un clon limpio del back
- **Cuando**: se corre `docker compose up`
- **Entonces**: Neo4j levanta junto con Postgres

**Escenario 2**

- **Dado**: la prueba de concepto
- **Cuando**: corre el CI
- **Entonces**: el test con Testcontainers de Neo4j pasa

**Escenario 3**

- **Dado**: el modelo escrito
- **Cuando**: el equipo lo revisa
- **Entonces**: cubre roadmaps, secciones, nodos, reglas, START/END y tipos de relación

* * *

## Prototipo

- **Capturas**: No aplica (sin pantalla).
- **URL Figma**: No aplica.
- **Storybook**: No aplica.
- **Mock API / Swagger**: No aplica.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 3
- **Prioridad (MoSCoW / Numérica)**: Must

* * *

## Dependencias / Impactos

- Servicios involucrados: Plataforma (`tpi-system-compose`, mesh).
- Módulos afectados: Infra del back, CI.
- Otros equipos / aprobaciones: Quien mantiene la plataforma (G1).
- Impacto en datos / migraciones: Sin migración (solo prueba).
- Riesgos y mitigación (opcional): Que la plataforma no tenga recursos para Neo4j; mitigación: acordarlo la primera semana.

## Tareas

- [ ] T-M01.1 Neo4j en el compose local
- [ ] T-M01.2 Acordar Neo4j con plataforma (G1)
- [ ] T-M01.3 Prueba de concepto con Spring Data Neo4j + Testcontainers
- [ ] T-M01.4 Modelo escrito en 04

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

Neo4j está decidido (DEC-016) pero no existe en el compose ni en la mesh.

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|G1]]
- [[sprints/sprint-3/08-dudas|P1]]
- [[sprints/sprint-3/08-dudas|P4]]
