---
tags: [tpi, g10, taiga, us]
codigo: US-3572
ref: 3572
estado: "Done"
responsable: "Mateo Delgado Costa"
epica: "[G10] — Esqueleto del servicio Roadmap — TRANSVERSAL (v3)"
sprint: "G10 - Sprint 1"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/3572
---

# US-3572: Servicio roadmap-service operativo y descubrible

> [!info] Generado desde Taiga (2026-10-14 18:47). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/3572) · Estado: **Done** · Responsable: **Mateo Delgado Costa** · Sprint: **G10 - Sprint 1**

[G10] – Servicio roadmap-service operativo y descubrible
----------------------------------------------------------------------------------

* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: equipo de desarrollo del G10 (roadmap)
*   **Quiero**: que el microservicio arranque en el puerto del diagrama de redes, se registre en Eureka, se anuncie en el mesh del Gateway y deje rastro de cada request
*   **Para**: que el resto de las historias del sprint tengan dónde correr y que las operaciones que cruzan microservicios se puedan seguir de punta a punta

* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: no hay reglas de negocio propias. Es una historia de plataforma: habilita las demás y no entrega valor al alumno ni al profesor por sí sola.
*   [ ] Validaciones: el arranque falla si una migración de Flyway falla. La sonda de Eureka es la de readiness: OUT_OF_SERVICE hasta que el contexto y Flyway estén listos.
*   [ ] Datos obligatorios: variables de entorno EUREKA_URL, SERVER_PORT (default 8010), GATEWAY_URL y las de base (DB_URL, DB_USERNAME, DB_PASSWORD).
*   [ ] Performance (tiempos, volumen, límites): endpoints de actuator baratos (solo health, info, prometheus); Eureka consulta /actuator/health/readiness.
*   [ ] Seguridad (roles, permisos, datos sensibles): el microservicio no valida el JWT; la identidad llega en los headers que inyecta el Gateway. Las credenciales del token técnico se inyectan desde el entorno y nunca se versionan.
*   [ ] Accesibilidad (WCAG/teclado/lectores): no aplica. La historia no tiene interfaz de usuario.
*   [ ] Otros: nombre en Eureka = roadmap-service, ruteo del Gateway /api/roadmap/**. Toda llamada saliente va por el Gateway, nunca micro a micro directo. Trazabilidad: HT onboarding plataforma. Dependencias: equipo del Gateway (G12) para rutas y prefijo /api. Riesgo: divergencia de contrato con el Gateway; mitigación, filtro de headers + tests.

* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: el servicio escucha en el puerto 8010 y se anuncia como roadmap-service.
*   [ ] **CA2**: se registra en Eureka con healthcheck habilitado y la sonda de readiness en verde.
*   [ ] **CA3**: GET /api/roadmap/public/ping responde a través del Gateway.
*   [ ] **CA4**: si una migración de Flyway falla, el servicio no arranca.
*   [ ] **CA5**: verify.sh del mesh (.tpi/platform) corre en verde incluyendo las rutas del Gateway.
*   [ ] **CA6**: las credenciales del token técnico no están versionadas (solo entorno/secret manager).

* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** el microservicio roadmap arranca, es descubrible y responde por el Gateway

**Escenario 1**

*   **Dado**: el servicio arrancó correctamente y se registró en Eureka
*   **Cuando**: el Gateway rutea GET /api/roadmap/public/ping
*   **Entonces**: responde 200

**Escenario 2**

*   **Dado**: que existe una migración de Flyway con SQL inválido
*   **Cuando**: se intenta arrancar el servicio
*   **Entonces**: el arranque falla y el servicio no queda escuchando

**Escenario 3**

*   **Dado**: el contexto de Spring aún no está listo
*   **Cuando**: Eureka consulta /actuator/health/readiness
*   **Entonces**: responde OUT_OF_SERVICE y no recibe tráfico

* * *
Prototipo
---------

*   **Capturas**: no aplica, la historia no tiene interfaz de usuario.
*   **URL Figma**: no aplica.
*   **Storybook**: no aplica.
*   **Mock API / Swagger**: GET /api/roadmap/public/ping. El contrato OpenAPI se publica en docs/api_doc/swagger.json.

## Tareas

- [x] #3573 Onboarding roadmap-service al mesh del Gateway (Eureka + rutas + verify.sh) · Closed · Mateo Delgado Costa
