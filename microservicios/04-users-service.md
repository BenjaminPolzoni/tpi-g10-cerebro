# Microservicio: Users & Identity Service (`tpi-users`)

> **Ficha Técnica Canónica y Contrato de Integración**  
> Tema: **Tema 05 — Autenticación, Identidad y Gestión de Usuarios**  
> Equipo Responsable: **Tema 05 (Gxx)**  
> Repositorio: `2026-P4-BE/tpi-users` (Local: `D:\Dev\IdeaProjects\Progra4\tpi-users`)  
> Estado: **Vigente (v2.0.0)**

---

## 1. Identidad y Red

| Parámetro | Valor |
|---|---|
| **Nombre de Aplicación (Eureka)** | `users-service` |
| **Prefijo en API Gateway** | `/api/users/**` |
| **Puerto por Defecto** | `8082` |
| **Puerto de Gestión (Management/Actuator)** | `8083` (`management.server.port`) |
| **Rutas Públicas** | `${app.api.public-path}/**` (`/api/users/public/**`, JWKS, emisión de tokens) |
| **Rutas Privadas** | `${app.api.private-path}/**` (`/api/users/**`) |
| **JWKS Endpoint** | `/.well-known/jwks.json` (consumido por API Gateway) |
| **Base de Datos** | MySQL / PostgreSQL (Flyway `db/migration`) |
| **Caché / Sesiones** | Redis (`6379`) |

---

## 2. Dominio y Responsabilidades

### Qué Hace Users Service (Fuente de Verdad de Identidad)
- **Proveedor de Identidad (IdP):** Autenticación de personas, login por credenciales, OAuth2/OIDC, registro y verificación de email.
- **Emisión de Tokens:**
  - Tokens de usuario final (JWT con claims `sub`, `roles`, etc.).
  - Tokens de servicio técnico M2M (`grant_type=client_credentials`).
- **Catálogo de Claves Públicas (JWKS):** Publica las claves RSA con las que el API Gateway verifica las firmas de los JWT entrantes.
- **Gestión de Perfiles y Avatares 2D:** Nombres, apellidos, legajos, correos institucionales e imágenes de perfil.

### Qué NO Hace Users Service
- **NO gestiona matrículas en cursos:** La relación alumno-curso es potestad de `course-service`.
- **NO gestiona la personalización 3D del alumno en el mapa:** El avatar 3D (ropa, colores, accesorios 3D en el canvas Three.js) es gestionado por `roadmap-service` (`StudentAvatarController`).

---

## 3. Emisión de Tokens de Servicio M2M (`client_credentials`)

Todos los microservicios que necesiten invocar APIs de otros servicios deben autenticarse primero contra `users-service` para obtener un JWT técnico.

### Endpoint de Emisión de Token
- **Método y URL:** `POST /api/users/public/auth/token`
- **Content-Type:** `application/json` (o `application/x-www-form-urlencoded`)
- **Body de la Petición:**
```json
{
  "grant_type": "client_credentials",
  "client_id": "roadmap-service",
  "client_secret": "${APP_CLIENT_SECRET}",
  "audience": "course-service"
}
```

### Respuesta Exitosa (200 OK):
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "course.sections.read course.groups.read"
}
```

### Reglas de Uso en Clientes M2M:
- **Caché Obligatoria:** Los microservicios emisores (incluido `roadmap-service`) deben cachear el token en memoria respetando el campo `expires_in` (con margen de seguridad de 60 segundos). **Está estrictamente prohibido solicitar un token por cada request HTTP.**
- **Audiencia Específica:** Debe solicitarse un token por cada microservicio de destino (`audience`).

---

## 4. Endpoints REST Consumidos por Roadmap

### 4.1 Consulta de Perfiles en Lote (`/api/users/batch`)
Roadmap consume este endpoint para enriquecer la pantalla de ranking visualizada por el docente (`PROFESSOR`/`MANAGER`), sustituyendo UUIDs anónimos por nombres y legajos reales.
- **Método y URL:** `POST /api/users/batch`
- **Scope Requerido:** `users.profile.batch.read`
- **Body:**
```json
{
  "user_ids": [
    "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
    "c8a1b2c3-d4e5-6f7a-8b9c-0d1e2f3a4b5c"
  ]
}
```
- **Respuesta Exitosa (200 OK):**
```json
[
  {
    "id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
    "first_name": "Juan",
    "last_name": "Pérez",
    "username": "jperez",
    "email": "jperez@alumno.utn.edu.ar",
    "student_id": "45678"
  }
]
```

---

## 5. Headers de Identidad Propagados por el API Gateway

Una vez validado el JWT de `users-service`, el Gateway inyecta los siguientes headers reservados hacia los microservicios internos:

| Header | Tipo | Descripción |
|---|---|---|
| `X-Principal-Type` | String | `"user"` (persona autenticada) o `"service"` (llamada técnica M2M). |
| `X-User-Id` | UUID | ID único del usuario autenticado (`sub` del JWT). |
| `X-User-Roles` | String | Roles asignados separados por coma (`STUDENT,PROFESSOR,MANAGER,ADMIN`). |
| `X-Service-Id` | String | Identidad del microservicio emisor en llamadas M2M (ej. `roadmap-service`). |
| `X-Service-Scopes` | String | Scopes técnicos habilitados para el servicio emisor. |
| `traceparent` / `X-Request-Id` | String | Identificador de trazabilidad distribuida para logs correlacionados. |

---

## 6. Clientes y Adaptadores en `tpi-roadmap`
- Gestor de Tokens: `com.utn.tpi.roadmap.security.ServiceTokenManager` (solicitud, caching con expiración y renovación transparente).
- Cliente de Perfiles: `com.utn.tpi.roadmap.clients.UsersProfileClient`.
