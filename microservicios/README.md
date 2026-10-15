# Mapa y Catálogo de Microservicios — Plataforma Gamificada de Aprendizaje

> **Directorio Central de Servicios y Repositorios**  
> Proyecto: Plataforma Gamificada de Aprendizaje (TPI 4° Cuatrimestre, UTN FRC)  
> Grupo 10 · Roadmap (`roadmap-service`)

Este directorio consolida en un único lugar toda la información técnica, funcional, arquitectónica, de contratos REST y eventos Kafka de cada microservicio de la plataforma, evitando la dispersión de especificaciones en múltiples notas o carpetas aisladas.

---

## 1. Matriz General de Microservicios

| # | Microservicio / Repo | Segmento Gateway | Puerto App (Mgmt) | Tema / Grupo | Responsabilidad Principal |
|---|---|---|---|---|---|
| **01** | [`course-service`](01-course-service.md) (`tpi-course`) | `/api/course/**` | `8086` (`8087`) | Tema 01 (G01) | Cursos, cohortes, secciones, módulos, comisiones y matrículas. |
| **02** | [`engine-challenge-service`](02-engine-challenge-service.md) (`tpi-engine-challenge`) | `/api/engine-challenge/**` | `8086` (`8087`) | Tema 09 (G09) | Ciclo de vida y corrección de desafíos; calcula XP, vidas y monedas ganadas/perdidas. |
| **03** | [`accounting-service`](03-accounting-service.md) (`tpi-accounting`) | `/api/accounting/**` | `8084` (`8085`) | Tema 08 (Gxx) | Fuente de verdad de vidas, saldo de monedas, reservas (holds) e inventario/equipamiento. |
| **04** | [`users-service`](04-users-service.md) (`tpi-users`) | `/api/users/**` | `8082` (`8083`) | Tema 05 (Gxx) | Identidad OIDC/OAuth2, login, JWKS, tokens de usuario y tokens de servicio M2M, perfiles de usuario. |
| **05** | [`backoffice-service`](05-backoffice-service.md) (`tpi-backoffice`) | `/api/backoffice/**` | `8088` (`8089`) | Tema 12 (G06) | Catálogo de parámetros globales (PAR-01 XP base, PAR-09 niveles, PAR-12 vidas). |
| **06** | [`notifications-bus-service`](06-notifications-bus-service.md) (`tpi-notifications`) | `/api/notifications/**` | `8090` (`8091`) | Tema 02 (G02) | Bus Kafka KRaft unificado, contratos de eventos, notificaciones por email y web push. |
| **07** | [`api-gateway`](07-api-gateway.md) (`tpi-api-gateway`) | `/api/**` | `8080` (`8081`) | Tema 11 (Infra) | Reverse proxy perimetral SCG, validación JWT, inyección de headers `X-*`, rate limiting y circuit breakers. |
| **08** | [`frontend-app`](08-frontend-app.md) (`2026-PIV-TPI-FE`) | UI (`/`) | `4200` / `8000` | Frontend (P4) | SPA Angular 18+, UI Kit `@2026-p4-fe/ui`, visor 3D de roadmap, inventario y avatares. |
| **09** | [`challenges-services`](09-challenges-services.md) (`tpi-practical/theoretical`) | `/api/practical-challenge/**`, `/api/theoretical-challenge/**` | `8092` / `8094` | Temas 03/04 | Ejecución de desafíos prácticos (Docker/código) y corrección de cuestionarios teóricos. |
| **10** | [`roadmap-service`](10-roadmap-service.md) (`tpi-roadmap`) | `/api/roadmap/**` | `8010` (`8011`) | Tema 10 (G10) | Grafo y progresión de aprendizaje, elegibilidad (Gate), ledger de XP, rankings dinámicos y avatar 3D. |

---

## 2. Mapa de Integración y Flujo de Datos

```mermaid
flowchart TD
    FE["Frontend Angular (2026-PIV-TPI-FE)"] -->|Cookie fu_at| GW["API Gateway (api-gateway :8080)"]
    
    GW -->|/api/course| CS["course-service (tpi-course)"]
    GW -->|/api/engine-challenge| ES["engine-challenge-service (tpi-engine-challenge)"]
    GW -->|/api/accounting| AC["accounting-service (tpi-accounting)"]
    GW -->|/api/users| US["users-service (tpi-users)"]
    GW -->|/api/backoffice| BO["backoffice-service (tpi-backoffice)"]
    GW -->|/api/roadmap| RS["roadmap-service (tpi-roadmap)"]

    %% M2M via Gateway
    RS -.->|M2M Token /api/course| CS
    RS -.->|M2M Token /api/accounting| AC
    RS -.->|M2M Token /api/backoffice| BO
    RS -.->|M2M Token /api/users| US
    ES -.->|M2M Token /api/roadmap Gate| RS
    ES -.->|M2M Token /api/accounting Holds| AC

    %% Kafka Events
    ES ==>|challenges.events| BUS["Kafka Event Bus"]
    BUS ==>|CHALLENGE_COMPLETED| RS
    AC ==>|accounting.events| BUS
    BUS ==>|LIFE_CREDITED / LIFE_DEBITED| RS
    BO ==>|administration.events| BUS
    BUS ==>|GLOBAL_CONFIGURATION_CHANGED| RS
    RS ==>|roadmap.events (Outbox)| BUS
```

---

## 3. Guía de Consulta Rápida por Escenario

- **Si vas a tocar matriculaciones, secciones o comisiones:**  
  Consulta [`01-course-service.md`](01-course-service.md).
- **Si vas a tocar el Gate de elegibilidad, inicio o fin de desafíos:**  
  Consulta [`02-engine-challenge-service.md`](02-engine-challenge-service.md) y [`03-accounting-service.md`](03-accounting-service.md).
- **Si vas a tocar vidas, inventario, ítems equipados o desempate en ranking:**  
  Consulta [`03-accounting-service.md`](03-accounting-service.md).
- **Si vas a tocar autenticación, tokens técnicos M2M o nombres de alumnos en ranking:**  
  Consulta [`04-users-service.md`](04-users-service.md).
- **Si vas a tocar umbrales de XP, curvas de niveles o parámetros globales:**  
  Consulta [`05-backoffice-service.md`](05-backoffice-service.md).
- **Si vas a publicar o consumir eventos Kafka:**  
  Consulta [`06-notifications-bus-service.md`](06-notifications-bus-service.md).
- **Si vas a probar llamadas por Gateway o headers de identidad:**  
  Consulta [`07-api-gateway.md`](07-api-gateway.md).
- **Si vas a integrar pantallas de Angular, proxies o UI Kit:**  
  Consulta [`08-frontend-app.md`](08-frontend-app.md).
- **Si vas a implementar o modificar la lógica de Roadmap:**  
  Consulta [`10-roadmap-service.md`](10-roadmap-service.md).
- **Si vas a levantar nuestra variante del roadmap (back + front) para probar:**  
  Consulta [`11-levantar-variante-roadmap.md`](11-levantar-variante-roadmap.md).
