---
tags: [tpi, g10, sprint-3, historia, ht]
id: C10
tipo: HT
epica: "EP-S3-2"
capa: "Docs"
esfuerzo: S
puntos: 2
prioridad: Should
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: []
---

# C10: Documentación global del micro

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-2 Correcciones de los profes|EP-S3-2]] · **HT** · Capa: **Docs** · **2 pts** · **Should** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HT-xx — Documentación global del micro** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: EQUIPO DE DESARROLLO
- **Quiero**: un documento global del micro: qué hace, modelo, endpoints, eventos, flags, cómo levantarlo y decisiones
- **Para**: que cualquiera entienda el servicio sin preguntar

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Se arma desde el cerebro (`arquitectura/`, `decisiones/`, `acuerdos/`) y los contratos del repo.
- [ ] Otros: Incluye la matriz de roles y permisos (C09).

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: Documento global en el repo del back.
- [ ] **CA2**: Incluye modelo, endpoints, eventos, flags y cómo levantarlo.
- [ ] **CA3**: Enlaza decisiones y contratos.
- [ ] **CA4**: Contratos desactualizados corregidos (DT-18).

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Documentación global

**Escenario 1**

- **Dado**: un integrante nuevo
- **Cuando**: lee el documento
- **Entonces**: levanta el servicio sin ayuda

**Escenario 2**

- **Dado**: otro grupo
- **Cuando**: busca qué eventos publicamos
- **Entonces**: los encuentra con su contrato

**Escenario 3**

- **Dado**: un flag
- **Cuando**: se busca en el documento
- **Entonces**: dice qué hace y su valor por defecto

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

- Servicios involucrados: Ninguno.
- Módulos afectados: `docs/` del back.
- Otros equipos / aprobaciones: Ninguno.
- Impacto en datos / migraciones: Sin migración.
- Riesgos y mitigación (opcional): Ninguno.

## Tareas

- [ ] T-C10.1 Armar el documento
- [ ] T-C10.2 Corregir contratos desactualizados

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

La documentación está repartida por tarea; el README del micro es básico.

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|E7]]

### Deuda técnica que cierra

- [[deuda-tecnica|DT-03]]
- [[deuda-tecnica|DT-18]]
