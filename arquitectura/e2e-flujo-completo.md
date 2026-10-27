# E2E del flujo completo (caja negra por Gateway)

Harness de prueba punta a punta de Roadmap contra un **micro desplegado**. Es
caja negra: habla por el **Gateway** con `java.net.http.HttpClient`, publica
eventos con `KafkaProducer` (JSON plano) y no usa mocks de runtime ni levanta
contexto de Spring. Vive en `src/test/java/com/utn/tpi/roadmap/e2e/`.

Objetivo: recorrer y verificar el camino real de un alumno — autenticación con
2FA, armado del grafo por el editor, matrícula y cierre de intento por el bus,
y el reflejo en progreso, nivel y ranking — sin depender de las HU en curso.

## 1. Escenarios

| Clase | Tag | Qué hace |
|---|---|---|
| `FlujoCompletoE2ETest` | `e2e` | Flujo completo (escribe y publica eventos). |
| `SmokeE2ETest` | `smoke` | Smoke read-only: ping público, whoami, roadmap y ranking. |
| `InventoryIntegratedE2ETest` (T-09.6) | `e2e` | Inventario del alumno y Gate (solo lectura; el Gate servicio a servicio usa Bearer técnico). |
| `MarketPurchaseHudE2ETest` (T-40.5) | `e2e` | Compra un ítem en el Mercado y sondea el inventario del roadmap hasta que aparece. |

Los escenarios de inventario corren con el perfil `-Pe2e` (tag `e2e`) y se
saltan sin su entorno. La persona autentica con el harness (`E2EAuth` →
cookie `fu_at`, nunca Bearer): `E2E_STUDENT_COOKIE` o login
(`E2E_STUDENT_EMAIL` más `E2E_STUDENT_PASSWORD`, con `E2E_STUDENT_2FA_CODE` o
`E2E_MAILBOX_URL`).

`InventoryIntegratedE2ETest` (T-09.6) necesita además `E2E_COURSE_ID` (con
matrícula; `E2E_STUDENT_ID` es opcional si el whoami lo resuelve) y, para el
Gate, `E2E_NODE_ID` más `E2E_SERVICE_TOKEN` (Bearer técnico
`client_credentials`, servicio a servicio).

`MarketPurchaseHudE2ETest` (T-40.5) necesita además `E2E_COURSE_ID` con
matrícula y `E2E_MARKET_OFFER_ID` (oferta activa de ese curso con stock).

### Flujo de `FlujoCompletoE2ETest`

1. **whoami** de profesor y alumno (`GET /api/users/me`) y validación de rol.
2. **Editor**: `GET /api/roadmap/courses/{courseId}/challenge-pool?type=...` →
   `POST /api/roadmap/courses/{courseId}/sections` →
   `POST /api/roadmap/sections/{sectionId}/nodes` (nodo `PRACTICAL_CHALLENGE`
   con el `challenge_id` elegido del pool).
3. **Matrícula**: publica `STUDENT_ENROLLED` en `courses.events` (envelope de 6
   campos snake_case, `event_version=1`, payload `{course_cohort_id, student_id}`).
4. **Cierre de intento v3**: publica `CHALLENGE_COMPLETED` en
   `challenges.events` con `producer=tema-03-challenges-service`,
   `resources.xp` y `result.status=APPROVED` (contrato
   `docs/contracts/motor-desafios-evento-cierre.md`).
5. **Verificación**: sondea
   `GET /api/roadmap/courses/{courseId}/students/{studentId}/progress` hasta que
   el nodo quede `completed` y el XP sume; y contrasta
   `GET .../students/me/level` y `GET /api/roadmap/courses/{courseId}/ranking`.

## 2. Cómo se ejecuta

Por defecto el tag `e2e` está **excluido** (`maven-surefire-plugin`,
`excludedGroups=e2e`), así que `test` y `verify` no lo ejecutan. El perfil
`e2e` levanta la exclusión y restringe la corrida al paquete `.../e2e/`.

```sh
# 1. Compila todo, incluido el harness (verde sin entorno).
./mvnw -q -B test-compile

# 2. Suite normal: NO ejecuta el e2e (el smoke corre y se salta sin entorno).
./mvnw -q -B test

# 3. Ejecuta el harness E2E. Sin E2E_* el escenario se SALTA (no falla).
./mvnw -B test -Pe2e

# 4. Corrida enfocada de un escenario.
./mvnw -B test -Pe2e -Dtest=FlujoCompletoE2ETest
./mvnw -B test -Dtest=SmokeE2ETest        # el smoke no necesita perfil
```

El harness **no depende de HU-47/HU-48 para compilar**: llama los endpoints por
HTTP y no importa sus clases. El endpoint `challenge-pool` (HU-47) debe estar
desplegado para que el paso 2 funcione; si el pool viniera vacío se usa
`E2E_CHALLENGE_ID`.

## 3. Contrato de entorno

Todo se inyecta por variables `E2E_*` (nunca en el repo). También se aceptan como
system property con el mismo nombre o en minúsculas con puntos
(`-DE2E_GATEWAY=...` o `-De2e.gateway=...`), que tienen prioridad. Si falta un
valor obligatorio el escenario se **salta** con `Assumptions`.

Plantilla comentada: [`src/test/resources/e2e.properties.example`](../src/test/resources/e2e.properties.example).

| Variable | Obligatoria | Default | Uso |
|---|---|---|---|
| `E2E_GATEWAY` | sí (o `GATEWAY_URL`) | — | Base del Gateway. |
| `E2E_COURSE_ID` | sí | — | Cohorte (`courseCohortId`). |
| `E2E_KAFKA_BOOTSTRAP` | sí | — | Brokers de Kafka del micro desplegado. |
| `E2E_PROFESSOR_EMAIL` / `_PASSWORD` | sí* | — | Login 2FA del profesor. |
| `E2E_PROFESSOR_COOKIE` | — | — | Cookie `fu_at` directa; omite el login. |
| `E2E_PROFESSOR_2FA_CODE` | — | — | Código 2FA explícito (sin dev-mailbox). |
| `E2E_STUDENT_EMAIL` / `_PASSWORD` | sí* | — | Login 2FA del alumno. |
| `E2E_STUDENT_COOKIE` | — | — | Cookie `fu_at` directa; omite el login. |
| `E2E_STUDENT_2FA_CODE` | — | — | Código 2FA explícito. |
| `E2E_STUDENT_ID` | — | whoami | Alumno; si falta se resuelve por whoami. |
| `E2E_NODE_ID` | sí (Gate) | — | Nodo del Gate de elegibilidad (T-09.6). |
| `E2E_SERVICE_TOKEN` | sí (Gate) | — | Bearer técnico servicio a servicio (T-09.6). |
| `E2E_MARKET_OFFER_ID` | sí (T-40.5) | — | Oferta activa con stock (T-40.5). |
| `E2E_MAILBOX_URL` | — | — | Dev-mailbox del código 2FA (ver §4). |
| `E2E_CHALLENGE_POOL_TYPE` | — | `PRACTICAL` | Query `?type=` del pool. |
| `E2E_CHALLENGE_ID` | — | — | Fallback si el pool viene vacío. |
| `E2E_XP` | — | `250` | XP que otorga el intento publicado. |
| `E2E_COURSES_TOPIC` | — | `courses.events` | Topic de matrícula. |
| `E2E_CHALLENGES_TOPIC` | — | `challenges.events` | Topic de cierre de intento. |
| `E2E_COURSES_PRODUCER` | — | `tema-02-courses-service` | Producer de `STUDENT_ENROLLED`. |
| `E2E_CHALLENGES_PRODUCER` | — | `tema-03-challenges-service` | Producer que filtra el listener. |
| `E2E_SERVICE_CLIENT_ID` / `_SECRET` | — | — | Reservado para pasos M2M futuros. |

\* Si se define la cookie del rol, no hacen falta email/password.

### Login + 2FA

`POST /api/users/public/auth/login` → se lee el **código de 6 dígitos** de
`E2E_MAILBOX_URL` (o de `E2E_<ROL>_2FA_CODE`) → `POST /api/users/public/auth/2fa/verify`
→ se captura la cookie `fu_at` de los `Set-Cookie`. Si no hay mailbox ni código,
se usa `E2E_<ROL>_COOKIE`; si tampoco hay, el escenario se salta. Hoy Users **no
expone** el dev-mailbox (el "inbox /dev/" del Javadoc no está implementado), por
eso el fallback por cookie es el camino recomendado en entornos reales.

## 4. Seguridad

- **Sin secretos en el repo:** credenciales, cookies y bootstrap se pasan por
  entorno; la plantilla solo documenta los nombres.
- **Sin mocks de runtime:** el harness no sustituye clientes ni servicios; solo
  salta cuando falta entorno.
- **Excluido de `verify`:** el tag `e2e` no se ejecuta en el ciclo normal.

## 5. Limitaciones

- Requiere un entorno integrado real (Gateway + Users + Courses + Motor/Kafka)
  con un profesor dueño de la cohorte y un alumno inscripto.
- El paso del pool depende del endpoint de HU-47 desplegado; sin él se usa
  `E2E_CHALLENGE_ID`.
- El sondeo espera hasta 90 s a que Kafka se refleje en el progreso.
- Un roadmap vacío o un alumno sin matrícula hacen fallar el smoke (no es un
  problema del harness sino del entorno).
