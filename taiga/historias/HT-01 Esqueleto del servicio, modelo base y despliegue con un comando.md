---
tags: [tpi, g10, taiga, ht]
codigo: HT-01
ref: 552
estado: "Done"
responsable: "Lautaro Jesus Diego"
epica: "[G10] — Esqueleto del servicio Roadmap — TRANSVERSAL (v3)"
sprint: "G10 - Sprint 1"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/552
---

# HT-01: Esqueleto del servicio, modelo base y despliegue con un comando

> [!info] Generado desde Taiga (2026-10-14 18:46). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/552) · Estado: **Done** · Responsable: **Lautaro Jesus Diego** · Sprint: **G10 - Sprint 1**

[G10] — HT-01 — Esqueleto del servicio, modelo base y despliegue con un comando
-------------------------------------------------------------------------------

* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: una base común del servicio —repositorio, modelo de grafo, pipeline, despliegue, Eureka, configuración externa, frontend base y consumer del bus— desde el día uno
*   **Para**: que el resto del sprint se construya sobre un stack que levanta con un comando, sin que su costo se reparta y distorsione las estimaciones del Sprint 2

* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Toda entidad nace con clave curso-cohorte y baja lógica (DoD nivel 1, RF-NFR-01). Un nodo tiene exactamente un tipo: UNIDAD, CONTENIDO, DESAFIO o EXAMEN. Sin llamadas directas entre microservicios: todo por API Gateway. Registro en Eureka como roadmap-service con prefijo /api/roadmap/**.
*   [ ] Validaciones: El pipeline corre build y tests en cada PR y bloquea el merge; prohibido el automerge. Los PR usan plantilla con checklist de DoD nivel 1.
*   [ ] Datos obligatorios: Parámetros propios (por ejemplo PAR-13, tope de reintentos) desde configuración externa desde el día uno, nunca como constantes. El XP, las vidas y PAR-01/02/04/05/08/09/12 los administran Motor, Accounting, Inventario y Backoffice.
*   [ ] Performance (tiempos, volumen, límites): El stack completo (app y base) levanta desde cero con un comando; /actuator/health/liveness y /actuator/health/readiness responden.
*   [ ] Seguridad (roles, permisos, datos sensibles): Identidad por headers del Gateway (X-User-Id, X-User-Roles con ADMIN/MANAGER/PROFESSOR/STUDENT/MS); ownership del curso validado contra Courses. Las llamadas salientes usan token técnico, nunca el JWT de una persona.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Sin pantalla propia; el scaffolding deja el layout y el ruteo listos.
*   [ ] Otros: Convención de ramas feat/T10-(tarjeta)-(slug). Ninguna persona percibe esta tarjeta: falla la V de INVEST a propósito, y se carga con puntos propios porque la DoD nivel 3 exige main con stack completo en un comando. Trazabilidad: DoD niveles 1 y 3, RF-NFR-01. Dependencias: Gateway, Eureka, Courses (ownership) y Backoffice (parámetros); bloquea al resto del sprint. Datos: migraciones iniciales de unidad, nodo y arista sobre base nueva. Riesgo: si se atrasa frena el sprint; mitigación, T-01.1 a T-01.4 los primeros días mientras el resto avanza con dominio y tests. El pipeline CI ya existe en el repo (verify.yml): esta historia no lo construye.

* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: docker compose up en un clon limpio levanta app y base y responde salud sin pasos manuales.
*   [ ] **CA2**: Un PR que rompe un test no se puede mergear.
*   [ ] **CA3**: El modelo admite los cuatro tipos de nodo con curso-cohorte y baja lógica.
*   [ ] **CA4**: Swagger queda publicado aunque esté vacío y el servicio figura en Eureka como roadmap-service con liveness y readiness.

* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Base del servicio y despliegue con un comando

**Escenario 1**  

*   **Dado**: clon limpio con Docker
*   **Cuando**: ejecuto docker compose up
*   **Entonces**: la app y la base levantan y la salud responde

**Escenario 2**  

*   **Dado**: un PR con un test que falla
*   **Cuando**: corre el pipeline
*   **Entonces**: falla y el merge queda bloqueado

**Escenario 3**  

*   **Dado**: el servicio levantado
*   **Cuando**: consulto Eureka y readiness
*   **Entonces**: figura roadmap-service y readiness está listo

* * *
Prototipo
---------

*   **Capturas**: No aplica: historia técnica sin pantalla propia.
*   **URL Figma**: No aplica.
*   **Storybook**: Pendiente: el scaffolding de frontend (T-01.9) deja layout y ruteo; los componentes se documentan al publicarse.
*   **Mock API / Swagger**: Swagger esqueleto publicado por springdoc; GET /actuator/health/liveness y GET /actuator/health/readiness.


## Tareas

- [x] #1675 T-01.1 — Inicializar repositorio, estructura y convención de ramas · Closed · Benjamin Polzoni
- [x] #1676 T-01.2 — Modelo base del grafo con curso-cohorte y baja lógica · Closed · Mateo Delgado Costa
- [x] #1677 T-01.3 — Migraciones iniciales de base de datos · Closed · Mateo Delgado Costa
- [x] #1678 T-01.4 — docker-compose app y base con un comando desde cero · Closed · Baltasar Rodriguez Teruel
- [x] #1680 T-01.6 — Parámetros propios desde configuración externa · Closed · Ludmila Mailen Cejas
- [x] #1681 T-01.7 — Registro Eureka, prefijo, headers y token técnico · Closed · Baltasar Rodriguez Teruel
- [x] #1682 T-01.8 — Esqueleto OpenAPI/Swagger publicado · Closed · Baltasar Rodriguez Teruel
- [x] #1683 T-01.9 — Scaffolding frontend: proyecto, ruteo, layout, gateway · Closed · Lautaro Jesus Diego
- [x] #1684 T-01.10 — Plantilla de PR con checklist DoD nivel 1 · Closed · Ludmila Mailen Cejas
- [x] #1685 T-01.11 — Endpoints liveness y readiness · Closed · Gabriela Camacho
- [x] #1686 T-01.12.1 — Configuración Kafka (spring-kafka) del consumer · Closed · Lorenzo Araujo
- [x] #1687 T-01.12.2 — Clases Event del contrato del bus (PDF) · Closed · Lorenzo Araujo
- [x] #1688 T-01.12.3 — Parseo y validación del evento (KafkaListener tipado) · Closed · Lorenzo Araujo
- [x] #1763 T-01.12.5 — Outbox con reintentos y DLQ para eventos propios · Closed · Benjamin Polzoni
- [x] #2073 T-01.12.4 — Registro de progreso desde el evento · Closed · Benjamin Polzoni
- [x] #2853 T-01.13 — Wiki: DER del modelo del Sprint 1 · Closed · Franco Maximiliano Amarilla
- [x] #2854 T-01.14 — Wiki: diagrama de clases del dominio · Closed · Franco Maximiliano Amarilla
