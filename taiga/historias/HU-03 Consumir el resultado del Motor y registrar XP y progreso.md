---
tags: [tpi, g10, taiga, hu]
codigo: HU-03
ref: 942
estado: "Done"
responsable: "Benjamin Polzoni"
epica: "[G10] — Progreso y desbloqueo"
sprint: "G10 - Sprint 1"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/942
---

# HU-03: Consumir el resultado del Motor y registrar XP y progreso

> [!info] Generado desde Taiga (2026-10-14 18:46). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/942) · Estado: **Done** · Responsable: **Benjamin Polzoni** · Sprint: **G10 - Sprint 1**

[G10] — HU-03 — Consumir el resultado del Motor y registrar XP y progreso
-------------------------------------------------------------------------

* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: SISTEMA
*   **Quiero**: consumir el evento de resultado del Motor con el XP ya calculado y sumarlo al ledger junto con el nodo completado y los desbloqueos, de forma idempotente
*   **Para**: que el progreso refleje cada desafío sin duplicar ni recalcular: el Motor calcula, Roadmap persiste y Accounting no sabe nada de XP

* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Roadmap NO calcula ni emite XP: el Motor envía xpOtorgado ya calculado, con el bonus de ítem si aplica, y nosotros lo sumamos a xp_movement. Con esRepeticion igual a true el evento se descarta conservando la primera solución (REQ-MOT-03). La idempotencia es por eventId: el duplicado que llega por replay con earliest es no-op. Los ajustes posteriores (REQ-MOT-04) generan un movimiento nuevo, nunca una edición (RF-CFG-06); si el ajuste viaja como delta o como total queda pendiente de acuerdo con Grupo 09. El envelope sigue el PDF del bus: eventId, eventType SNAKE en inglés, timestamp UTC del hecho, producer y payload tipado, sin eventVersion por decisión D-KAFKA.
*   [ ] Validaciones: El envelope trae los cinco campos obligatorios; el alumno está matriculado en el curso-cohorte; el nodeId y el challengeId son del curso; los eventTypes desconocidos se registran y no se interpretan; si viene aprobado se evalúa completed_node y los desbloqueos.
*   [ ] Datos obligatorios: Curso-cohorte, alumno, desafío, xp, motivo, eventId y timestamp del hecho.
*   [ ] Performance (tiempos, volumen, límites): Procesamiento en menos de 200 ms dentro del listener, con picos de 120 eventos concurrentes.
*   [ ] Seguridad (roles, permisos, datos sensibles): Se consume con el token técnico del servicio, nunca con credenciales del alumno. El payload es el mínimo necesario: prohibido el por si acaso.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Sin pantalla propia.
*   [ ] Otros: Es el único punto de entrada de XP al ledger propio. Los eventos propios (NODE_COMPLETED, NODE_UNLOCKED, en SNAKE inglés según el PDF) salen por outbox (T-01.12.5). No se emite xp.otorgado porque nadie lo consume (F1). Trazabilidad: REQ-MOT-02, REQ-MOT-03, REQ-MOT-04, RF-CFG-06, RF-NFR-01. Dependencias: Motor (evento y contrato REQ-MOT-02), bus Kafka y Gateway; el Motor publica contrato y garantías en el acta del día 3 y Notificaciones confirma topic y DLQ (P-09). Datos: xp_movement append-only con event_id único, más completed_node. Riesgo: duplicados por replay con earliest; mitigación, clave única por eventId en base, consumer idempotente y tests de replay.

* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Un CHALLENGE_COMPLETED válido suma el XP, marca el nodo completado y evalúa los desbloqueos.
*   [ ] **CA2**: Un evento con esRepeticion se descarta sin cambios.
*   [ ] **CA3**: El mismo eventId dos veces no produce doble registro.
*   [ ] **CA4**: Un alumno o desafío inválido, o un evento malformado, se rechaza con log y sin registro.

* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Registro del resultado publicado por el Motor de Desafíos

**Escenario 1**  

*   **Dado**: un CHALLENGE_COMPLETED aprobado con el xp ya calculado por el Motor
*   **Cuando**: llega el evento al topic que confirme Notificaciones
*   **Entonces**: se suma al ledger, se marca el nodo y se evalúan los desbloqueos

**Escenario 2**  

*   **Dado**: el mismo eventId llega dos veces por un replay
*   **Cuando**: se procesa el duplicado
*   **Entonces**: la clave única lo frena y no se duplica nada

**Escenario 3**  

*   **Dado**: un evento con esRepeticion igual a true
*   **Cuando**: llega el evento
*   **Entonces**: se descarta conservando la primera solución

**Escenario 4**  

*   **Dado**: un alumno no matriculado en el curso-cohorte
*   **Cuando**: llega el evento
*   **Entonces**: se rechaza con log y sin registro

* * *
Prototipo
---------

*   **Capturas**: No aplica: la historia no tiene pantalla propia.
*   **URL Figma**: No aplica.
*   **Storybook**: No aplica.
*   **Mock API / Swagger**: Listener de CHALLENGE_COMPLETED con Event tipado, más endpoint de depuración GET /api/roadmap/historial-xp habilitado solo fuera de producción.


## Tareas

- [x] #1149 T-03.1 — Listener del evento de resultado del Motor · Closed · Benjamin Polzoni
- [x] #1151 T-03.3 — Suma al ledger con idempotencia y desbloqueos · Closed · Benjamin Polzoni
- [x] #1156 T-03.4 — Endpoint de depuración de historial (solo fuera de producción) · Closed · Benjamin Polzoni
- [x] #1159 T-03.5 — Tests de escenarios BDD · Closed · Benjamin Polzoni
- [x] #2082 T-03.2 — Schema del evento consumido (contrato PDF del bus) · Closed · Benjamin Polzoni
