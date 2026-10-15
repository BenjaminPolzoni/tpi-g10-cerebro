# Contrato de Integración: Parámetros de Roadmap y Progreso (T10 ↔ T12)

> **Destinatario:** Equipo Tema 10 (Roadmap y Progreso)  
> **Emisor:** Equipo Tema 12 (Backoffice)  
> **Propósito:** Definición de los endpoints REST síncronos, DTOs en Java, respuestas JSON y eventos asíncronos en Apache Kafka para la gestión de curvas de niveles, desbloqueos y progresión de XP del estudiante según el PRD oficial.

---

## 🏛️ 1. URLs Base y Headers de Seguridad Obligatorios

* **Base URL Local (Docker / Red interna):** `http://localhost:8080`
* **Base URL Gateway (Producción / Integración):** `https://<gateway-host>`
* **Service Name (Eureka):** `tema-12-backoffice-service`

### Headers de Seguridad Obligatorios
Para solicitudes de servicio a servicio (Service-to-Service), los endpoints están protegidos por el filtro de seguridad de plataforma. Roadmap debe propagar:

```http
X-User-Roles: MS
X-User-Id: tema-10-roadmap-progreso
```

> [!WARNING]  
> Si estos headers no viajan en la petición HTTP, el microservicio rechazará la solicitud devolviendo un código `403 Forbidden`.

---

## 🌐 2. Endpoints (Rutas Disponibles)

| Método | Endpoint | Uso recomendado |
|---|---|---|
| `GET` | `/api/administration/parameters` | **Recomendado:** Devuelve la lista completa de parámetros vigentes en una única llamada (ideal en el Cold Start para poblar la escala de progresión). |
| `GET` | `/api/administration/parameters/{key}` | Consulta individual de un parámetro puntual por su clave (ej: `/api/administration/parameters/PAR-09`). |

---

## 📋 3. Tabla de Parámetros Involucrados

Parámetros requeridos por el servicio de Roadmap y Progreso según el PRD (RF-CFG-04 y modelo de niveles):

| Parámetro | Concepto de Negocio | Valor en PRD | Rol en Roadmap y Progreso |
|---|---|:---:|---|
| **`PAR-01`** | XP Base por dificultad | `{"easy": 100, "medium": 250, "hard": 500}` | Referencia de escala para estimar el avance de nodos en el grafo de aprendizaje. |
| **`PAR-08`** | XP por defecto para desbloqueo | `500` | Cantidad estándar de XP acumulada requerida para desbloquear el siguiente bloque o nodo. |
| **`PAR-09`** | Curva de niveles | Array progresivo de **10 niveles** | Escala oficial de puntos acumulados para calcular el nivel actual (`LevelUp`) del estudiante. |

---

## ☕ 4. DTO Java Base y Consulta General

### 4.1 DTO Genérico (`ParameterResponseDto.java`)
```java
package ar.edu.utn.frc.tup.p4.client.dtos.parameters;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class ParameterResponseDto<T> {

    private String key;
    private T value;
    private Integer version;
}
```

### 4.2 Consulta General: `GET /api/administration/parameters`
*Response `200 OK`:*
```json
[
  {
    "key": "PAR-01",
    "value": {
      "easy": 100,
      "medium": 250,
      "hard": 500
    },
    "version": 1
  },
  {
    "key": "PAR-08",
    "value": 500,
    "version": 1
  },
  {
    "key": "PAR-09",
    "value": [
      { "level": 1, "xpRequired": 0 },
      { "level": 2, "xpRequired": 500 },
      { "level": 3, "xpRequired": 1200 },
      { "level": 4, "xpRequired": 2200 },
      { "level": 5, "xpRequired": 3500 },
      { "level": 6, "xpRequired": 5200 },
      { "level": 7, "xpRequired": 7300 },
      { "level": 8, "xpRequired": 9800 },
      { "level": 9, "xpRequired": 13000 },
      { "level": 10, "xpRequired": 17000 }
    ],
    "version": 1
  }
]
```

---

## 🔍 5. Detalle Ordenado por Parámetro (Endpoint, JSON, DTO y Evento Kafka)

---

### 5.1 `PAR-01` — XP Base por Dificultad

#### A. Endpoint Individual
`GET /api/administration/parameters/PAR-01`

#### B. JSON de Respuesta (200 OK)
```json
{
  "key": "PAR-01",
  "value": {
    "easy": 100,
    "medium": 250,
    "hard": 500
  },
  "version": 1
}
```

#### C. DTO Específico en Java
```java
package ar.edu.utn.frc.tup.p4.client.dtos.parameters;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class XpBaseByDifficultyDto {

    private Integer easy;
    private Integer medium;
    private Integer hard;
}
```

#### D. Evento de Kafka (`administration.events`)
* **Partition Key:** `"PAR-01"`
* **Payload emitido:**
```json
{
  "eventId": "uuid-par-01",
  "eventType": "GLOBAL_CONFIGURATION_CHANGED",
  "eventVersion": 1,
  "timestamp": "2026-09-24T10:00:00Z",
  "producer": "tema-12-backoffice-service",
  "payload": {
    "paramKey": "PAR-01",
    "value": { "easy": 100, "medium": 250, "hard": 500 },
    "version": 2,
    "previousVersion": 1,
    "description": "XP base según dificultad",
    "updatedAt": "2026-09-24T10:00:00Z",
    "updatedBy": "usr-admin-8831"
  }
}
```

---

### 5.2 `PAR-08` — XP por Defecto para Desbloqueo

#### A. Endpoint Individual
`GET /api/administration/parameters/PAR-08`

#### B. JSON de Respuesta (200 OK)
```json
{
  "key": "PAR-08",
  "value": 500,
  "version": 1
}
```

#### C. DTO en Java
```java
ParameterResponseDto<Integer> response;
Integer xpDesbloqueoDefault = response.getValue(); // 500 XP
```

#### D. Evento de Kafka (`administration.events`)
* **Partition Key:** `"PAR-08"`
* **Payload emitido:**
```json
{
  "eventId": "uuid-par-08",
  "eventType": "GLOBAL_CONFIGURATION_CHANGED",
  "eventVersion": 1,
  "timestamp": "2026-09-24T10:05:00Z",
  "producer": "tema-12-backoffice-service",
  "payload": {
    "paramKey": "PAR-08",
    "value": 500,
    "version": 2,
    "previousVersion": 1,
    "description": "XP requerida por defecto para desbloquear contenido",
    "updatedAt": "2026-09-24T10:05:00Z",
    "updatedBy": "usr-admin-8831"
  }
}
```

---

### 5.3 `PAR-09` — Curva de Niveles (10 Niveles)

#### A. Endpoint Individual
`GET /api/administration/parameters/PAR-09`

#### B. JSON de Respuesta (200 OK)
```json
{
  "key": "PAR-09",
  "value": [
    { "level": 1, "xpRequired": 0 },
    { "level": 2, "xpRequired": 500 },
    { "level": 3, "xpRequired": 1200 },
    { "level": 4, "xpRequired": 2200 },
    { "level": 5, "xpRequired": 3500 },
    { "level": 6, "xpRequired": 5200 },
    { "level": 7, "xpRequired": 7300 },
    { "level": 8, "xpRequired": 9800 },
    { "level": 9, "xpRequired": 13000 },
    { "level": 10, "xpRequired": 17000 }
  ],
  "version": 1
}
```

#### C. DTO Específico en Java
```java
package ar.edu.utn.frc.tup.p4.client.dtos.parameters;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class LevelThresholdDto {

    private Integer level;
    private Integer xpRequired;
}
```

#### D. Evento de Kafka (`administration.events`)
* **Partition Key:** `"PAR-09"`
* **Payload emitido:**
```json
{
  "eventId": "uuid-par-09",
  "eventType": "GLOBAL_CONFIGURATION_CHANGED",
  "eventVersion": 1,
  "timestamp": "2026-09-24T10:10:00Z",
  "producer": "tema-12-backoffice-service",
  "payload": {
    "paramKey": "PAR-09",
    "value": [
      { "level": 1, "xpRequired": 0 },
      { "level": 2, "xpRequired": 500 },
      { "level": 3, "xpRequired": 1200 },
      { "level": 4, "xpRequired": 2200 },
      { "level": 5, "xpRequired": 3500 },
      { "level": 6, "xpRequired": 5200 },
      { "level": 7, "xpRequired": 7300 },
      { "level": 8, "xpRequired": 9800 },
      { "level": 9, "xpRequired": 13000 },
      { "level": 10, "xpRequired": 17000 }
    ],
    "version": 2,
    "previousVersion": 1,
    "description": "Curva progresiva de XP acumulada por nivel (10 niveles)",
    "updatedAt": "2026-09-24T10:10:00Z",
    "updatedBy": "usr-admin-8831"
  }
}
```
