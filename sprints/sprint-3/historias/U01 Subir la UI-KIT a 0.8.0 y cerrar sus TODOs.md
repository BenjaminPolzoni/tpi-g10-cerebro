---
tags: [tpi, g10, sprint-3, historia, ht]
id: U01
tipo: HT
epica: "EP-S3-3"
capa: "Front"
esfuerzo: S
puntos: 3
prioridad: Must
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: []
---

# U01: Subir la UI-KIT a 0.8.0 y cerrar sus TODOs

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-3 Consistencia visual con la UI-KIT|EP-S3-3]] · **HT** · Capa: **Front** · **3 pts** · **Must** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HT-xx — Subir la UI-KIT a 0.8.0 y cerrar sus TODOs** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: EQUIPO DE DESARROLLO
- **Quiero**: subir el front a la UI-KIT 0.8.0 y cerrar los TODOs que esperaban cambios del kit
- **Para**: usar las mejoras del kit y no mantener parches

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Mergear `feature/ui-lib-0-8-0`. TODOs: #59, #53, #51, #83/#84/#85 y `::ng-deep` de pagination.
- [ ] Validaciones: `npm run verify` y tests visuales en verde.
- [ ] Accesibilidad (WCAG/teclado/lectores): 0.8.0 trae mejoras de aria (#83, #85).

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: Bump a 0.8.0 mergeado con verify y tests visuales en verde.
- [ ] **CA2**: TODOs destrabados cerrados.
- [ ] **CA3**: HU-22: insignias en modo solo lectura en `ranking-detail`.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** UI-KIT 0.8.0

**Escenario 1**

- **Dado**: el front en 0.7.1
- **Cuando**: se mergea el bump
- **Entonces**: verify y los tests visuales pasan

**Escenario 2**

- **Dado**: el TODO #59
- **Cuando**: se usa `interactive=false`
- **Entonces**: las insignias del ranking son de solo lectura

**Escenario 3**

- **Dado**: la pagination
- **Cuando**: se quita el `::ng-deep`
- **Entonces**: sigue centrada

* * *

## Prototipo

- **Capturas**: Ranking y perfil.
- **URL Figma**: No aplica.
- **Storybook**: Storybook del kit 0.8.0.
- **Mock API / Swagger**: No aplica.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 3
- **Prioridad (MoSCoW / Numérica)**: Must

* * *

## Dependencias / Impactos

- Servicios involucrados: Ninguno.
- Módulos afectados: Todo el front.
- Otros equipos / aprobaciones: Coordinar con los otros grupos del front.
- Impacto en datos / migraciones: Sin migración.
- Riesgos y mitigación (opcional): Cambios visuales en pantallas de otros grupos; mitigación: tests visuales.

## Tareas

- [ ] T-U01.1 Mergear el bump
- [ ] T-U01.2 Cerrar TODOs
- [ ] T-U01.3 Avisar a los otros grupos

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

El front está en ^0.7.1. La rama `feature/ui-lib-0-8-0` no está mergeada. Hay 9 TODOs que se destraban con 0.8.0 (incluye ui-kit#59 de HU-22).

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|G13]]

### Deuda técnica que cierra

- [[deuda-tecnica|DT-14]]
