# Mapa y Catálogo de Microservicios — Plataforma Gamificada de Aprendizaje

> **Directorio Central de Servicios y Repositorios**  
> Proyecto: Plataforma Gamificada de Aprendizaje (TPI 4° Cuatrimestre, UTN FRC)  
> Grupo 10 · Roadmap (`roadmap-service`)

Este directorio consolida en un único lugar toda la información técnica, funcional, arquitectónica, de contratos REST y eventos Kafka de cada microservicio de la plataforma, evitando la dispersión de especificaciones en múltiples notas o carpetas aisladas.

---

## 1. Matriz General de Microservicios

> [!important] Fuente de verdad
> Los segmentos, los puertos, el equipo, la base y los scopes (`offers` / `needs`) salen del registro de la plataforma: `tpi-system-compose/registry/services.yml` (local en `~/dev/TPI_2026/Backend/tpi-system-compose`). Si esta tabla y el registro no coinciden, **vale el registro**. Tabla revisada contra el registro el 2026-10-26.

Todos los repos de back están en la organización `2026-P4-BE` (rama por defecto `main`). Los de front están en `2026-P4-FE` (rama por defecto `develop`).

| # | Microservicio / Repo | Segmento Gateway | Puerto (registry) | Equipo / Tema | Responsabilidad Principal |
|---|---|---|---|---|---|
| **01** | [`course-service`](01-course-service.md) (`tpi-course`) | `/api/course/**` | `8086` | grupo-01 · Tema 01 | Cursos, cohortes, secciones, módulos, comisiones y matrículas. Es dueño del ciclo de vida de la cohorte (archivar) y de `finalAcademicStatus`. |
| **02** | [`engine-challenge-service`](02-engine-challenge-service.md) (`tpi-engine-challenge`) | `/api/engine-challenge/**` | `8096` | g09 · Tema 09 | Ciclo de vida y corrección de desafíos; calcula XP, vidas y monedas ganadas/perdidas. |
| **03** | [`accounting-service`](03-accounting-service.md) (`tpi-accounting`) | `/api/accounting/**` | `8090` | accounting · Tema 08 | Fuente de verdad de vidas, saldo de monedas, reservas (holds) e inventario/equipamiento. MySQL. |
| **04** | [`users-service`](04-users-service.md) (`tpi-users`) | `/api/users/**` | plataforma | plataforma (G07) | Identidad OIDC/OAuth2, login, JWKS, tokens de usuario y de servicio M2M, perfiles y legajo. |
| **05** | [`backoffice-service`](05-backoffice-service.md) (`tpi-backoffice`) | `/api/backoffice/**` | `8098` | grupo-06 · Tema 12 | Catálogo de parámetros globales (PAR-01 XP base, PAR-09 niveles, PAR-12 vidas). |
| **06** | [`notifications-bus-service`](06-notifications-bus-service.md) (`tpi-notifications`) | `/api/notifications/**` | plataforma | plataforma · Tema 02 | Bus Kafka KRaft unificado, contratos de eventos, notificaciones por email y web push. |
| **07** | [`api-gateway`](07-api-gateway.md) (`tpi-api-gateway`) | `/api/**` | `8080` | Infra · Tema 11 | Reverse proxy perimetral SCG, validación JWT, inyección de headers `X-*`, rate limiting y circuit breakers. |
| **08** | [`frontend-app`](08-frontend-app.md) (`2026-P4-FE/2026-PIV-TPI-FE`, UI Kit en `2026-P4-FE/2026-PIV-TPI-UI-KIT`) | UI (`/`) | `4200` / `8000` | Frontend (P4) | SPA Angular 18+, UI Kit `@2026-p4-fe/ui`, visor 3D de roadmap, inventario y avatares. |
| **09a** | [`practical-challenge-service`](09-challenges-services.md) (`tpi-practical-challenge`) | `/api/practical-challenge/**` | `8094` | g05 · Tema 03 | Desafíos prácticos (código). Su cliente de escritorio es `tpi-practical-challenge-desktop` (Electron). |
| **09b** | [`theoretical-challenge-service`](09-challenges-services.md) (`tpi-theoristcal-challenge`, así se escribe el repo) | `/api/theoretical-challenge/**` | `8088` | g04 · Tema 04 | Cuestionarios teóricos y su corrección. |
| **10** | [`roadmap-service`](10-roadmap-service.md) (`tpi-roadmap`) | `/api/roadmap/**` | `8010` | roadmap · Tema 10 (G10) | Grafo y progresión de aprendizaje, elegibilidad (Gate), ledger de XP, rankings dinámicos y avatar 3D. |
| **12** | `llm-service` (`tpi-llm`) | `/api/llm/**` | `8084` | g03 · Tema 07 | Evaluación LLM: nota del uso de la IA en un desafío, Golden Set, rúbrica calibrada, moderación del chat y tutor socrático. |
| **13** | `sandbox-service` (`tpi-sandbox`) | `/api/sandbox/**` | `8092` | g08 | Ejecución aislada del código de los desafíos prácticos (`sandbox.executions.use`). |
| **14** | `market-service` (`tpi-market`) | `/api/market/**` | `8100` | market | Mercado/tienda de la plataforma. |
| **15** | `community-service` (`tpi-community`) | — (no está en el registro) | — | — | Todavía es solo el andamio, sin código de negocio (2026-10-26). |
| — | `tpi-skills-hub` | — | — | — | No es un micro de la plataforma: es la migración del Skill Hub a Angular + Spring Boot. |
| — | `tpi-system-compose` | — | — | plataforma | Compose, registro (`registry/services.yml`), Vault, mesh Tailscale, bus y plantillas de equipo. |

Los repos `ci-cd-paso-a-paso`, `delivery-lab`, `turnos-api` y `tienda-api` también están en la organización, pero son material de clase y no forman parte del sistema.

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

---

## 4. Cómo leer el código de otro micro (para cualquier agente)

Se hace **solo en modo lectura** y sin clonar, con el `gh` CLI autenticado. No se abren PRs ni se pushea a repos de otros equipos: lo que haga falta se pide por issue.

```bash
# Buscar un símbolo o un texto en un repo
gh search code "finalAcademicStatus" --repo 2026-P4-BE/tpi-course --limit 30
# Ver solo los paths (sin javadoc generado)
gh search code "X" --repo 2026-P4-BE/<repo> --json path --jq '.[].path' | grep -v java_doc | sort -u
# Leer un archivo entero
gh api repos/2026-P4-BE/<repo>/contents/<path> -H "Accept: application/vnd.github.raw"
# Árbol de archivos
gh api "repos/2026-P4-BE/<repo>/git/trees/main?recursive=1" --jq '.tree[].path'
# Último commit (para anotar contra qué se verificó)
gh api repos/2026-P4-BE/<repo>/commits/main --jq '.sha[0:8]+" "+.commit.committer.date'
# Issues y PRs
gh search issues --repo 2026-P4-BE/<repo> "texto"; gh search prs --repo 2026-P4-BE/<repo> "texto"
```

> [!warning] Límites
> - `gh search code` busca **solo en la rama por defecto**, y su índice puede ir atrasado algunas horas.
> - Tampoco ve escrituras indirectas, como MapStruct o `copyProperties`. Para afirmar que «nadie hace X», leer los mappers o services con `gh api .../contents`, o clonar en una carpeta aparte: `gh repo clone 2026-P4-BE/<repo> /tmp/<repo> -- --depth 1`.
> - Al citar código ajeno en una nota, poner el repo, el path y el commit.
