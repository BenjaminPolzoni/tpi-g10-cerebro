# Microservicio: Engine Challenge Service (`tpi-engine-challenge`)

> **Ficha Técnica Canónica y Contrato de Integración**  
> Tema: **Tema 09 — Motor de Desafíos y Evaluación de Intentos**  
> Equipo Responsable: **Grupo 09 (G09)**  
> Repositorio: `2026-P4-BE/tpi-engine-challenge` (Local: `D:\Dev\IdeaProjects\Progra4\tpi-engine-challenge`)  
> Estado: **Vigente (v2.0.0)**

---

## 1. Identidad y Red

| Parámetro | Valor |
|---|---|
| **Nombre de Aplicación (Eureka)** | `engine-challenge-service` |
| **Prefijo en API Gateway** | `/api/engine-challenge/**` (preservado sin rewrite) |
| **Puerto por Defecto** | `8086` |
| **Puerto de Gestión (Management/Actuator)** | `8087` (`management.server.port`) |
| **Rutas Públicas** | `${app.api.public-path}/**` (`/api/engine-challenge/public/**`) |
| **Rutas Privadas** | `${app.api.private-path}/**` (`/api/engine-challenge/**`) |
| **Rutas de Corrección Interna** | `/api/intentos/**` (comunicación directa HMAC fail-closed entre correctores y motor, fuera de Gateway) |
| **Audience M2M** | `engine-challenge-service` |

---

## 2. Dominio y Responsabilidades

### Qué Hace Engine Challenge Service (Fuente de Verdad)
- **Coordinación de Intentos:** Creación, temporización, estado (`INITIALIZED`, `IN_PROGRESS`, `FINALIZED`, `ABORTED`, `CORRECTED`) y cierre de intentos.
- **Cálculo de Recursos y Gamificación:**
  - **El Motor es el único responsable de calcular:**
    - `coins`: Monedas ganadas en base a aciertos y rendimiento.
    - `xp`: Puntos de experiencia (XP base de Backoffice `PAR-01` + multiplicadores por tiempo/bonus).
    - `add_live` / `subtract_live`: Vidas a acreditar o debitar (ejecutado aguas abajo por Accounting).
    - `active_item`: Ítems consumibles aplicados en el intento.
- **Congelamiento de Parámetros:** Al iniciar el intento, congela los parámetros vigentes de Backoffice (`PAR-01`, `PAR-12`) para que modificaciones posteriores no alteren la liquidación.
- **Orquestación de Correctores:** Delega la ejecución a `practical-challenge-service` (Docker) o `theoretical-challenge-service` (evaluación teórica).

### Qué NO Hace Engine Challenge Service
- **NO calcula elegibilidad ni evalúa el árbol:** Llama al Gate de Roadmap de forma previa y obligatoria.
- **NO persiste el ledger acumulado de XP del alumno:** Emite el evento de cierre y delega en Roadmap el guardado append-only.
- **NO administra el saldo de vidas ni el inventario:** Se comunica con Accounting mediante reservas (`holds`).

---

## 3. Acuerdos Clave con Roadmap (Grupo 10)

### 3.1 Roadmap NO Calcula XP (DEC-013)
- **Acuerdo Histórico y Vigente:** Roadmap recibe el valor final de XP calculado por el Motor y lo registra como un movimiento atómico en su tabla `xp_movement`. Roadmap jamás replica la lógica de cálculo ni los multiplicadores del Motor.

### 3.2 Gate de Elegibilidad Síncrono (Pull)
- Antes de crear cualquier intento (`ATTEMPT_INIT`), el Motor llama de forma síncrona a Roadmap:  
  `GET /api/roadmap/courses/{courseId}/students/{studentId}/nodes/{nodeId}/eligibility`
- Si la respuesta es `eligible=false`, el Motor **aborta inmediatamente** la inicialización y retorna el motivo al usuario (ej. `no_lives`, `prerequisites_not_met`, `previous_readings_pending`).
- Una vez validado `eligible=true`, Roadmap termina su participación previa y el Motor continúa con Accounting para reservar vidas/ítems.

### 3.3 Consumo de Eventos de Cierre
- El Motor publica **un único evento por intento cerrado** a `challenges.events`:
  - `CHALLENGE_COMPLETED`: Intento finalizado y corregido con éxito. Mueve recursos (XP y monedas).
  - `CHALLENGE_ABORTED`: Intento cancelado o expirado. **Nunca mueve recursos** (XP = 0).

---

## 4. Contrato REST del Gate de Elegibilidad (Expuesto por Roadmap para Motor)

### Endpoint del Gate
- **Método y URL:** `GET /api/roadmap/courses/{courseId}/students/{studentId}/nodes/{nodeId}/eligibility`
- **Scope Requerido por Motor:** `roadmap.gate.read`
- **Headers:**  
  `Authorization: Bearer <m2m_token>`  
  `X-Service-Id: engine-challenge-service`

### Respuesta Exitosa: Alumno Elegible (200 OK)
```json
{
  "eligible": true,
  "node_id": "8a31e809-5c4a-472e-836b-d3ebbbef6920",
  "student_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "course_id": "e2a1b3c4-d5e6-7f8a-9b0c-1d2e3f4a5b6c",
  "reasons": []
}
```

### Respuesta Exitosa: Alumno No Elegible (200 OK)
```json
{
  "eligible": false,
  "node_id": "8a31e809-5c4a-472e-836b-d3ebbbef6920",
  "student_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "course_id": "e2a1b3c4-d5e6-7f8a-9b0c-1d2e3f4a5b6c",
  "reasons": [
    "no_lives",
    "prerequisites_not_met"
  ]
}
```

---

## 5. Eventos Kafka Producidos por Motor

- **Tópico:** `challenges.events`
- **Producer:** `engine-challenge-service`
- **Clave del Mensaje (`Key`):** `id_user` (alumno)
- **Envelope Oficial (5 Campos, snake_case v8):**

### Schema de `CHALLENGE_COMPLETED`:
```json
{
  "event_id": "e7b049ae-4c6e-44db-bb92-95f51950e304",
  "event_type": "CHALLENGE_COMPLETED",
  "timestamp": "2026-10-15T09:15:30.123Z",
  "producer": "engine-challenge-service",
  "payload": {
    "attempt_id": "76d41829-1954-46c5-a0bc-6ec5fb25ce1a",
    "challenge_id": "b0a2f647-7592-4f35-b28f-7f78c93a02bb",
    "node_id": "8a31e809-5c4a-472e-836b-d3ebbbef6920",
    "student_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
    "course_id": "e2a1b3c4-d5e6-7f8a-9b0c-1d2e3f4a5b6c",
    "resources": {
      "xp": 250,
      "coins": 50,
      "add_live": 0,
      "subtract_live": 0
    },
    "score": 100.0,
    "duration_seconds": 185,
    "completed_at": "2026-10-15T09:15:28.000Z"
  }
}
```

### Idempotencia en Roadmap:
- Roadmap almacena `event_id` en `xp_movement` con restricción de unicidad (`UNIQUE INDEX uk_xp_movement_event_id`). Si el evento se reentrega, Roadmap descarta el duplicado sin modificar el saldo acumulado.

---

## 6. Seguridad y Scopes M2M

| Scope | Origen | Destino | Propósito |
|---|---|---|---|
| `roadmap.gate.read` | `engine-challenge-service` | `roadmap-service` | Consultar la elegibilidad previa del alumno. |
| `accounting.reservation.write` | `engine-challenge-service` | `accounting-service` | Crear hold de vidas o ítems para el intento. |
| `course.enrollment.read` | `engine-challenge-service` | `course-service` | Verificación complementaria de cursado. |
| `backoffice.parameters.read` | `engine-challenge-service` | `backoffice-service` | Obtención de parámetros PAR-01 y PAR-12. |
