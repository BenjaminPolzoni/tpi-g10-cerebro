---
tags: [tpi, g10, taiga, ht]
codigo: HT-09
ref: 4251
estado: "Done"
responsable: "Stefano Zoffoli"
epicas: "[[epicas/EP-144 Esqueleto del servicio Roadmap — TRANSVERSAL (v3)|EP-144]]"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4251
---

# HT-09: Eliminar simulaciones y datos de ejemplo del microservicio

> [!info] Generado desde Taiga (2026-10-15 16:54). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4251) · Estado: **Done** · Responsable: **Stefano Zoffoli** · Sprint: **G10 - Sprint 2**
> Épica: [[epicas/EP-144 Esqueleto del servicio Roadmap — TRANSVERSAL (v3)|EP-144]] · Tareas cerradas: **7/7**

[G10] — HT-09 — Eliminar simulaciones y datos de ejemplo del microservicio
-------------------------------------------------------------------------

* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: relevar y retirar los mocks, stubs y datos de ejemplo del microservicio, dejando cada cliente en modo real por defecto
*   **Para**: que en un entorno integrado las fallas de integración se vean y no queden ocultas por datos simulados

* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: 1) Se relevan todos los mocks, stubs y datos de ejemplo y cada uno se clasifica: eliminar, mover a tests o mantener solo en local/demo. 2) El modo por defecto de cada cliente pasa a real; el stub solo por perfil explícito de test o local. 3) Si una integración real está bloqueada por otro grupo, no se reemplaza con datos silenciosos: error explícito o degradación documentada, nunca "habilitado" por defecto. 4) La semilla de HT-02 se conserva solo en local/demo. Justificación técnica: ningún actor final la percibe (falla la V de INVEST a propósito). En el Sprint 1 se dejaron dobles para avanzar sin bloqueo y, en un entorno real, eso oculta fallas: es lo que pasó con HT-06, que quedó Done sin cumplir su Escenario 1.
*   [ ] Validaciones: La configuración se valida al arrancar (como T-01.6): en el perfil integrado no levanta con ningún cliente en modo stub.
*   [ ] Datos obligatorios: Inventario de dobles con la decisión por ítem (eliminar, mover a tests o mantener en local/demo).
*   [ ] Performance (tiempos, volumen, límites): Sin impacto.
*   [ ] Seguridad (roles, permisos, datos sensibles): Sin cambios; llamadas con token técnico por el Gateway.
*   [ ] Accesibilidad (WCAG/teclado/lectores): No aplica.
*   [ ] Otros: Dobles relevados el 30/09 (backend): InMemoryInventoryClient (INVENTORY_CLIENT_MODE=stub por defecto); InMemoryCoursesCatalogClient (COURSES_CATALOG_MODE=stub por defecto, sin consumidores); PendingCourseSectionsClient (COURSES_SECTIONS_CLIENT_MODE=stub por defecto); PendingCohortOwnershipClient y PendingMotorCatalogClient (stub opcional, por defecto http); RoadmapSimulationService con DEFAULT_UNITS y fallbackPool() de 4 desafíos falsos, con init-mvp y auto-init-on-get detrás de SIMULATION_ENABLED=false; perfil demo (DemoDataSeeder, DemoData, DemoCohortOwnershipClient) ya aislado con el perfil demo; flags stub-unavailable de Courses e Inventario. Cada mock se retira cuando su integración real pasa la prueba e2e, no antes. Si Courses no habilita el token técnico a tiempo rige el plan B (doble solo en tests, flag unidades-desde-courses apagado). Alcance sobre el front sin definir (P-18): hay dobles del front (InMemoryRoadmapAdapter, seed.ts, InMemoryBadgesAdapter, InMemoryBankAdapter, ranking.seed.ts, materials-page y la tienda local). Dependencias: HT-07 y HU-36 (Courses), HU-16 (Inventario), HU-40 (ítems). Riesgo: retirar un mock antes de que el real esté habilitado frena el desarrollo; mitigación: orden por integración y plan B.

* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Inventario de mocks, stubs y datos de ejemplo publicado en la Wiki, con la decisión por ítem.
*   [ ] **CA2**: En el perfil integrado no hay ningún cliente en modo stub.
*   [ ] **CA3**: Arrancar el perfil integrado con un cliente en stub falla con un mensaje claro.
*   [ ] **CA4**: init-mvp no genera unidades por defecto sin avisar (alineado con HT-07, CA3).
*   [ ] **CA5**: Los dobles quedan solo en el perfil de test y los tests siguen pasando.
*   [ ] **CA6**: Prueba e2e contra los servicios reales con capturas (repite T-06.7 con el criterio corregido).

* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Microservicio sin simulaciones en el perfil integrado

**Escenario 1**  

*   **Dado**: el perfil integrado con COURSES_SECTIONS_CLIENT_MODE=stub
*   **Cuando**: arranca el servicio
*   **Entonces**: falla con un error claro de configuración

**Escenario 2**  

*   **Dado**: Courses rechaza el token técnico
*   **Cuando**: se ejecuta init-mvp
*   **Entonces**: error explícito "token rechazado" y no se crea un roadmap por defecto

**Escenario 3**  

*   **Dado**: el perfil local
*   **Cuando**: corre la semilla de demo
*   **Entonces**: los datos de ejemplo existen solo en ese perfil

* * *
Prototipo
---------

*   **Capturas**: No aplica: historia técnica sin pantalla. Evidencia: inventario en la Wiki, configuración por perfil y capturas e2e.
*   **URL Figma**: No aplica.
*   **Storybook**: No aplica.
*   **Mock API / Swagger**: No aplica.


## Tareas

- [x] #4341 T-09.1 Publicar el inventario de dobles ya relevado · Closed · Franco Maximiliano Amarilla
- [x] #4343 T-09.2 Modos por defecto a real y validación al arrancar · Closed · Stefano Zoffoli
- [x] #4347 T-09.3 Mover los dobles al perfil de test · Closed · Stefano Zoffoli
- [x] #4353 T-09.4 Quitar las unidades por defecto de init-mvp (con HU-36) · Closed · Stefano Zoffoli
- [x] #4354 T-09.5 Quitar el mock de ítems (con HU-40) y de vidas (con HU-16) · Closed · Stefano Zoffoli
- [x] #4355 T-09.6 e2e y capturas · Closed · Stefano Zoffoli
- [x] #5408 T-09.7 Wiki, OpenAPI y diagrama de secuencia · Closed · Franco Maximiliano Amarilla
