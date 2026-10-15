# T-15.6 — BDD y carga del Gate

## Alcance ejecutable

La suite `GateEligibilityBddSuiteTest` ejecuta cinco escenarios Gherkin contra el stack HTTP de
Spring, seguridad, servicios y H2 con migraciones reales:

1. alumno habilitado, repetición idempotente del GET y ausencia de escrituras;
2. alumno sin matrícula → `not_enrolled`;
3. curso archivado → `course_archived`;
4. precedencia `content_not_read` → `prerequisite_pending` al registrar la lectura;
5. cero vidas libres → `no_lives` en `STANDARD`, `RECOVERY` habilitado y caída de Accounting →
   HTTP 503 Problem Details sin respuesta funcional del Gate.

La idempotencia compara antes y después las filas de `student_course`, `content_reading`,
`completed_node`, `node_unlock` y `xp_movement`. El GET no crea intentos ni modifica progreso.

## Carga

`performance/k6/gate-eligibility.js` usa 120 usuarios virtuales constantes sobre HTTP real. El
criterio no negociable es `http_req_duration: p(95)<200`; cualquier request HTTP fallida también
hace fallar la ejecución. Un warm-up llena la caché de vidas antes de comenzar la medición.

La preparación y las limitaciones están documentadas en `performance/README.md`.

### Evidencia local del 26-09-2026

- k6 `v2.3.0`, Windows, Java 21;
- 120 VUs constantes durante 30 segundos;
- 119.342 requests HTTP totales, incluyendo preparación y warm-up;
- 119.340 iteraciones completas, ninguna interrumpida;
- P95 HTTP: **98,9 ms**;
- requests fallidas: **0 de 119.342 (0,00 %)**;
- checks: **358.023 de 358.023 exitosos**;
- thresholds `p(95)<200` y `rate==0`: **cumplidos**.

El resultado crudo se generó en `target/k6-gate-summary.json`, artefacto local no versionado. Se
debe regenerar en cada entorno cuya capacidad se quiera evaluar.

## Límites contractuales

- T-15.5 cerró el vocabulario de Sprint 1 con cinco razones. Los dos valores propuestos que no
  tenían semántica contractual quedaron retirados; T-15.6 conserva la prueba de recuperación
  vigente sin inventar una razón adicional.
- El resultado local no certifica el P95 del circuito integrado con Gateway, Accounting,
  PostgreSQL y red. Repetir allí requiere el token técnico y credenciales provistos por
  Gateway/Users.
