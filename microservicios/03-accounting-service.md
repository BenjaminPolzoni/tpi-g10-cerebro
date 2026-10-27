# Microservicio: Accounting & Inventory Service (`tpi-accounting`)

> **Ficha Técnica Canónica y Contrato de Integración**  
> Tema: **Tema 08 — Contabilidad, Vidas, Monedas e Inventario de Ítems**  
> Equipo Responsable: **Tema 08 (Gxx)**  
> Repositorio: `2026-P4-BE/tpi-accounting` (Local: `D:\Dev\IdeaProjects\Progra4\tpi-accounting`)  
> Estado: **Vigente (v2.0.0)**

---

## 1. Identidad y Red

| Parámetro | Valor |
|---|---|
| **Nombre de Aplicación (Eureka)** | `accounting-service` |
| **Prefijo en API Gateway** | `/api/accounting/**` |
| **Puerto por Defecto** | `8084` |
| **Puerto de Gestión (Management/Actuator)** | `8085` (`management.server.port`) |
| **Rutas Públicas** | `${app.api.public-path}/**` (`/api/accounting/public/**`) |
| **Rutas Privadas** | `${app.api.private-path}/**` (`/api/accounting/**`) |
| **Base de Datos** | PostgreSQL (migraciones Flyway `db/migration`) |
| **Audience M2M** | `accounting-service` |

---

## 2. Dominio y Responsabilidades

### Qué Hace Accounting Service (Fuente de Verdad Única)
- **Cuentas de Alumno:** Apertura, ciclo de vida y balance de cuentas por alumno y cohorte.
- **Gestión de Vidas:** Saldo de vidas disponibles, vidas reservadas (`reservedLives`), historial de débitos y créditos, y aplicación del tope máximo de vidas según `PAR-12`.
- **Saldo de Monedas:** Balance de monedas obtenidas en desafíos o compras en el marketplace.
- **Reservas y Holds:** Bloqueo temporal de recursos al iniciar un desafío (`holds`) para evitar sobreconsumos concurrentes.
- **Inventario y Equipamiento de Ítems:** Posesión de ítems cosméticos o consumibles, equipamiento activo y estado de inventario del estudiante.

### Qué NO Hace Accounting Service
- **NO evalúa la elegibilidad del estudiante en el Roadmap:** Accounting informa si el alumno tiene vidas libres (`freeLives > 0`); la decisión final de admisión al desafío la toma Roadmap en su Gate.
- **NO calcula ni almacena el XP del alumno:** El XP es administrado exclusivamente por Roadmap (`xp_movement`).

---

## 3. Acuerdos y Decisiones de Integración con Roadmap

### 3.1 Consolidación de "Inventario" y "Accounting"
- En la arquitectura, **el inventario de ítems y la contabilidad de vidas residen en el mismo microservicio** (`accounting-service`).
- Roadmap interactúa mediante un único cliente técnico (`InventoryClient`), que invoca `/api/accounting/...`.

### 3.2 Cálculo de Vidas Libres en el Gate de Elegibilidad
- El Gate de Roadmap calcula las vidas disponibles según la fórmula:
  $$\text{freeLives} = \text{currentLives} - \text{reservedLives}$$
- **Regla de Bloqueo:** Solo se bloquea con el motivo `no_lives` si el nodo es de tipo `STANDARD` y $\text{freeLives} \le 0$.
- **Excepción de Recuperación:** Los nodos de tipo `RECOVERY` (recuperación de vidas) y `LLM` **no consultan vidas**. De esta forma, un alumno sin vidas puede jugar desafíos de recuperación, y una caída de Accounting no bloquea la recuperación.

### 3.3 Pantalla de Inventario del Estudiante (HU-35)
- Roadmap expone el endpoint BFF `GET /api/roadmap/courses/{courseId}/inventory` para la UI del alumno (`STUDENT`).
- Internamente Roadmap delega en `GET /api/accounting/courses/{courseId}/students/{studentId}/equip-summary`.
- **Resiliencia ante caídas:** Si Accounting no está disponible, la pantalla responde el último estado conocido en caché local con el flag `stale: true` (retención de hasta 24 horas). En contraste, el Gate **nunca** utiliza datos desactualizados (falla cerrado).
- **Cuenta ausente:** Si Accounting devuelve `404 ACCOUNT_NOT_FOUND`, Roadmap propaga un Problem Details `404 inventory.account-not-found` sin asumir que tiene 0 vidas ni abrir el desafío.

### 3.4 Desempate en Ranking por Vidas Perdidas (`RF-RNK-11`)
- En el cálculo de ranking dinámico, si dos o más estudiantes empatan en XP e insignias, el 2° criterio de desempate es la **menor cantidad de vidas perdidas históricamente**.
- Roadmap consulta esta métrica a Accounting en una única llamada por lote (`batch/lives-lost`).

---

## 4. Endpoints REST Consumidos por Roadmap

Todas las llamadas se enrutan por el API Gateway (`${app.gateway.url}/api/accounting/...`) con token técnico M2M.

### 4.1 Resumen de Equipamiento y Vidas (`equip-summary`)
Trae vidas, saldo de monedas e ítems equipados en una sola llamada por alumno:
- **Método y URL:** `GET /api/accounting/courses/{courseId}/students/{studentId}/equip-summary`
- **Scope Requerido:** `accounting.equipment.read`
- **Respuesta Exitosa (200 OK):**
```json
{
  "student_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "course_id": "e2a1b3c4-d5e6-7f8a-9b0c-1d2e3f4a5b6c",
  "lives": {
    "current": 3,
    "reserved": 1,
    "free": 2,
    "max": 5
  },
  "coins": {
    "balance": 350
  },
  "equipped_items": [
    {
      "item_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "slot": "AVATAR_HAT",
      "name": "Gorra de Graduado",
      "asset_url": "https://storage.utn.edu.ar/items/hat_grad.glb"
    }
  ]
}
```

### 4.2 Disponibilidad Rápida de Vidas (`lives-availability`)
- **Método y URL:** `GET /api/accounting/courses/{courseId}/students/{studentId}/lives-availability`
- **Scope Requerido:** `accounting.lives.read`
- **Respuesta Exitosa (200 OK):**
```json
{
  "student_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "current_lives": 3,
  "reserved_lives": 0,
  "free_lives": 3,
  "has_free_lives": true
}
```

### 4.3 Consulta en Lote de Vidas Perdidas para Ranking (`batch/lives-lost`)
- **Método y URL:** `POST /api/accounting/courses/{courseId}/students/batch/lives-lost`
- **Scope Requerido:** `accounting.lives.read`
- **Body:**
```json
{
  "student_ids": [
    "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
    "c8a1b2c3-d4e5-6f7a-8b9c-0d1e2f3a4b5c"
  ]
}
```
- **Respuesta Exitosa (200 OK):**
```json
{
  "lives_lost": {
    "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d": 4,
    "c8a1b2c3-d4e5-6f7a-8b9c-0d1e2f3a4b5c": 1
  }
}
```

---

## 5. Eventos Kafka

- **Tópico:** `accounting.events`
- **Producer:** `accounting-service`
- **Clave del Mensaje (`Key`):** `student_id`

### Eventos Consumidos por Roadmap:
1. **`LIFE_DEBITED`:**
   - Emitido cuando un alumno pierde una vida (por ejemplo, tras fallar un desafío).
   - Roadmap actualiza el indicador de `recovery_pending = true` si el alumno se quedó sin vidas.
2. **`LIFE_CREDITED`:**
   - Emitido tras completar un desafío de recuperación o una compra.
   - Roadmap desmarca `recovery_pending` cuando el saldo vuelve a ser positivo.

---

## 6. Seguridad y Scopes M2M

| Scope | Destinado a | Propósito |
|---|---|---|
| `accounting.equipment.read` | `roadmap-service` | Lectura de equipamiento e inventario para HU-35. |
| `accounting.lives.read` | `roadmap-service` | Validación de vidas libres y desempate de ranking. |
| `accounting.reservation.write` | `engine-challenge-service` | Creación y confirmación de holds al iniciar intentos. |

---

## 7. Clientes y Adaptadores en `tpi-roadmap`
- Clientes HTTP: `com.utn.tpi.roadmap.clients.InventoryClient`, `com.utn.tpi.roadmap.clients.AccountingLivesClient`.
- Listener Kafka: `com.utn.tpi.roadmap.events.lives.AccountingEventsListener`.
- Resiliencia: Circuit breaker con fallback a datos locales en UI; falla cerrado en Gate.
