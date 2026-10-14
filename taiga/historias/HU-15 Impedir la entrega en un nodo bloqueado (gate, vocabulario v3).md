---
tags: [tpi, g10, taiga, hu]
codigo: HU-15
ref: 741
estado: "Done"
responsable: "Baltasar Rodriguez Teruel"
epicas: "[[epicas/EP-60 Progreso y desbloqueo|EP-60]]"
sprint: "G10 - Sprint 1"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/741
---

# HU-15: Impedir la entrega en un nodo bloqueado (gate, vocabulario v3)

> [!info] Generado desde Taiga (2026-10-14 20:44). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/741) · Estado: **Done** · Responsable: **Baltasar Rodriguez Teruel** · Sprint: **G10 - Sprint 1**
> Épica: [[epicas/EP-60 Progreso y desbloqueo|EP-60]] · Tareas cerradas: **8/8**

[G10] — HU-15 — Impedir la entrega en un nodo bloqueado (gate, vocabulario v3)
------------------------------------------------------------------------------

* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: SISTEMA CONSUMIDO POR MOTOR, PRÁCTICOS Y TEÓRICOS
*   **Quiero**: un gate síncrono que devuelva un motivo claro cuando el alumno no puede entregar
*   **Para**: que ningún equipo de desafíos acepte entregas en nodos que el alumno todavía no desbloqueó

* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Evalúa en orden, con el vocabulario v3 acordado como breaking change con Grupo 09: no_inscripto, contenido_no_leido (HU-11), prerrequisito_pendiente (HU-13 y D-01) y sin_vidas, leído a Inventario, con la excepción del desafío de recuperación (RF-REC-04) y de los desafíos LLM. Degradación: si un origen externo no responde, devuelve habilitado en false con motivo origen_no_disponible, extensión pendiente de acuerdo con G09 (F5). Es bloqueante, no un aviso. Los desbloqueos alcanzados no se revierten (RF-CFG-06).
*   [ ] Validaciones: El nodo y el alumno tienen que ser del mismo curso-cohorte, y la respuesta es idempotente: la misma consulta devuelve el mismo motivo.
*   [ ] Datos obligatorios: Curso-cohorte, alumno y nodo.
*   [ ] Performance (tiempos, volumen, límites): P95 por debajo de 200 ms con 120 consultas concurrentes (RF-NFR-03).
*   [ ] Seguridad (roles, permisos, datos sensibles): Token técnico por equipo consumidor; el alumno ve la existencia y la condición, nunca el contenido bloqueado.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Sin pantalla propia: el mensaje lo dibuja cada consumidor a partir del motivo entregado.
*   [ ] Otros: Usa el cliente de Inventario con caché de HT-03 y un kill-switch de operación que fuerza no habilitado si el contrato se rompe. Trazabilidad: RF-CFG-06, RF-REC-04, RF-NFR-03, REQ-MOT-01 (consumeVida), D-07. Dependencias: Inventario (vidas e ítems), los tres equipos consumidores y el Gateway; el contrato se firma con los tres equipos en el acta del día 5, incluyendo el breaking change de G09 y la extensión origen_no_disponible. Datos: lee el grafo, las lecturas y los clientes externos. Riesgo: degradación en producción; mitigación, motivo explícito, tests y kill-switch.

* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Un alumno sin la lectura obligatoria recibe contenido_no_leido.
*   [ ] **CA2**: Un alumno sin el prerrequisito recibe prerrequisito_pendiente.
*   [ ] **CA3**: Un alumno fuera del curso recibe no_inscripto.
*   [ ] **CA4**: Un alumno con 0 vidas recibe sin_vidas, salvo que se trate de recuperación o de un desafío LLM.
*   [ ] **CA5**: Si un origen externo no responde, devuelve habilitado en false con motivo origen_no_disponible, pendiente de acuerdo con G09.

* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Gate de habilitación con vocabulario v3

**Escenario 1**  

*   **Dado**: un contenido obligatorio sin leer
*   **Cuando**: un equipo de desafíos consulta el gate
*   **Entonces**: responde contenido_no_leido

**Escenario 2**  

*   **Dado**: el contenido leído pero un prerrequisito pendiente
*   **Cuando**: se consulta el gate
*   **Entonces**: responde prerrequisito_pendiente

**Escenario 3**  

*   **Dado**: un alumno con 0 vidas en Inventario
*   **Cuando**: se consulta el gate para un desafío de recuperación
*   **Entonces**: no responde sin_vidas, por la excepción de RF-REC-04

**Escenario 4**  

*   **Dado**: Inventario que no responde
*   **Cuando**: se consulta el gate
*   **Entonces**: responde habilitado en false con motivo origen_no_disponible, nunca habilitado por defecto

**Escenario 5**  

*   **Dado**: un alumno fuera del curso
*   **Cuando**: se consulta el gate
*   **Entonces**: responde no_inscripto

* * *
Prototipo
---------

*   **Capturas**: No aplica: el gate no tiene pantalla propia.
*   **URL Figma**: No aplica.
*   **Storybook**: No aplica.
*   **Mock API / Swagger**: GET /api/roadmap/gate con contrato versionado publicado en OpenAPI y acordado con los tres equipos consumidores.


## Tareas

- [x] #1292 T-15.1 — Endpoint de gate con vocabulario v3 versionado · Closed · Baltasar Rodriguez Teruel
- [x] #1293 T-15.2 — Integración con Inventario (caché y degradación) y lectura del ledger · Closed · Baltasar Rodriguez Teruel
- [x] #1294 T-15.3 — Evaluación de contenido_no_leido y prerrequisito_pendiente · Closed · Fenoglio Santino
- [x] #1295 T-15.4 — Evaluación de no_inscripto, sin_vidas y recuperación · Closed · Iker Alonso
- [x] #1297 T-15.5 — Acta y publicación OpenAPI del contrato · Closed · Baltasar Rodriguez Teruel
- [x] #1298 T-15.6 — Tests BDD y carga P95 con 120 concurrentes · Closed · Baltasar Rodriguez Teruel
- [x] #2890 T-15.7 — Wiki: BPMN del gate · Closed · Quinteros Tomás
- [x] #2891 T-15.8 — Wiki: secuencia del gate · Closed · Quinteros Tomás
