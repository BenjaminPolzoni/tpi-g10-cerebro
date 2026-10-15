---
tags: [tpi, g10, sprint-3, historia, ht]
id: M12
tipo: HT
epica: "EP-S3-1"
capa: "Back"
esfuerzo: M
puntos: 5
prioridad: Must
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [M05, M06]
---

# M12: Gate y progreso con reglas combinadas y XP mínimo

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-1 Múltiples roadmaps por curso y grafo configurable|EP-S3-1]] · **HT** · Capa: **Back** · **5 pts** · **Must** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HT-xx — Gate y progreso con reglas combinadas y XP mínimo** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: EQUIPO DE DESARROLLO
- **Quiero**: que el gate y el progreso evalúen las reglas combinadas y el XP mínimo con el mismo evaluador
- **Para**: que el alumno vea bloqueado exactamente lo que el gate bloquea

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Un único evaluador para el gate y el recorrido (como hoy `block_reason`).
- [ ] Performance (tiempos, volumen, límites): El P95 del gate no supera 200 ms con la caché de reglas.

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: El gate y el recorrido usan el mismo evaluador sobre el árbol de reglas.
- [ ] **CA2**: El XP mínimo de sección se evalúa.
- [ ] **CA3**: Tests BDD con el ejemplo de los profes (secciones 1 a 5).
- [ ] **CA4**: Medición del P95 del gate.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Gate con reglas nuevas

**Escenario 1**

- **Dado**: el ejemplo de los profes
- **Cuando**: un alumno completa las secciones 1 y 2
- **Entonces**: se desbloquea la 3 y la 5 sigue bloqueada

**Escenario 2**

- **Dado**: la sección 4 con XP ≥ 500
- **Cuando**: el alumno llega a 500 XP
- **Entonces**: la 4 se desbloquea

**Escenario 3**

- **Dado**: una regla `A y (B o C)`
- **Cuando**: el Motor consulta el gate
- **Entonces**: responde igual que el recorrido

* * *

## Prototipo

- **Capturas**: No aplica (sin pantalla).
- **URL Figma**: No aplica.
- **Storybook**: No aplica.
- **Mock API / Swagger**: No aplica.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 5
- **Prioridad (MoSCoW / Numérica)**: Must

* * *

## Dependencias / Impactos

- Servicios involucrados: Ninguno.
- Módulos afectados: `GateEvaluator`, `GateService`, servicio de progreso.
- Otros equipos / aprobaciones: G09 (el gate es su contrato).
- Impacto en datos / migraciones: Sin migración.
- Riesgos y mitigación (opcional): Latencia; mitigación: caché de reglas.

## Tareas

- [ ] T-M12.1 Evaluador sobre árbol de reglas
- [ ] T-M12.2 XP mínimo
- [ ] T-M12.3 BDD del ejemplo de los profes
- [ ] T-M12.4 Medir el P95

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

`GateEvaluator` evalúa un modo AND/OR por sección o nodo, sin XP mínimo.

### Depende de

- [[sprints/sprint-3/historias/M05 Dependencias entre secciones|M05]] Dependencias entre secciones
- [[sprints/sprint-3/historias/M06 Dependencias entre nodos con reglas combinadas|M06]] Dependencias entre nodos con reglas combinadas

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|P7]]
