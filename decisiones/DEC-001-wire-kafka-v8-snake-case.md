---
tags: [tpi, g10, decision, kafka, contratos]
fecha: 2026-10-12
estado: aceptada
reemplaza: ""
---

# DEC-001: Wire Kafka y HTTP en snake_case (contratos-kafka v8), sin alias

## Contexto
Roadmap leía el sobre y los payloads con alias camelCase y snake_case a la vez (`@JsonAlias`, HU3-T03.2 D-HU3-05) porque cada productor usaba un casing distinto: Motor en snake_case, Notificaciones en camelCase, Accounting en camelCase. `contratos-kafka` v8 fijó **un solo nombre por campo, en snake_case**. Courses, Backoffice y Motor ya publicaban v8 (verificado en sus repos para el PR #191).

## Decisión
Roadmap **escribe y lee solo snake_case** en el sobre (`event_id`, `event_type`, `event_version`, `timestamp`, `producer`, `payload`) y en los payloads, sin alias ni ventana de convivencia. Un mensaje camelCase va a la DLT sin reintentos. El contrato HTTP de Roadmap también pasó a snake_case, con `@JsonProperty` explícito en cada campo multi-palabra y **sin estrategia global de Jackson**, para no renombrar de rebote los payloads de Kafka y del outbox.

## Alternativas descartadas
- **Mantener alias camelCase + snake_case**: era el estado previo; esconde productores desalineados y duplica el contrato. Se retiró.
- **Estrategia global `SNAKE_CASE` de Jackson**: rompería los payloads de Kafka/outbox en el mismo deploy (comentario en `application.properties`; `9dee26e` tuvo que fijar a mano los nombres camelCase de Courses al probarla).
- **Ventana de convivencia v3/v8**: no la hay; el rollback exige drenar el outbox a la inversa.

## Consecuencias
- Positivas: contrato único, errores de casing visibles (DLT) en vez de silenciosos.
- Negativas / deuda:
  - `LIFE_CREDITED`/`LIFE_DEBITED` de Accounting siguen con payload camelCase: única excepción, leída con alias hasta `tpi-accounting#227`.
  - Las filas `PENDING` del outbox anteriores al corte quedan en camelCase: hay que drenarlas antes de desplegar (runbook en `T-191`).
  - Falta confirmar que Gamificación, Accounting y Notificaciones consumen `roadmap.events` en v8.
  - `roadmap-service.asyncapi.yaml`, `KAFKA_EVENT_STANDARD (1).md` y el texto de Taiga HT-11 siguen en camelCase/v3.
  - El listener legado v1/v2 quedó apagado pero no borrado.

## Referencias
- Código / PR / doc: PR #191 (`2171242`, `1c2e643`, `74e884f`, 2026-10-12); `ced4ba0` (REST a snake_case, 2026-10-05); `f936760` (`@JsonProperty` explícito, 2026-10-08).
- `tpi-roadmap/docs/T-191-KAFKA-V8-CUTOVER.md`, `docs/contracts/motor-desafios-evento-cierre.md`, `docs/contracts/backoffice-par.md`.
- Relacionadas: [[acuerdos/notificaciones-bus|bus de eventos]], [[acuerdos/motor-desafios-g09|Motor]], [[acuerdos/accounting|Accounting]], [[decisiones/DEC-002-outbox-transaccional-eventos-salientes|DEC-002]].
