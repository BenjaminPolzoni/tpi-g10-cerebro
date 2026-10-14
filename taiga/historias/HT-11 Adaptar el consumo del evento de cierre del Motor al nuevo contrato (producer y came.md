---
tags: [tpi, g10, taiga, ht]
codigo: HT-11
ref: 7048
estado: "Done"
responsable: "Sin asignar"
epica: "Sin épica"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/7048
---

# HT-11: Adaptar el consumo del evento de cierre del Motor al nuevo contrato (producer y camelCase)

> [!info] Generado desde Taiga (2026-10-14 18:47). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/7048) · Estado: **Done** · Responsable: **Sin asignar** · Sprint: **G10 - Sprint 2**

**Como** equipo de Roadmap (G10)
**quiero** que el listener del evento de cierre del Motor (G09) lea el contrato vigente
**para** volver a registrar XP, progreso y desbloqueos cuando un alumno cierra un intento.

**Origen:** issue de G09 https://github.com/2026-P4-BE/tpi-roadmap/issues/120

**Contexto**
Desde el 05/10 el Motor publica `CHALLENGE_COMPLETED` / `CHALLENGE_ABORTED` en `challenges.events` con:
- `producer = tema-03-challenges-service` (antes `THEME-02-CHALLENGE-ENGINE`), según `contratos-kafka` v5.
- payload entero en camelCase (`userId`, `courseId`, `nodeId`, `attemptId`, `challengeId`, `addLive`, `attemptNumber`, `closureReason`, etc.).

Hoy `RoadmapEventListener` filtra por el producer anterior y `ChallengeClosurePayload` lee snake_case: todos los cierres se descartan. Bloquea HU-03 en el entorno integrado y lo que depende del cierre (HU-21, HU-38, ranking).

Contrato de G09: https://github.com/2026-P4-BE/tpi-engine-challenge/blob/develop/docs/contracts/eventos-bus.md

**Criterios de aceptación**
- El listener procesa los eventos con `producer = tema-03-challenges-service` e ignora el producer anterior.
- `ChallengeClosurePayload` lee solo los nombres en camelCase, sin alias (las dos formas no conviven).
- Los tests usan los ejemplos literales del contrato de G09 y cubren: producer anterior ignorado, payload en snake_case a la DLT y convivencia con `spring.jackson.property-naming-strategy=SNAKE_CASE`.
- `docs/contracts/motor-desafios-evento-cierre.md`, `docs/contexto.md` y `docs/contracts/bus-notificaciones.md` reflejan el contrato nuevo.
- Se confirma a G09 en el issue #120 y se prueba un cierre de punta a punta.

**Fuera de alcance:** retirar el listener del topic anterior `challenges.results`.

## Tareas

- [x] #7049 T-11.1 Leer el producer nuevo y el payload en camelCase en el listener del cierre · Closed · Iker Alonso
- [x] #7050 T-11.2 Tests de contrato del evento de cierre con los ejemplos de G09 · Closed · Iker Alonso
- [x] #7051 T-11.3 Actualizar los contratos en docs, confirmar a G09 y probar un cierre de punta a punta · Closed · Iker Alonso
