---
tags: [tpi, g10, sprint-3, historia, ht]
id: B01
tipo: HT
epica: "EP-S3-0"
capa: "Back"
esfuerzo: S
puntos: 2
prioridad: Must
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: []
---

# B01: Cerrar o mergear las ramas colgadas del back

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-0 Deuda del Sprint 2|EP-S3-0]] · **HT** · Capa: **Back** · **2 pts** · **Must** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HT-xx — Cerrar o mergear las ramas colgadas del back** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: EQUIPO DE DESARROLLO
- **Quiero**: decidir cada rama sin mergear del back (mergear o cerrar) con un criterio escrito
- **Para**: que develop sea la única fuente de verdad y nadie construya sobre código que no va a llegar

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: `feature/t-21-7-roadmap-events-topic` es redundante: develop ya publica en `roadmap.events` por defecto (#134). `revert-130-feature/5390-ranking-rules-parity` deja el ranking sin tests y no se mergea. `bypass-desafio-11-10` es de demo: su flag no puede llegar encendido a producción.
- [ ] Validaciones: `fix/account-not-found-gate` se prueba en el entorno integrado contra #193 (404 `ACCOUNT_NOT_FOUND` de Inventario) antes de decidir.
- [ ] Otros: Cada rama cerrada deja un comentario en su PR con el motivo.

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: `feature/t-21-7-roadmap-events-topic` cerrada sin mergear, con el motivo en el PR.
- [ ] **CA2**: `fix/account-not-found-gate` mergeada si cubre algo que #193 no cubre, o cerrada con el motivo.
- [ ] **CA3**: `bypass-desafio-11-10` cerrada, o mergeada con el flag apagado por defecto y documentado como solo demo.
- [ ] **CA4**: `revert-130-…` cerrada sin mergear.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Limpieza de ramas del back

**Escenario 1**

- **Dado**: la rama `feature/t-21-7-roadmap-events-topic` y develop con `roadmap.events` por defecto
- **Cuando**: se revisa la rama
- **Entonces**: se cierra sin mergear con el motivo en el PR

**Escenario 2**

- **Dado**: la rama `fix/account-not-found-gate` y develop con #193
- **Cuando**: se prueba en el entorno integrado un alumno sin cuenta en Accounting
- **Entonces**: se decide mergear o cerrar según si el 404 ya llega bien

**Escenario 3**

- **Dado**: la rama `revert-130-…`
- **Cuando**: se revisa
- **Entonces**: se cierra sin mergear porque deja el ranking sin tests

* * *

## Prototipo

- **Capturas**: No aplica (sin pantalla).
- **URL Figma**: No aplica.
- **Storybook**: No aplica.
- **Mock API / Swagger**: No aplica.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 2
- **Prioridad (MoSCoW / Numérica)**: Must

* * *

## Dependencias / Impactos

- Servicios involucrados: Ninguno.
- Módulos afectados: Ramas del repo `tpi-roadmap`.
- Otros equipos / aprobaciones: Ninguno.
- Impacto en datos / migraciones: Sin migración.
- Riesgos y mitigación (opcional): Cerrar una rama con trabajo útil; mitigación: revisar el diff completo y dejar el motivo en el PR.

## Tareas

- [ ] T-B01.1 Revisar y cerrar `feature/t-21-7-roadmap-events-topic` y `revert-130-…`
- [ ] T-B01.2 Probar `fix/account-not-found-gate` contra #193 y decidir
- [ ] T-B01.3 Decidir `bypass-desafio-11-10`

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

Hay ramas sin decidir: `feature/t-21-7-roadmap-events-topic` (redundante con #134), `fix/account-not-found-gate` (a revisar contra #193), `bypass-desafio-11-10` (flag de demo) y `revert-130-feature/5390-ranking-rules-parity` (deja el ranking sin tests).

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|E5]]

### Deuda técnica que cierra

- [[deuda-tecnica|DT-17]]
