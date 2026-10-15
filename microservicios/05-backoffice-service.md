# Microservicio: Backoffice Service (`tpi-backoffice`)

> **Ficha Técnica Canónica y Contrato de Integración**  
> Tema: **Tema 12 — Backoffice y Parámetros Globales de la Plataforma**  
> Equipo Responsable: **Grupo 06 (G06)**  
> Repositorio: `2026-P4-BE/tpi-backoffice`  
> Estado: **Vigente (v2.0.0)**

---

## 1. Identidad y Red

| Parámetro | Valor |
|---|---|
| **Nombre de Aplicación (Eureka)** | `backoffice-service` |
| **Prefijo en API Gateway** | `/api/backoffice/**` |
| **Puerto por Defecto** | `8088` |
| **Puerto de Gestión (Management/Actuator)** | `8089` (`management.server.port`) |
| **Rutas Públicas** | `${app.api.public-path}/**` (`/api/backoffice/public/**`) |
| **Rutas Privadas** | `${app.api.private-path}/**` (`/api/backoffice/**`) |
| **Audience M2M** | `backoffice-service` |

---

## 2. Dominio y Responsabilidades

### Qué Hace Backoffice Service (Fuente de Verdad)
- **Administración Global de la Plataforma:** Parámetros configurables del sistema (PAR), reglas de negocio globales y catálogos de referencia.
- **Vigencia Prospectiva (No Retroactiva):** Los cambios sobre los parámetros PAR rigen únicamente **hacia adelante** (RF-CFG-06). Modificar el XP base o el tope de vidas no recalcula eventos o liquidaciones pasadas.

### Qué NO Hace Backoffice Service
- **NO calcula niveles ni rankings de alumnos:** Publica los umbrales de la curva; Roadmap es quien calcula el nivel del alumno a partir de su `total_xp`.
- **NO almacena saldo de monedas ni vidas de alumnos.**

---

## 3. Parámetros Consumidos por Roadmap

Roadmap consume los siguientes parámetros canónicos del catálogo:

| Parámetro | Concepto | Estructura / Valores de Ejemplo | Uso en Roadmap |
|---|---|---|---|
| **`PAR-01`** | XP base por dificultad de desafío | `{"easy": 100, "medium": 250, "hard": 500}` | Estimación referencial visual y metadata de nodos. |
| **`PAR-09`** | Curva oficial de niveles | Array ordenado de hasta **200 niveles** con su umbral de XP acumulado | Cálculo del nivel actual y progreso porcentual hacia el siguiente nivel (`LevelService`). |
| **`PAR-12`** | Vidas iniciales y tope máximo | `{"initial_lives": 5, "max_lives": 5}` | Techo de vidas y visualización en inventario. |

---

## 4. Endpoints REST Consumidos por Roadmap

### 4.1 Carga Inicial de Catálogo de Parámetros (`/api/backoffice/parameters`)
Roadmap invoca este endpoint en el arranque (cold-start) y cachea la respuesta en memoria utilizando Caffeine Cache:
- **Método y URL:** `GET /api/backoffice/parameters`
- **Scope Requerido:** `backoffice.parameters.read`
- **Headers:**  
  `Authorization: Bearer <m2m_token>`  
  `X-Service-Id: roadmap-service`
- **Respuesta Exitosa (200 OK):**
```json
{
  "parameters": [
    {
      "key": "PAR-01",
      "value": {
        "easy": 100,
        "medium": 250,
        "hard": 500
      },
      "updated_at": "2026-10-01T12:00:00Z"
    },
    {
      "key": "PAR-09",
      "value": {
        "levels": [
          {"level": 1, "min_xp": 0},
          {"level": 2, "min_xp": 100},
          {"level": 3, "min_xp": 250},
          {"level": 4, "min_xp": 500},
          {"level": 5, "min_xp": 1000},
          {"level": 6, "min_xp": 2000},
          {"level": 7, "min_xp": 4000},
          {"level": 8, "min_xp": 8000},
          {"level": 9, "min_xp": 15000},
          {"level": 10, "min_xp": 30000}
        ]
      },
      "updated_at": "2026-10-11T18:00:00Z"
    },
    {
      "key": "PAR-12",
      "value": {
        "initial_lives": 5,
        "max_lives": 5
      },
      "updated_at": "2026-10-01T12:00:00Z"
    }
  ]
}
```

---

## 5. Eventos Kafka y Actualización Reactiva

- **Tópico:** `administration.events`
- **Clave del Mensaje (`Key`):** `param_key` (ej. `"PAR-09"`)

### Evento `GLOBAL_CONFIGURATION_CHANGED`:
Cuando un administrador modifica un parámetro en Backoffice, se emite este evento:
```json
{
  "event_id": "8f3e2b10-67a9-45bc-98de-112233445566",
  "event_type": "GLOBAL_CONFIGURATION_CHANGED",
  "timestamp": "2026-10-15T09:00:00.000Z",
  "producer": "backoffice-service",
  "payload": {
    "param_key": "PAR-09",
    "updated_at": "2026-10-15T09:00:00.000Z"
  }
}
```

### Comportamiento en Roadmap:
- El consumidor `AdministrationEventsListener` recibe el evento.
- Si `param_key == "PAR-09"` o `"PAR-12"`, invalida la caché local de Caffeine inmediatamente.
- La próxima consulta de nivel u hoja de vidas dispara un refresco pull contra `/api/backoffice/parameters`.

---

## 6. Clientes y Adaptadores en `tpi-roadmap`
- Cliente HTTP: `com.utn.tpi.roadmap.clients.ParCatalogClient`.
- Servicio de Niveles: `com.utn.tpi.roadmap.services.LevelService`.
- Listener Kafka: `com.utn.tpi.roadmap.events.administration.AdministrationEventsListener`.
