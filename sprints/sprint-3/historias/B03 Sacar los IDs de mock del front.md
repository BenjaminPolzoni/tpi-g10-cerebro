---
tags: [tpi, g10, sprint-3, historia, ht]
id: B03
tipo: HT
epica: "EP-S3-0"
capa: "Front"
esfuerzo: S
puntos: 3
prioridad: Must
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: []
---

# B03: Sacar los IDs de mock del front

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-0 Deuda del Sprint 2|EP-S3-0]] · **HT** · Capa: **Front** · **3 pts** · **Must** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HT-xx — Sacar los IDs de mock del front** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: ALUMNO
- **Quiero**: ver siempre mis datos y los de mi curso, nunca los de un alumno o curso de prueba
- **Para**: confiar en lo que muestra el roadmap y el ranking

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: El alumno sale de la sesión y el curso de la ruta. Sin sesión o sin curso se muestra un error; nunca un respaldo silencioso.
- [ ] Validaciones: No quedan referencias a `DEMO_STUDENT_ID`, `COURSE_SEED_ID` ni `CURRENT_STUDENT_ID` fuera de tests y mocks.
- [ ] Seguridad (roles, permisos, datos sensibles): Un alumno no puede ver datos de otro por un id fijo en el código.
- [ ] Accesibilidad (WCAG/teclado/lectores): El mensaje de error se anuncia (`aria-live`).

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: `roadmap.store.ts`, `hex-world-page` y `challenge-attempt.service` toman el alumno de la sesión.
- [ ] **CA2**: `RoadmapStore` y `ranking-panel` toman el curso de la ruta.
- [ ] **CA3**: `ranking-detail` usa el alumno de la sesión.
- [ ] **CA4**: Sin sesión o sin curso se muestra un error claro.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Datos reales en lugar de mocks

**Escenario 1**

- **Dado**: un alumno logueado en el curso X
- **Cuando**: abre el roadmap
- **Entonces**: ve su progreso del curso X

**Escenario 2**

- **Dado**: un alumno logueado
- **Cuando**: abre el detalle del ranking
- **Entonces**: su fila resaltada es la suya

**Escenario 3**

- **Dado**: una sesión vencida
- **Cuando**: se abre el roadmap
- **Entonces**: se muestra un error y no los datos de un alumno de prueba

* * *

## Prototipo

- **Capturas**: Roadmap, mundo hexagonal y ranking.
- **URL Figma**: No aplica (sin cambio visual).
- **Storybook**: No aplica.
- **Mock API / Swagger**: Sin cambios de API.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 3
- **Prioridad (MoSCoW / Numérica)**: Must

* * *

## Dependencias / Impactos

- Servicios involucrados: Ninguno nuevo.
- Módulos afectados: `roadmap.store.ts`, `hex-world-page`, `challenge-attempt.service`, `ranking-panel`, `ranking-detail`.
- Otros equipos / aprobaciones: Ninguno.
- Impacto en datos / migraciones: Sin migración.
- Riesgos y mitigación (opcional): Pantallas que dependían del respaldo fallan en desarrollo; mitigación: usar el proxy con headers de un alumno demo real.

## Tareas

- [ ] T-B03.1 Reemplazar `DEMO_STUDENT_ID` por el alumno de la sesión
- [ ] T-B03.2 Reemplazar `COURSE_SEED_ID` por el curso de la ruta
- [ ] T-B03.3 Reemplazar `CURRENT_STUDENT_ID` en `ranking-detail`
- [ ] T-B03.4 Tests de las pantallas sin sesión

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

`DEMO_STUDENT_ID` se usa de respaldo en `roadmap.store.ts`, `hex-world-page` y `challenge-attempt.service`. `COURSE_SEED_ID` es el curso por defecto del store y del `ranking-panel`. `CURRENT_STUDENT_ID` (mock) en `ranking-detail`.

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

Ninguna.

### Deuda técnica que cierra

- [[deuda-tecnica|DT-09]]
