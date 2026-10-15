---
tags: [tpi, g10, sprint-3, historia, ht]
id: C09
tipo: HT
epica: "EP-S3-2"
capa: "Back"
esfuerzo: M
puntos: 5
prioridad: Should
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: []
---

# C09: Permisos en vez de roles

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-2 Correcciones de los profes|EP-S3-2]] · **HT** · Capa: **Back** · **5 pts** · **Should** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HT-xx — Permisos en vez de roles** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: EQUIPO DE DESARROLLO
- **Quiero**: autorizar por permisos y no por roles, con el catálogo de G06
- **Para**: que los permisos se configuren desde los parámetros globales sin cambiar código

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Matriz rol → permisos escrita (DT-03) y acordada con G06. Los chequeos de dueño del curso se mantienen.
- [ ] Seguridad (roles, permisos, datos sensibles): Cada `@PreAuthorize` usa `hasAuthority('roadmap.…')`. El gate valida el scope `roadmap.gate.read` (DT-01).
- [ ] Otros: Las reglas ya están en constantes por controller (`CAN_EDIT`, `CAN_VIEW`…): en gran parte es reemplazarlas.

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: Matriz rol → permisos escrita y acordada con G06.
- [ ] **CA2**: Todos los `@PreAuthorize` usan permisos.
- [ ] **CA3**: `RankingController` y `requireOwner` sin chequeos de rol a mano.
- [ ] **CA4**: El gate valida su scope.
- [ ] **CA5**: Tests de autorización por endpoint.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Permisos

**Escenario 1**

- **Dado**: un usuario con el permiso `roadmap.graph.edit`
- **Cuando**: edita un nodo de su curso
- **Entonces**: puede

**Escenario 2**

- **Dado**: un usuario sin ese permiso
- **Cuando**: edita un nodo
- **Entonces**: recibe 403

**Escenario 3**

- **Dado**: un servicio sin `roadmap.gate.read`
- **Cuando**: consulta el gate
- **Entonces**: recibe 403

* * *

## Prototipo

- **Capturas**: No aplica (sin pantalla).
- **URL Figma**: No aplica.
- **Storybook**: No aplica.
- **Mock API / Swagger**: No aplica.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 5
- **Prioridad (MoSCoW / Numérica)**: Should

* * *

## Dependencias / Impactos

- Servicios involucrados: Backoffice (catálogo de permisos), API Gateway (cómo llegan).
- Módulos afectados: Todos los controllers, `SecurityConfig`, `GatewayHeadersFilter`.
- Otros equipos / aprobaciones: G06 (bloqueante).
- Impacto en datos / migraciones: Sin migración.
- Riesgos y mitigación (opcional): Que G06 no tenga el catálogo; mitigación: proponer los nombres nosotros.

## Tareas

- [ ] T-C09.1 Matriz rol → permisos
- [ ] T-C09.2 Acordar con G06
- [ ] T-C09.3 Migrar los `@PreAuthorize`
- [ ] T-C09.4 Scope del gate
- [ ] T-C09.5 Tests de autorización

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

Las reglas usan `hasRole`/`hasAnyRole` en constantes por controller (`CAN_EDIT`, `CAN_VIEW`…), más chequeos a mano en `RankingController` y `requireOwner`. El gate acepta cualquier servicio sin validar el scope `roadmap.gate.read`.

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|G2]]
- [[sprints/sprint-3/08-dudas|G6]]

### Deuda técnica que cierra

- [[deuda-tecnica|DT-01]]
- [[deuda-tecnica|DT-02]]
- [[deuda-tecnica|DT-03]]
