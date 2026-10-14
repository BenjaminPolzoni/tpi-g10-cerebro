---
tags: [tpi, g10, acuerdo, indice]
fecha: 2026-10-14
---

# Acuerdos con otros grupos y servicios

Índice de lo que G10 (Roadmap) intercambia con cada contraparte. Fuente: `tpi-roadmap/docs/contracts/` en `origin/develop` (tip `57ff06a`, 2026-10-14). Estructura de cada nota: [[plantillas/acuerdo]].

> [!info] Cómo leerlo
> - **Estado** sigue la plantilla: `propuesto`, `vigente`, `reemplazado`, `caido`.
> - "Gxx (verificar)" = el número de grupo no aparece en los docs.
> - Los contratos viven en el repo back: `tpi-roadmap/docs/contracts/` ([carpeta en GitHub](https://github.com/2026-P4-BE/tpi-roadmap/tree/develop/docs/contracts)).
> - Ninguna acta tiene **aprobación nominal** de ambos lados registrada (en `roadmap-events-v1.md` solo figura la fila de G10).

| Contraparte | Grupo | Qué intercambiamos | Estado | Nota |
|---|---|---|---|---|
| Courses and Enrollment | G01 | Cohortes, secciones, comisiones, participantes, restricciones y material (REST M2M); eventos de matrícula y archivado | vigente (acta T-10.1 sin firma formal) | [[acuerdos/courses-g01\|Courses]] |
| Motor de Desafíos | G09 | Evento de cierre de intento (`challenges.events`, v8); gate de elegibilidad v1.3; catálogo y pool de desafíos | vigente (gate sin firma nominal) | [[acuerdos/motor-desafios-g09\|Motor de desafíos]] |
| Accounting | Gxx (Tema 08, verificar) | Vidas, saldo, ítems, vidas perdidas (ranking); eventos `LIFE_*`, `LIVES_*`, `ITEM_EQUIP_*` | vigente (firma nominal pendiente) | [[acuerdos/accounting\|Accounting]] |
| Inventario | Gxx (verificar) | `equip-summary` para el Gate y la pantalla de inventario; 404 `ACCOUNT_NOT_FOUND` | vigente | [[acuerdos/inventario\|Inventario]] |
| Backoffice | G06 (Tema 12) | Parámetros PAR-01/09/12 (REST) y `GLOBAL_CONFIGURATION_CHANGED`; nosotros publicamos `roadmap.events` | vigente (payload v8 por confirmar) | [[acuerdos/backoffice\|Backoffice]] |
| Users / Identity | G07 (Tema 01) | Perfiles para el ranking del profesor; emisión del token técnico; roles | vigente | [[acuerdos/users\|Users]] |
| Notificaciones / bus | G02 | Envelope de 6 campos, topics por dominio, claves, DLT; `roadmap.events` | propuesto (borrador sin acta) | [[acuerdos/notificaciones-bus\|Notificaciones y bus]] |
| API Gateway, Eureka, Kafka | Gxx (Tema 01 y Tema 11, verificar) | Ruteo `/api/roadmap/**`, identidad propagada, tokens de servicio y scopes, broker | vigente | [[acuerdos/plataforma-gateway-kafka\|Plataforma]] |

## Contratos reemplazados (no usar como fuente)
| Contrato | Reemplazado por |
|---|---|
| `contrato-evento-motor-v2.md` (`ATTEMPT_CORRECTED`, camelCase, `THEME-02-CHALLENGE-ENGINE`) | `motor-desafios-evento-cierre.md` (v8 snake_case) |
| `motor-desafios.md` §1 y buena parte de §4 | `motor-desafios-evento-cierre.md`; el gate sigue en `roadmap-motor-gate-v1.md` |
| `respuesta-motor-a-roadmap-v2.md` §2 | `motor-desafios-evento-cierre.md` |
| `CONTRATO_T10_BACKOFFICE.md` (ruta `/api/administration`, headers `X-User-*`, 10 niveles) | `backoffice-par.md` |
| `KAFKA_EVENT_STANDARD (1).md` (camelCase) y `roadmap-service.asyncapi.yaml` (v3) | `contratos-kafka` v8 (ver [[decisiones/DEC-001-wire-kafka-v8-snake-case\|DEC-001]]) |
| `GET /api/bank/.../lives`, `/api/wallet/inventory/lives` | `accounting-roadmap-v1.md` |

## Pendientes transversales
> [!warning] Lo que más pesa
> 1. **HU-49** (restricciones `HIDDEN`/`LOCKED`, evento de cambio, aviso): bloqueada por G01.
> 2. **Flags apagados por defecto** (`SECTIONS_SYNC_ENABLED`, `ROADMAP_BY_GROUP_ENABLED`): funcionalidad hecha que no se ve en la demo. Ver [[decisiones/DEC-004-flags-apagados-por-defecto|DEC-004]].
> 3. **Rama `fix/account-not-found-gate`** sin mergear frente al PR #193 ya en develop: ver [[acuerdos/inventario|Inventario]].
> 4. Confirmar con Gamificación, Accounting y Notificaciones que consumen `roadmap.events` en v8.
> 5. Firmas nominales de las actas (Accounting, Motor, Courses T-10.1).

Decisiones técnicas relacionadas: [[decisiones/README|índice de decisiones]].
