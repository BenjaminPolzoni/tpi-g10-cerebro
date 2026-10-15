---
tags: [tpi, g10, sprint-3, historia, hu]
id: B11
tipo: HU
epica: "EP-S3-0"
capa: "Back"
esfuerzo: M
puntos: 5
prioridad: Must
estado: Propuesta
responsable: ""
taiga: "HU-01, HU-41"
depende: []
---

# B11: Reintentos y edición de nodos (HU-01 y HU-41)

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-0 Deuda del Sprint 2|EP-S3-0]] · **HU** · Capa: **Back** · **5 pts** · **Must** · Taiga: [[taiga/historias/HU-01 Crear nodos en el grafo (unidades, contenidos, desafíos, exámenes)|HU-01]], [[taiga/historias/HU-41 Editar un nodo del roadmap de forma individual|HU-41]]
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HU-01, HU-41 — Reintentos y edición de nodos (HU-01 y HU-41)**

* * *

## Descripción (Como / Quiero / Para)

- **Como**: PROFESOR
- **Quiero**: definir cuántos reintentos tiene un desafío y editar un nodo sin perder su configuración
- **Para**: controlar la dificultad del recorrido sin sorpresas al guardar

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: `reintentos_permitidos` va de 0 al tope del parámetro PAR-13 de Backoffice. Un PUT que no trae `lives_policy` conserva la actual. Si el Motor da de baja un desafío, el nodo queda marcado (CA8 de HU-01).
- [ ] Validaciones: Reintentos dentro del rango; fuera, 400.
- [ ] Seguridad (roles, permisos, datos sensibles): ADMIN, GESTOR o PROFESSOR dueño.
- [ ] Otros: Si M03 pasa los nodos a Neo4j, el campo vive ahí.

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: Campo de reintentos en el nodo, validado contra PAR-13.
- [ ] **CA2**: Un PUT sin `lives_policy` no resetea el nodo a STANDARD.
- [ ] **CA3**: La baja de un desafío del Motor marca el nodo y el profesor lo ve.
- [ ] **CA4**: Tests de los tres casos.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Reintentos y edición segura de nodos

**Escenario 1**

- **Dado**: un nodo con `lives_policy=RECOVERY`
- **Cuando**: el profesor hace PUT sin ese campo
- **Entonces**: el nodo sigue en RECOVERY

**Escenario 2**

- **Dado**: PAR-13 = 3
- **Cuando**: el profesor pone 5 reintentos
- **Entonces**: recibe 400

**Escenario 3**

- **Dado**: el Motor da de baja el desafío de un nodo
- **Cuando**: llega el evento
- **Entonces**: el nodo queda marcado como «desafío no disponible»

* * *

## Prototipo

- **Capturas**: Editor de nodo.
- **URL Figma**: Pendiente.
- **Storybook**: `generic-input` numérico.
- **Mock API / Swagger**: PUT/PATCH /api/roadmap/nodes/{nodeId}.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 5
- **Prioridad (MoSCoW / Numérica)**: Must

* * *

## Dependencias / Impactos

- Servicios involucrados: Backoffice (PAR-13), Motor (baja de desafío).
- Módulos afectados: Entidad y servicio de nodos, `GraphController`, editor de nodo.
- Otros equipos / aprobaciones: G09 (evento de baja).
- Impacto en datos / migraciones: Migración: columna `retries_allowed`.
- Riesgos y mitigación (opcional): Solaparse con M03; mitigación: hacerlo antes y migrarlo junto con el grafo.

## Tareas

- [ ] T-B11.1 Columna y validación de reintentos
- [ ] T-B11.2 Corregir el PUT que resetea `lives_policy`
- [ ] T-B11.3 Consumir la baja de desafío del Motor
- [ ] T-B11.4 Tests

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

No existe el campo `reintentos_permitidos`. Un PUT sin `lives_policy` resetea el nodo a STANDARD. No se consume la baja de desafío del Motor (CA8 de HU-01).

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

Ninguna.
