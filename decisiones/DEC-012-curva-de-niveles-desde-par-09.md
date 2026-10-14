---
tags: [tpi, g10, decision, par, niveles, backoffice]
fecha: 2026-09-24
estado: aceptada
reemplaza: ""
---

# DEC-012: La curva de niveles viene de Backoffice (PAR-09), no de constantes

## Contexto
Los parámetros globales (PAR-xx) los posee Backoffice y solo rigen hacia adelante. El nivel del alumno depende de su `total_xp` y de una curva configurable, que además usan las insignias (`LEVEL_REACHED`).

## Decisión
Roadmap pide los PAR a Backoffice por REST (`GET /api/backoffice/parameters`), los cachea (TTL 5 min, máx 50) y los invalida con `GLOBAL_CONFIGURATION_CHANGED`. El nivel se calcula en `LevelService` a partir del `total_xp` del ledger con la curva PAR-09 `[{level, xpRequired}]`, validada por el cliente: arranca en 0, estrictamente ascendente y niveles consecutivos. Desde `#177` admite hasta **200 niveles** y el mapa `level_N` se ordena por número (el contrato original decía 10). Se exponen `GET /students/{id}/level` y `/students/me/level`. Sin valores por defecto en código.

## Alternativas descartadas
- **Constantes de código**: los valores PAR no pueden estar en el código.
- **Claves propias de PAR-01** (`basic/medium/advanced`): se adoptaron las del contrato `easy/medium/hard`.
- **Consumir PAR-08 y PAR-13**: PAR-08 se descartó (ver [[decisiones/DEC-011-quitar-umbral-xp-seccion-v8|DEC-011]]); PAR-13 queda sin dueño ni lector.

## Consecuencias
- Positivas: el curso refleja la configuración vigente sin redeploy; sin el evento de invalidación, el nivel puede ir hasta 5 min desfasado.
- Negativas / deuda:
  - Dependencia de Backoffice: sin dato, el cliente lanza `ParUnavailableException`; `hasReachedLevel` devuelve `false` para no frenar el registro de XP.
  - `COURSE_LEVEL_UP` está en el catálogo pero **no se emite**.
  - `level-curve.ts` está duplicado en `accounting` y en `roadmap/mocks` (auditoría Sprint 3).
  - Backoffice aún debe confirmar el payload v8 del evento (`param_key` ya confirmado en 2.0.0).

## Referencias
- Código / PR / doc: `432c67b` (cliente PAR con caché y evento, 2026-09-24), `cc71f75` (`LevelService`, 2026-10-03), `5723659` (endpoint de nivel), `6399cf7` (200 niveles, PR #177, 2026-10-11), `clients/backoffice/*`, `events/ParRefreshListener`.
- `tpi-roadmap/docs/contracts/backoffice-par.md`, `docs/contracts/CONTRATO_T10_BACKOFFICE.md`.
- Relacionadas: [[acuerdos/backoffice|Backoffice]], [[decisiones/DEC-006-insignias-sistema-y-curso|DEC-006]].
