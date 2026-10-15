---
tags: [tpi, g10, sprint-3, historia, ht]
id: U03
tipo: HT
epica: "EP-S3-3"
capa: "Front"
esfuerzo: M
puntos: 5
prioridad: Could
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [U01]
---

# U03: Colores y espaciado del roadmap con tokens

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-3 Consistencia visual con la UI-KIT|EP-S3-3]] · **HT** · Capa: **Front** · **5 pts** · **Could** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HT-xx — Colores y espaciado del roadmap con tokens** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: EQUIPO DE DESARROLLO
- **Quiero**: que el roadmap use los tokens del kit para colores, espaciado y tipografía
- **Para**: que el tema claro y oscuro funcione igual que en el resto

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Se borra el puente `--color-*`. Quedan afuera `engine/` y el arte.
- [ ] Validaciones: Regla de `stylelint` contra hex/rgb literales en las carpetas de G10.

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: Puente `--color-*` borrado.
- [ ] **CA2**: Sin colores literales fuera de `engine/` y arte.
- [ ] **CA3**: Regla de `stylelint` activa.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Tokens del kit

**Escenario 1**

- **Dado**: el roadmap
- **Cuando**: se cambia a tema oscuro
- **Entonces**: todos los componentes cambian

**Escenario 2**

- **Dado**: un color literal nuevo
- **Cuando**: se commitea
- **Entonces**: `stylelint` falla

**Escenario 3**

- **Dado**: `engine/`
- **Cuando**: tiene colores literales
- **Entonces**: la regla no lo marca

* * *

## Prototipo

- **Capturas**: Roadmap en tema claro y oscuro.
- **URL Figma**: No aplica.
- **Storybook**: Tokens del kit.
- **Mock API / Swagger**: No aplica.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 5
- **Prioridad (MoSCoW / Numérica)**: Could

* * *

## Dependencias / Impactos

- Servicios involucrados: Ninguno.
- Módulos afectados: CSS del roadmap.
- Otros equipos / aprobaciones: Ninguno.
- Impacto en datos / migraciones: Sin migración.
- Riesgos y mitigación (opcional): Regresiones visuales; mitigación: tests visuales.

## Tareas

- [ ] T-U03.1 Reemplazar colores
- [ ] T-U03.2 Borrar el puente
- [ ] T-U03.3 Regla de stylelint

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

316 colores hardcodeados y un puente de tokens `--color-*` propio.

### Depende de

- [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs|U01]] Subir la UI-KIT a 0.8.0 y cerrar sus TODOs

### Dudas que la frenan

Ninguna.

### Deuda técnica que cierra

- [[deuda-tecnica|DT-15]]
