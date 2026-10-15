# T-02.2: Guion de Sprint Review

> Cubre lo mergeado en `develop` (back y front) de Roadmap, confirmado como el alcance oficial
> del sprint: HU-01 (grafo), HU-06 (lectura obligatoria), HU-13 (reglas AND/OR), HU-15 / T-15.x
> (vidas y política de vidas). Necesita un curso `10000000-0000-4000-8000-000000000001` con
> 12 alumnos y su historial de intentos ya cargado: la semilla `demo` (`DemoDataSeeder`) que lo
> creaba se eliminó en HT-09, así que hoy ese fixture tiene que venir del flujo real de
> Courses/Users. Objetivo: recorrerlo en menos de 10 minutos, sin ayuda (CA2). **Bloqueador real,
> no cosmético:** el paso 3 de "Antes de arrancar" no se puede completar todavía — Users no tiene
> las 13 cuentas con los UUIDs fijos que este guion necesita (detalle ahí mismo).

## Antes de arrancar (una sola vez, no cuenta en los 10 minutos)

1. Levantar `tpi-roadmap` con el curso del fixture ya cargado: la semilla `demo` que lo creaba
   se eliminó en HT-09, así que el curso, los 12 alumnos y el grafo tienen que venir del flujo
   real de Courses/Users.
2. Confirmar que `roadmap-service` está en el allowlist del Gateway (`GATEWAY_ALLOWLIST`) y
   registrado en Eureka (`GET /eureka/apps/ROADMAP-SERVICE` → `UP`).
3. Conseguir tres tokens reales vía Users/Identidad, con el login real (2 fases, `AuthController`
   de `tpi-users`), uno para el profesor y uno para cada uno de los alumnos `...0001` y `...0002`
   (el alumno `...0012` no hace falta con token propio: el profesor puede consultar el
   progreso de cualquiera):
   ```bash
   # Fase 1: credenciales -> challengeId (dispara el 2FA por mail, no da tokens)
   curl -s -X POST -H "Content-Type: application/json" \
     -d '{"email":"<email>","password":"<password>"}' \
     "$GATEWAY_URL/api/users/public/auth/login"

   # El código de 6 dígitos NO tiene endpoint para leerlo (el "inbox de desarrollo /dev/"
   # que menciona el Javadoc de AuthController es aspiracional, no existe implementado):
   # leerlo directo de la tabla outbox_event de Users (MySQL, no Postgres):
   #   SELECT JSON_UNQUOTE(JSON_EXTRACT(payload, '$.payload.code'))
   #   FROM outbox_event
   #   WHERE event_type = 'TWO-FACTOR-EMAIL-PREPARED'
   #     AND JSON_UNQUOTE(JSON_EXTRACT(payload, '$.payload.to')) = '<email>'
   #   ORDER BY created_at DESC LIMIT 1;

   # Fase 2: challengeId + código -> tokens (cookies + body)
   curl -s -X POST -H "Content-Type: application/json" \
     -d '{"challengeId":"<de la fase 1>","code":"<leído de outbox_event>"}' \
     "$GATEWAY_URL/api/users/public/auth/2fa/verify"
   ```
   **Hueco real, no cosmético:** no hay ningún usuario en `tpi-users` con los UUIDs fijos del
   fixture de Roadmap (`30000000-0000-4000-8000-000000000001`..`012`, el profesor).
   `AdminBootstrap` es RF-USR-01 real (contraseña aleatoria, para el primer admin de una
   instalación limpia), no un sembrador de cuentas de prueba. Sin esas 13 cuentas creadas del lado
   de Users con esos mismos ids, este paso no se puede completar hoy tal como está. Esto falta
   coordinarlo con el equipo de Users.
4. Definir `$GATEWAY_URL` (base del Gateway real) y exportar los tokens:
   ```bash
   export GATEWAY_URL="https://<gateway-real>"
   export TOKEN_PROFESOR="<JWT del profesor>"
   export TOKEN_ALUMNO_01="<JWT del alumno 30000000-0000-4000-8000-000000000001>"
   export TOKEN_ALUMNO_02="<JWT del alumno 30000000-0000-4000-8000-000000000002>"
   export COURSE=10000000-0000-4000-8000-000000000001
   ```

## Cronómetro (~9 minutos)

### 1. HU-01 — El profesor ya tiene el grafo armado (1 min)

```bash
curl -s -H "Authorization: Bearer $TOKEN_PROFESOR" \
  "$GATEWAY_URL/api/roadmap/courses/$COURSE" | jq
```

Mostrar: 3 unidades ("Introducción", "Programación orientada a objetos", "Colecciones y
persistencia"), 11 nodos de tipo `UNIT`/`CONTENT`/`THEORETICAL_CHALLENGE`/`PRACTICAL_CHALLENGE`,
cada uno con su `challengeId`, `livesPolicy` y `prerequisiteNodeIds`. Anotar de esta respuesta
el `id` de "Variables y tipos" (desafío 1) y "Modelado de dominio" (desafío 7) para los pasos
siguientes — no son fijos, los genera la base al sembrar.

### 2. HU-13 — Reglas de desbloqueo AND/OR (2 min)

El fixture ya dejó cargado: desafío 5 exige 1 **y** 2 (AND); desafío 7 exige 5 **y** 6 (AND);
desafío 9 exige 7 **o** 8 (OR). Mostrarlo leyendo las reglas del desafío 9:

```bash
curl -s -H "Authorization: Bearer $TOKEN_PROFESOR" \
  "$GATEWAY_URL/api/roadmap/nodes/<id-desafio-9>/rules" | jq
# { "data": { "mode": "OR", "prerequisiteNodeIds": ["<id-7>", "<id-8>"] }, "success": true, ... }
```

Editarla en vivo (agregar un tercer prerrequisito) y confirmar que el `GET` de arriba lo refleja:

```bash
curl -s -X PATCH -H "Authorization: Bearer $TOKEN_PROFESOR" -H "Content-Type: application/json" \
  -d '{"mode":"OR","prerequisiteNodeIds":["<id-7>","<id-8>","<id-1>"]}' \
  "$GATEWAY_URL/api/roadmap/nodes/<id-desafio-9>/rules"
```

### 3. HU-06 — Lectura obligatoria desbloquea el desafío (2 min)

Alumno 01 (`...0001`, sin intentos todavía en el fixture): el desafío 1 exige haber leído
"Material de lectura" primero.

```bash
# Antes de leer: 403 (o el desafío no aparece habilitado en el progreso, ver paso 5)
curl -s -X POST -H "Authorization: Bearer $TOKEN_ALUMNO_01" \
  "$GATEWAY_URL/api/roadmap/courses/$COURSE/nodes/<id-desafio-1>/start"

# Marca el contenido como leído (idempotente, HU-06 CA2)
curl -s -X POST -H "Authorization: Bearer $TOKEN_ALUMNO_01" \
  "$GATEWAY_URL/api/roadmap/nodes/<id-material-lectura>/read" | jq

# Ahora sí arranca
curl -s -X POST -H "Authorization: Bearer $TOKEN_ALUMNO_01" \
  "$GATEWAY_URL/api/roadmap/courses/$COURSE/nodes/<id-desafio-1>/start" | jq
```

### 4. HU-15 / T-15.x — Vidas y política de vidas (2 min)

Alumno 02 (`...0002`, guion `"1 !2 !2 !2"`): perdió sus 3 vidas iniciales fallando el desafío 2
tres veces. Mostrar el gate bloqueando por `no_lives`:

```bash
curl -s -H "Authorization: Bearer $TOKEN_ALUMNO_02" \
  "$GATEWAY_URL/api/roadmap/courses/$COURSE/students/30000000-0000-4000-8000-000000000002/nodes/<id-desafio-2>/eligibility" | jq
# { "data": { "eligible": false, "reason": "no_lives" }, "success": true, ... }
```

Mostrar que el desafío de recuperación de vida (el 4, "Recuperación de vida",
`livesPolicy: RECOVERY`) lo exime igual sin vidas:

```bash
curl -s -H "Authorization: Bearer $TOKEN_ALUMNO_02" \
  "$GATEWAY_URL/api/roadmap/courses/$COURSE/students/30000000-0000-4000-8000-000000000002/nodes/<id-recuperacion>/eligibility" | jq
# { "data": { "eligible": true, "reason": null }, "success": true, ... }
```

### 5. Progreso general del alumno (1.5 min)

Alumno 12 (`...0012`, hizo todos los desafíos): ver su progreso consolidado — XP, vidas
vigentes y estado (`locked`/`enabled`/`completed`) de cada nodo del roadmap.

```bash
curl -s -H "Authorization: Bearer $TOKEN_PROFESOR" \
  "$GATEWAY_URL/api/roadmap/courses/$COURSE/students/30000000-0000-4000-8000-000000000012/progress" | jq
```

Contrastarlo con el alumno 01 (sin intentos): la mayoría de los nodos en `locked`, solo el
primero `enabled`.

## Qué NO entra en este guion (para dejarlo en <10 min)

- Resultado del motor vía Kafka (`ChallengeResultBddSteps`/T-03.x): el fixture ya insertó los
  resultados directo por `ProgressService.recordResult`, no se dispara un evento en vivo acá.
- Ranking (Tema 10, todavía no tiene endpoint propio en este back).
- CRUD del grafo desde cero (crear secciones/nodos): ya se ve de sobra con el `GET` del paso 1;
  si el tiempo sobra, es la primera candidata a agregar.

## Pendiente para que esto corra de punta a punta

- **Bloqueador real (no de esta tarea):** crear en `tpi-users` las 13 cuentas
  (profesor + 12 alumnos) con los UUIDs fijos que usa el fixture de Roadmap
  (`30000000-0000-4000-8000-000000000001`..`012`). Verificado: no existen hoy (`AdminBootstrap`
  es RF-USR-01 real, para el primer admin, no un sembrador de cuentas de prueba). Sin esto, el
  login real del paso 3 no tiene con qué autenticar a esos ids concretos.
  Login y 2FA en sí **sí están confirmados y andan** (`AuthController` de `tpi-users`,
  develop); lo único manual es leer el código de la tabla `outbox_event` (no hay endpoint,
  el "inbox /dev/" del Javadoc no está implementado).
- Confirmar `$GATEWAY_URL` del entorno de la review.
- Confirmar que el Gateway ya tiene `roadmap-service` en su allowlist (`GATEWAY_ALLOWLIST`) —
  en `main` de `tpi-api-gateway` el default sigue siendo solo `users-service`; se pisa por env
  var en el deploy, no por código, así que hay que confirmarlo en el entorno de la review, no
  acá.
