---
tags: [tpi, g10, sprint-3, historia, ht]
id: U05
tipo: HT
epica: "EP-S3-3"
capa: "Front"
esfuerzo: S
puntos: 3
prioridad: Should
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [U01]
---

# U05: Ranking con componentes del kit

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-3 Consistencia visual con la UI-KIT|EP-S3-3]] · **HT** · Capa: **Front** · **3 pts** · **Should** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HT-xx — Ranking con componentes del kit** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: ALUMNO
- **Quiero**: el ranking con la misma tabla y chips que el resto de la plataforma
- **Para**: leerlo igual que las otras tablas

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Se mantiene el anonimato de filas ajenas (DEC-007).
- [ ] Accesibilidad (WCAG/teclado/lectores): Tabla con `caption` y encabezados del kit.

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: `generic-table` y `generic-badge` en `ranking/*`.
- [ ] **CA2**: Anonimato intacto.
- [ ] **CA3**: Tests visuales.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Ranking con el kit

**Escenario 1**

- **Dado**: el ranking
- **Cuando**: se abre
- **Entonces**: usa `generic-table`

**Escenario 2**

- **Dado**: una fila ajena
- **Cuando**: se ve
- **Entonces**: sigue sin datos personales

**Escenario 3**

- **Dado**: un lector de pantalla
- **Cuando**: recorre la tabla
- **Entonces**: lee el caption y los encabezados

* * *

## Prototipo

- **Capturas**: Ranking.
- **URL Figma**: No aplica.
- **Storybook**: `generic-table`.
- **Mock API / Swagger**: No aplica.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 3
- **Prioridad (MoSCoW / Numérica)**: Should

* * *

## Dependencias / Impactos

- Servicios involucrados: Ninguno.
- Módulos afectados: `ranking/*`.
- Otros equipos / aprobaciones: Ninguno.
- Impacto en datos / migraciones: Sin migración.
- Riesgos y mitigación (opcional): Ninguno.

## Tareas

- [ ] T-U05.1 Tabla y chips del kit
- [ ] T-U05.2 Tests

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

El ranking tiene 3 `<table>` crudas y chips propios.

### Depende de

- [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs|U01]] Subir la UI-KIT a 0.8.0 y cerrar sus TODOs

### Dudas que la frenan

Ninguna.
