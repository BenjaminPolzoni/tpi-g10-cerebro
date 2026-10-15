# Contrato Roadmap ↔ Backoffice PAR (Tema 12)

Estado: **contrato recibido (CONTRATO_T10_BACKOFFICE.md)**. Cubre REST + eventos de PAR-01/08/09.
Base: `agent.md` §3.3; `clients/backoffice/ParCatalogClient.java`.

Estado: cliente REST con caché + invalidación por evento implementados (`clients/backoffice`, `events/ParRefreshListener`). Todavía ningún caso de uso consume PAR (niveles y ranking futuros).

> Los valores PAR los posee BackOffice; nunca constantes de código. Solo rigen hacia adelante.

---

## 1. Base y headers servicio-a-servicio

| Dato | Valor |
|---|---|
| Base local | `http://localhost:8080` |
| Base Gateway | `https://<gateway-host>` |
| Eureka | `tema-12-backoffice-service` |
| Autenticación | Token de servicio de Roadmap: `Authorization: Bearer`, audience `backoffice-service`, scope `backoffice.parameters.read` (Backoffice exige la authority sin `SCOPE_`). El Gateway descarta los `X-User-*` que manda un micro. Confirmado por plataforma (revisión de la #77). |


---

## 2. Endpoints

| Método | Endpoint | Uso |
|---|---|---|
| `GET` | `/api/backoffice/parameters` | **Cold start**: lista completa vigente en una llamada |
| `GET` | `/api/backoffice/parameters/{key}` | Consulta puntual (ej. `PAR-09`) |

Respuesta: `{ "key": "PAR-01", "value": {...}, "version": 1 }` (DTO genérico `ParameterResponseDto<T>` con `@JsonIgnoreProperties(ignoreUnknown = true)`).

---

## 3. Parámetros

### PAR-01 — XP base por dificultad

`value`: `{ "easy": 100, "medium": 250, "hard": 500 }`.

⚠️ Choque: nuestro `ParProperties.BaseXp` usa `basic/medium/advanced`. **Claves del contrato (`easy/medium/hard`)** adoptadas en cliente, properties y tests.

### PAR-08 — XP por defecto para desbloqueo

`value`: `500`. **Fuera de nuestro alcance por decisión**: nuestro desbloqueo es por prerrequisitos, no por umbral de XP. No se agrega a la config ni se consume.

### PAR-09 — Curva de niveles (10 niveles)

`value`: `[{ "level": 1, "xpRequired": 0 }, ...]` (10 entradas).

Parser adaptado: extrae `xpRequired` en orden con la misma validación (arranca en 0, estrictamente ascendente, máx 10, niveles 1..N en secuencia).

### PAR-12 — Vidas iniciales y techo

`value`: `{ "initialLives": 3, "maxLives": 3 }`. Se consume como el resto (`ParCatalogClient.lives()`): positivos y techo >= iniciales. PAR-13 (reintentos) no está en el contrato T12 y queda pendiente explícito: sin dueño ni lector actual, se define su fuente antes de usarlo.

---

## 4. Evento `GLOBAL_CONFIGURATION_CHANGED`

Topic `administration.events`, key = valor de `param_key`. Sobre y payload en snake_case (contratos-kafka v8, un solo nombre por campo, sin alias): Backoffice publica `payload.param_key` desde su 2.0.0 (#208).

El listener lee solo `param_key` (obligatorio) y `version` (para el log). Un payload con `paramKey` en camelCase se ignora y se confirma: no hay fallback.

Resto del payload según el contrato recibido, con nombres v8 **a confirmar por Backoffice** (#208): `value`, `previousVersion`, `description`, `updatedAt`, `updatedBy`.

Sirve para aplicar cambios **solo hacia adelante** y versionar (`previousVersion` permite detectar saltos). El listener ya invalida la clave ante el evento; queda para cuando Backoffice publique de verdad.

⚠️ El sobre también se lee en v8 (`event_id`, `event_type`, `event_version` = 1, `timestamp`, `producer`, `payload`; `EventParser`). Un sobre en camelCase va a la DLT y no invalida la caché: queda el TTL de 5 minutos.

---

## 5. Qué falta (follow-up a Backoffice)

1. Confirmar `producer`: `tema-12-backoffice-service`.
