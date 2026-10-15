---
tags: [tpi, g10, sprint-3, historia, hu]
id: B04
tipo: HU
epica: "EP-S3-0"
capa: "Back"
esfuerzo: M
puntos: 3
prioridad: Must
estado: Propuesta
responsable: ""
taiga: "HU-48"
depende: []
---

# B04: Pre-chequeo de elegibilidad para el alumno (HU-48)

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-0 Deuda del Sprint 2|EP-S3-0]] · **HU** · Capa: **Back** · **3 pts** · **Must** · Taiga: [[taiga/historias/HU-48 Saber si puedo entrar a un desafío antes de abrirlo|HU-48]]
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HU-48 — Pre-chequeo de elegibilidad para el alumno (HU-48)**

* * *

## Descripción (Como / Quiero / Para)

- **Como**: ALUMNO
- **Quiero**: que al elegir un desafío se valide con mi sesión si puedo entrar y, si no, por qué
- **Para**: no chocar con un error genérico del Motor

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Usa el mismo `GateService` y el mismo vocabulario que el gate del Motor (`not_enrolled`, `content_not_read`, `prerequisite_pending`, `no_lives`, …). No crea intentos ni modifica nada. El Motor vuelve a consultar el gate del lado del servidor.
- [ ] Validaciones: Nodo de desafío del curso; el alumno sale del token.
- [ ] Datos obligatorios: `courseId` y `nodeId`. El `studentId` nunca viaja en la ruta.
- [ ] Performance (tiempos, volumen, límites): P95 por debajo de 200 ms, igual que el gate.
- [ ] Seguridad (roles, permisos, datos sensibles): Rol STUDENT con matrícula activa. Hoy el front llama a `GET /courses/{c}/students/{s}/nodes/{n}/eligibility`, que `SecurityConfig` reserva a `ServiceIdentity`: con el JWT del alumno da 403.
- [ ] Otros: El PR #175 cerró las tareas de HU-48 pero el endpoint para el alumno no está en develop. Borrar `ProgressService.startChallenge` (código muerto).

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: Existe `GET /api/roadmap/courses/{courseId}/nodes/{nodeId}/eligibility` para el alumno, con su JWT.
- [ ] **CA2**: Devuelve `{eligible, reason, challenge_id, attempt_type}` con el mismo evaluador que el gate.
- [ ] **CA3**: El front llama a este endpoint y no al del Motor.
- [ ] **CA4**: `ProgressService.startChallenge` borrado.
- [ ] **CA5**: OpenAPI actualizado.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Chequeo previo del alumno

**Escenario 1**

- **Dado**: un desafío con contenido obligatorio sin leer
- **Cuando**: el alumno lo elige
- **Entonces**: recibe `eligible=false`, `reason=content_not_read`, y no se llama al Motor

**Escenario 2**

- **Dado**: un alumno con 0 vidas y un nodo STANDARD
- **Cuando**: consulta su elegibilidad
- **Entonces**: recibe `reason=no_lives`

**Escenario 3**

- **Dado**: un desafío habilitado
- **Cuando**: el alumno lo elige
- **Entonces**: recibe `eligible=true` con su `attempt_type` y el front abre el intento

* * *

## Prototipo

- **Capturas**: Torre del mundo hexagonal y desafío del mapa de sección con el motivo de bloqueo.
- **URL Figma**: Pendiente.
- **Storybook**: Pendiente.
- **Mock API / Swagger**: GET /api/roadmap/courses/{courseId}/nodes/{nodeId}/eligibility → {eligible, reason, challenge_id, attempt_type}.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 3
- **Prioridad (MoSCoW / Numérica)**: Must

* * *

## Dependencias / Impactos

- Servicios involucrados: Accounting (vidas, vía gate), Courses (matrícula), API Gateway.
- Módulos afectados: `GateController` o `ProgressController`, `GateService`, `SecurityConfig`, `challenge-attempt.service` (front).
- Otros equipos / aprobaciones: Ninguno bloqueante.
- Impacto en datos / migraciones: Sin migración.
- Riesgos y mitigación (opcional): Que el chequeo del alumno y el del Motor difieran; mitigación: ambos usan `GateService`.

## Tareas

- [ ] T-B04.1 Endpoint de elegibilidad para el alumno sobre `GateService`
- [ ] T-B04.2 Front: usar el endpoint del alumno
- [ ] T-B04.3 Borrar `ProgressService.startChallenge`
- [ ] T-B04.4 BDD y OpenAPI

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

El PR #175 cerró las tareas de HU-48, pero en develop el único endpoint de elegibilidad es el del Motor (`/courses/{c}/students/{s}/nodes/{n}/eligibility`), que `SecurityConfig` reserva a `ServiceIdentity`. El front llama a ese endpoint con el JWT del alumno, así que en el entorno integrado recibe 403. `ProgressService.startChallenge` quedó como código muerto.

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

Ninguna.

### Deuda técnica que cierra

- [[deuda-tecnica|DT-04]]
