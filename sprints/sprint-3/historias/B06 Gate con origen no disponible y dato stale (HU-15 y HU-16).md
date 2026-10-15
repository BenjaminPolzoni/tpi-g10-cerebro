---
tags: [tpi, g10, sprint-3, historia, hu]
id: B06
tipo: HU
epica: "EP-S3-0"
capa: "Back"
esfuerzo: M
puntos: 5
prioridad: Should
estado: Propuesta
responsable: ""
taiga: "HU-15, HU-16"
depende: []
---

# B06: Gate con origen no disponible y dato stale (HU-15 y HU-16)

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-0 Deuda del Sprint 2|EP-S3-0]] · **HU** · Capa: **Back** · **5 pts** · **Should** · Taiga: [[taiga/historias/HU-15 Impedir la entrega en un nodo bloqueado (gate, vocabulario v3)|HU-15]], [[taiga/historias/HU-16 Integración real con Inventario para las vidas del gate|HU-16]]
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HU-15, HU-16 — Gate con origen no disponible y dato stale (HU-15 y HU-16)**

* * *

## Descripción (Como / Quiero / Para)

- **Como**: ALUMNO
- **Quiero**: recibir un motivo claro cuando no puedo entrar a un desafío porque otro servicio está caído
- **Para**: entender que no es mi culpa y reintentar más tarde

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Fail-closed (DEC-003): si Accounting o Courses no responden y no hay caché vigente, el gate bloquea con `origen_no_disponible`. El gate nunca habilita con un dato `stale`; la pantalla de inventario sí puede mostrarlo con aviso.
- [ ] Performance (tiempos, volumen, límites): Timeouts cortos hacia Accounting y Courses para no superar el P95 de 200 ms.
- [ ] Seguridad (roles, permisos, datos sensibles): Sin cambios de permisos.

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: Con Accounting caído y sin caché vigente: `eligible=false`, `reason=origen_no_disponible` (no 503).
- [ ] **CA2**: Con Courses caído al leer comisiones o restricciones: mismo motivo.
- [ ] **CA3**: Con un dato `stale` el gate no habilita.
- [ ] **CA4**: El front muestra un texto para `origen_no_disponible`.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Gate con servicios caídos

**Escenario 1**

- **Dado**: Accounting caído y sin caché
- **Cuando**: el Motor consulta el gate
- **Entonces**: recibe `eligible=false` con `reason=origen_no_disponible`

**Escenario 2**

- **Dado**: una caché de vidas vencida
- **Cuando**: el Motor consulta el gate
- **Entonces**: no habilita con ese dato

**Escenario 3**

- **Dado**: Courses caído con `ROADMAP_BY_GROUP_ENABLED=true`
- **Cuando**: se consulta el gate
- **Entonces**: devuelve `origen_no_disponible`

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

- Servicios involucrados: Accounting, Courses.
- Módulos afectados: `GateService`, `GateEvaluator`, `InventoryService`.
- Otros equipos / aprobaciones: Ninguno.
- Impacto en datos / migraciones: Sin migración.
- Riesgos y mitigación (opcional): Cambiar 503 por 200 con motivo puede romper al Motor si espera 503; mitigación: avisar a G09 y actualizar el acta del gate.

## Tareas

- [ ] T-B06.1 Motivo `origen_no_disponible` en el gate
- [ ] T-B06.2 Tests de servicios caídos y caché vencida
- [ ] T-B06.3 Avisar a G09 y actualizar el acta del gate

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

Si Accounting o Courses no responden, el gate devuelve 503 en vez del motivo `origen_no_disponible`. La pantalla de inventario usa el último dato de 24 h con `stale`, pero el gate no (y no debe usarlo para habilitar).

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|E9]]
