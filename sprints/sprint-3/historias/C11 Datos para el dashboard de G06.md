---
tags: [tpi, g10, sprint-3, historia, ht]
id: C11
tipo: HT
epica: "EP-S3-2"
capa: "Back + acuerdo"
esfuerzo: S
puntos: 2
prioridad: Should
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: []
---

# C11: Datos para el dashboard de G06

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-2 Correcciones de los profes|EP-S3-2]] · **HT** · Capa: **Back + acuerdo** · **2 pts** · **Should** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HT-xx — Datos para el dashboard de G06** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: BACKOFFICE (G06)
- **Quiero**: saber qué datos de progreso, ranking y XP me da Roadmap y por dónde
- **Para**: armar el dashboard entre todos los grupos

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Ya existen endpoints de progreso, ranking, nivel y avance por grupo, y el topic `roadmap.events`.
- [ ] Seguridad (roles, permisos, datos sensibles): Lectura entre servicios con scope (`roadmap.progress.read`).

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: Acordado con G06 qué datos y por dónde (REST o eventos).
- [ ] **CA2**: Registrado en `acuerdos/`.
- [ ] **CA3**: Si hace falta algo nuevo, queda como HU.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Datos para el dashboard

**Escenario 1**

- **Dado**: el dashboard de G06
- **Cuando**: pide el progreso agregado de un curso
- **Entonces**: lo recibe con su scope

**Escenario 2**

- **Dado**: un nodo completado
- **Cuando**: se publica en `roadmap.events`
- **Entonces**: G06 lo puede consumir

**Escenario 3**

- **Dado**: un dato que no existe
- **Cuando**: G06 lo pide
- **Entonces**: queda como HU nueva

* * *

## Prototipo

- **Capturas**: No aplica (sin pantalla).
- **URL Figma**: No aplica.
- **Storybook**: No aplica.
- **Mock API / Swagger**: No aplica.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 2
- **Prioridad (MoSCoW / Numérica)**: Should

* * *

## Dependencias / Impactos

- Servicios involucrados: Backoffice.
- Módulos afectados: Endpoints de progreso y ranking, `roadmap.events`.
- Otros equipos / aprobaciones: G06.
- Impacto en datos / migraciones: Sin migración.
- Riesgos y mitigación (opcional): Ninguno.

## Tareas

- [ ] T-C11.1 Reunión con G06
- [ ] T-C11.2 Acta en `acuerdos/`

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

Existen endpoints de progreso, ranking, nivel y avance por grupo, y el topic `roadmap.events`.

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|G3]]
