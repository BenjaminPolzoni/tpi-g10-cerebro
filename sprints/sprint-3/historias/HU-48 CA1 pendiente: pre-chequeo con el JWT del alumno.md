---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-48
estado: Propuesta
responsable: ""
epica: "Deuda del Sprint 2"
sprint: "G10 - Sprint 3"
puntos: 3
prioridad: Must
en_taiga: true
---

# HU-48: CA1 pendiente: pre-chequeo con el JWT del alumno

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Deuda del Sprint 2|Deuda del Sprint 2]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Ya existe en Taiga: [[taiga/historias/HU-48 Saber si puedo entrar a un desafío antes de abrirlo|HU-48]] (épica EP-60). En el Sprint 3 se **reabre** con lo que falta.

[G10] — HU-48 — Saber si puedo entrar a un desafío antes de abrirlo
-------------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: que al elegir un desafío se valide con mi sesión si puedo entrar y, si no, por qué
*   **Para**: no chocar con un error genérico del Motor

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Usa el mismo `GateService` y el mismo vocabulario que el gate del Motor (`not_enrolled`, `content_not_read`, `prerequisite_pending`, `no_lives`, …). No crea intentos ni modifica nada. El Motor vuelve a consultar el gate del lado del servidor.
*   [ ] Validaciones: Nodo de desafío del curso; el alumno sale del token.
*   [ ] Datos obligatorios: `courseId` y `nodeId`. El `studentId` nunca viaja en la ruta.
*   [ ] Performance (tiempos, volumen, límites): P95 por debajo de 200 ms, igual que el gate.
*   [ ] Seguridad (roles, permisos, datos sensibles): Rol STUDENT con matrícula activa. Hoy el front llama a `GET /courses/{c}/students/{s}/nodes/{n}/eligibility`, que `SecurityConfig` reserva a `ServiceIdentity`: con el JWT del alumno da 403.
*   [ ] Accesibilidad (WCAG/teclado/lectores): No aplica.
*   [ ] Otros: El PR #175 cerró las tareas de HU-48 pero el endpoint para el alumno no está en develop. Borrar `ProgressService.startChallenge` (código muerto).

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Existe `GET /api/roadmap/courses/{courseId}/nodes/{nodeId}/eligibility` para el alumno, con su JWT.
*   [ ] **CA2**: Devuelve `{eligible, reason, challenge_id, attempt_type}` con el mismo evaluador que el gate.
*   [ ] **CA3**: El front llama a este endpoint y no al del Motor.
*   [ ] **CA4**: `ProgressService.startChallenge` borrado.
*   [ ] **CA5**: OpenAPI actualizado.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Chequeo previo del alumno

**Escenario 1**  

*   **Dado**: un desafío con contenido obligatorio sin leer
*   **Cuando**: el alumno lo elige
*   **Entonces**: recibe `eligible=false`, `reason=content_not_read`, y no se llama al Motor

**Escenario 2**  

*   **Dado**: un alumno con 0 vidas y un nodo STANDARD
*   **Cuando**: consulta su elegibilidad
*   **Entonces**: recibe `reason=no_lives`

**Escenario 3**  

*   **Dado**: un desafío habilitado
*   **Cuando**: el alumno lo elige
*   **Entonces**: recibe `eligible=true` con su `attempt_type` y el front abre el intento

* * *

Prototipo
---------

*   **Capturas**: Torre del mundo hexagonal y desafío del mapa de sección con el motivo de bloqueo.
*   **URL Figma**: Pendiente.
*   **Storybook**: Pendiente.
*   **Mock API / Swagger**: GET /api/roadmap/courses/{courseId}/nodes/{nodeId}/eligibility → {eligible, reason, challenge_id, attempt_type}.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 3
*   **Prioridad (MoSCoW / Numérica)**: Must

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 3 | Must |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Accounting (vidas, vía gate), Courses (matrícula), API Gateway.
*   Módulos afectados: `GateController` o `ProgressController`, `GateService`, `SecurityConfig`, `challenge-attempt.service` (front).
*   Otros equipos / aprobaciones: Ninguno bloqueante.
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Que el chequeo del alumno y el del Motor difieran; mitigación: ambos usan `GateService`.

## Tareas

- [ ] T-48.5 Endpoint de elegibilidad para el alumno sobre `GateService`
- [ ] T-48.6 Front: usar el endpoint del alumno
- [ ] T-48.7 Borrar `ProgressService.startChallenge`
- [ ] T-48.8 BDD y OpenAPI

---

## Contexto del Sprint 3 (no va a Taiga)

### Criterios de la HU original (Taiga)

Verificados contra `origin/develop` (back `fc1917e`, front `67cbad4a`) el 2026-10-15. ✅ cumple · ❌ no cumple · ⚠️ hecho pero no anda de punta a punta.

- [ ] ❌ **CA1**: Un alumno sin la lectura obligatoria ve «contenido no leído» y no se llama al Motor. — el front llama a `/eligibility`, pero `SecurityConfig` la reserva a `ServiceIdentity`: con el JWT del alumno da 403
- [ ] ⚠️ **CA2**: Un nodo habilitado abre el intento en la misma pestaña con el attempt_type de su política de vidas. — el front navega en la misma pestaña con el `attempt_type`, pero no llega porque falla el CA1
- [ ] ⚠️ **CA3**: Un nodo de recuperación abre con attempt_type RECOVERY aunque el alumno tenga 0 vidas. — el gate exime a RECOVERY de las vidas, pero no llega porque falla el CA1
- [x] ✅ **CA4**: El endpoint POST …/start deja de existir y el OpenAPI lo refleja. — ya no hay `POST …/start` en los controllers

### Qué hay hoy en el código

El PR #175 cerró las tareas de HU-48, pero en develop el único endpoint de elegibilidad es el del Motor (`/courses/{c}/students/{s}/nodes/{n}/eligibility`), que `SecurityConfig` reserva a `ServiceIdentity`. El front llama a ese endpoint con el JWT del alumno, así que en el entorno integrado recibe 403. `ProgressService.startChallenge` quedó como código muerto.

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

Ninguna.

### Deuda técnica que cierra

- [[deuda-tecnica|DT-04]]
