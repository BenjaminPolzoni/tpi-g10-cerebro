# T-25.2 — Fuente de las vidas perdidas para el desempate del ranking

## Estado

**Implementada contra el contrato de Accounting. Falta verificarla contra el Accounting real.**

El ranking lee las vidas perdidas del lote de Accounting (acta
`docs/contracts/accounting-roadmap-v1.md` §3.5). Si Accounting no responde, el criterio queda
neutro y el dato viaja sin valor (`lost_lives: null`), nunca como cero.

## Por qué no se usa `student_course.lost_lives`

La tarea pedía usar esa columna "siempre que una auditoría del código confirme que el dato es
confiable". La auditoría (03/10/2026) concluyó que **no lo es**:

| Dónde | Qué hace con `lost_lives` |
|---|---|
| `ProgressService.recordResult` | **No lo toca.** Solo llama a `StudentCourse.addXp`; las vidas quedan intactas (D-HU3-01). Es el único camino por el que entra un resultado del Motor en producción. |
| `StudentCourse.applyResult` | Lo actualizaría, pero **nadie lo llama**. |
| `RoadmapEventListener` | No procesa `resources.add_live` ni `resources.subtract_live`: son de Accounting (`agent.md` §3.1b). |
| `CourseCohortSyncService` | Lo inicializa en 0 al crear la matrícula. |

En producción la columna vale siempre 0: ordenar por ella no desempata nada y mostrarla sería
informar un dato falso. Coincide con `agent.md` §3.1b: las columnas `lives` y `lost_lives` son un
"espejo en desuso" y "ninguna decisión de negocio puede leerlas como fuente".

## Fuente: Accounting, por lote

```http
GET /api/accounting/courses/{courseId}/accounts
```

```json
[
  { "studentId": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "totalLivesLost": 2, "neverLostALife": false }
]
```

Roadmap usa `studentId` y `totalLivesLost`. Es una sola llamada por curso, con caché corta.

## Cómo se comporta

| Situación | Orden | `stats.lost_lives` |
|---|---|---|
| Accounting responde y conoce al alumno | A igual XP e insignias, arriba quien perdió menos | El valor informado |
| Accounting responde, pero falta la cuenta de algún alumno de un grupo empatado (igual XP e insignias) | El criterio queda neutro **para ese grupo**: nadie gana el desempate por no tener dato. Los demás grupos se desempatan normal | El valor informado para quien lo tiene; `null` para quien no |
| Accounting no responde, rechaza la llamada o no hay token | Criterio neutro para toda la cohorte | `null` en todas las filas |
| La respuesta trae una cuenta sin alumno, sin vidas, con vidas negativas, o dos cuentas del mismo alumno | Se descarta el lote entero: criterio neutro | `null` en todas las filas |

`RankingTiebreakCriterion.LOST_LIVES` aparece en `stats.tiebreak` cuando ese criterio fue el que
separó a dos filas de igual XP.

### Un solo dato faltante apaga el criterio para todo su grupo

Es la consecuencia buscada de no dejar que el faltante gane ni pierda el desempate, y conviene
tenerla presente: **alcanza con un alumno sin cuenta en Accounting para que las vidas perdidas no
desempaten a nadie de su grupo** (los que comparten su XP y sus insignias), incluso entre dos
alumnos cuyos datos sí se conocen.

El caso donde más pesa es el inicio del curso o cualquier empate grande: 30 alumnos en 0 XP y
0 insignias, con una matrícula que todavía no tiene cuenta, dejan el criterio sin efecto para los
30. Ese grupo pasa al criterio siguiente (ejercicios superados). Los demás grupos de empate no se
ven afectados.

### `lost_lives` es un dato del alumno, no del orden

`stats.lost_lives` informa lo que dijo Accounting de ese alumno, haya ordenado o no. Cuando el
criterio queda neutro para un grupo, el valor de quien lo tiene viaja igual. Por eso puede verse
una fila con `lost_lives: 3` arriba de otra con `lost_lives: 0`: en ese caso `stats.tiebreak`
dice qué criterio las ordenó (por ejemplo `completed_exercises`) y nunca vale `lost_lives`.

Quien lea el campo tiene que tomarlo así:

- **Para explicar el orden:** mirar `tiebreak`, no comparar `lost_lives` entre filas.
- **Para "candidato a promoción" (RF-RNK-05):** `lost_lives` es el dato correcto, porque esa
  regla pregunta si el alumno perdió vidas, no cómo quedó ordenado. Con `null` no se puede
  afirmar que nunca perdió una.

## Dónde se consulta a Accounting y dónde no

- `RankingService.studentView` y `staffView` leen el lote de Accounting. Primero leen lo que viene
  por red (el lote y la curva de niveles) y después consultan la base dentro de una transacción de
  solo lectura (`RankingSnapshot`): el orden y los datos por fila salen de la misma foto, y la
  conexión no queda retenida mientras se espera a otro servicio.
- `RankingService.localRankingOf` no consulta a Accounting ni desempata por vidas perdidas. Lo usa
  `BadgeCriteriaChecks.inEliteZone` (insignia `ZONE_P90`), que corre dentro de
  `ProgressService.recordResult` con el lock de escritura del alumno tomado: ahí no se espera a
  un servicio externo. Consecuencia: en un empate de XP e insignias justo en el corte de P90, la
  insignia puede resolverse distinto de como se ve el ranking.
- No queda ningún método público que arme el ranking consultando a Accounting fuera de las vistas:
  así un llamador nuevo no puede meter la llamada de red dentro de una transacción con locks.

**Seguimiento pendiente:** la insignia `ZONE_P90` es permanente y el ranking se recalcula. Si la
insignia se otorga con el ranking local y después el visible ordena distinto por vidas perdidas, la
insignia queda. Hay que decidir con el PO si se acepta, o si `ZONE_P90` se evalúa fuera de la
transacción del resultado para poder usar el mismo ranking que se muestra.

## Configuración

`app.clients.lost-lives.*`: `base-url` (Gateway), `path`, `timeout`, `token.audience`,
`token.scope`, `cache.ttl`, `cache.failure-ttl` y `mode` (`http` por defecto; `stub` solo en tests). La audience y el scope salen
de las mismas variables que el resto de Accounting (`ACCOUNTING_TOKEN_AUDIENCE`,
`ACCOUNTING_TOKEN_SCOPE`), con los mismos defaults: `accounting-service` y
`accounting.account.read`.

El lote de cada curso se guarda `cache.ttl` (30 s por defecto), así que no hay una llamada a
Accounting por cada consulta del ranking. Si la lectura falla, el cliente lo avisa una vez en el
log y no reintenta hasta que pase `cache.failure-ttl` (30 s): con Accounting lento o caído, las
consultas siguientes degradan al instante en vez de esperar el timeout cada una. El mensaje del
log distingue la falta de token (configuración) de una respuesta de error de Accounting.

## Pendiente para cerrar la tarea

1. **Accounting (G12):** confirmar que el lote de §3.5 está implementado y que acepta el scope
   `accounting.account.read`, que es el que usa el resto del cliente.
2. **Formato de la respuesta:** auditoría (10/2026) de `tpi-accounting` `develop`: el endpoint
   expone el wire en snake_case (`student_id`, `total_lives_lost`, `never_lost_a_life`). El cliente
   usa snake_case como nombre primario y acepta camelCase como alias del acta v1 §3.5. Falta
   confirmar en el entorno integrado si la respuesta viene sin sobre, como en el acta.
3. Probar el ranking contra el Accounting real con dos alumnos empatados.
