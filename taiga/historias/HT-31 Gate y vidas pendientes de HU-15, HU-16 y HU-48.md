---
tags: [tpi, g10, taiga, ht]
codigo: HT-31
ref: 9270
estado: "New"
responsable: "Sin asignar"
epicas: "[[epicas/EP-8632 Deuda del Sprint 2|EP-8632]]"
sprint: "G10 - Sprint 03"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/9270
---

# HT-31: Gate y vidas pendientes de HU-15, HU-16 y HU-48

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/9270) · Estado: **New** · Responsable: **Sin asignar** · Sprint: **G10 - Sprint 03**
> Épica: [[epicas/EP-8632 Deuda del Sprint 2|EP-8632]] · Tareas cerradas: **0/7**

[G10] — HT-31 — Gate y vidas pendientes de HU-15, HU-16 y HU-48
---------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: que el gate responda con un motivo cuando un origen no responde, que las vidas muestren el último dato conocido y que el alumno pueda consultar su elegibilidad
*   **Para**: cumplir lo que les falta a HU-15, HU-16 y HU-48 sin reabrirlas

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Cada tarea lleva el código de la HU original y el CA que cierra; al terminarla se deja un comentario en la HU original de Taiga. Gate fail-closed (DEC-003): nunca habilita con un dato viejo o faltante.
*   [ ] Validaciones: Cada CA cerrado tiene su test.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): El gate no supera el P95 de 200 ms (la medición está en HT-20).
*   [ ] Seguridad (roles, permisos, datos sensibles): El pre-chequeo de HU-48 usa el JWT del alumno y solo responde por él.
*   [ ] Accesibilidad (WCAG/teclado/lectores): El motivo `origen_no_disponible` y el aviso de dato desactualizado se muestran en texto.
*   [ ] Otros: Pasar de 503 a 200 con motivo cambia el contrato del gate con G09.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1** (HU-15 CA5): Con Accounting o Courses caídos y sin caché vigente, el gate responde `eligible=false` con `origen_no_disponible` (no 503), el front lo muestra y el acta del gate queda actualizada con G09.
*   [ ] **CA2** (HU-16 CA3): La pantalla de inventario muestra el último dato de vidas con aviso durante 24 h si Accounting no responde, y el gate nunca habilita con un dato `stale`.
*   [ ] **CA3** (HU-48 CA1 a CA3): El alumno consulta la elegibilidad con su JWT, recibe el mismo motivo que el gate y el front usa ese endpoint en vez del del Motor.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Gate y vidas

**Escenario 1** (HU-15)

*   **Dado**: Accounting caído y sin caché vigente
*   **Cuando**: el Motor consulta el gate por un alumno
*   **Entonces**: recibe `eligible=false` con `origen_no_disponible`, no un 503

**Escenario 2** (HU-16)

*   **Dado**: Accounting caído y un dato de vidas de hace 3 horas
*   **Cuando**: el alumno abre el inventario y el Motor consulta el gate
*   **Entonces**: el alumno ve el dato con el aviso de desactualizado y el gate no habilita

**Escenario 3** (HU-48)

*   **Dado**: un alumno sin la lectura obligatoria de un nodo
*   **Cuando**: elige el desafío de ese nodo
*   **Entonces**: ve «contenido no leído» y no se llama al Motor

* * *

Prototipo
---------

*   **Capturas**: Inventario con dato desactualizado; motivo de bloqueo del desafío.
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-callout`.
*   **Mock API / Swagger**: GET /api/roadmap/courses/{courseId}/nodes/{nodeId}/eligibility (alumno, HU-48).

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 8
*   **Prioridad (MoSCoW / Numérica)**: Must · 1 (máxima del sprint)

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 8 | Must · 1 (máxima del sprint) |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Accounting (vidas), Courses, Motor (contrato del gate), API Gateway (JWT del alumno).
*   Módulos afectados: `GateService`, `GateEvaluator`, `InventoryClient`, `InventoryService`, `SecurityConfig`, inventario y `challenge-attempt.service` del front.
*   Otros equipos / aprobaciones: G09 (acta del gate, bloqueante para mergear T-31.1).
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Que G09 no apruebe el cambio de contrato a tiempo; mitigación: mandar el acta la semana 1.


## Tareas

- [ ] #9287 T-31.1 HU-15 CA5 · El gate responde origen_no_disponible en vez de 503 · New · Gabriela Camacho
- [ ] #9288 T-31.2 HU-15 CA5 · Acordar el cambio con el Motor y mostrar el motivo · New · Gabriela Camacho
- [ ] #9289 T-31.3 HU-16 CA3 · Mostrar el último dato de vidas con aviso durante 24 h · New · Gabriela Camacho
- [ ] #9290 T-31.4 HU-16 CA3 · El gate nunca habilita con un dato viejo · New · Gabriela Camacho
- [ ] #9291 T-31.5 HU-48 CA1 · Endpoint para que el alumno pregunte si puede entrar a un desafío · New · Gabriela Camacho
- [ ] #9292 T-31.6 HU-48 CA1 · Que el front pregunte con el endpoint del alumno · New · Gabriela Camacho
- [ ] #9342 T-31.7 Wiki, OpenAPI y diagrama de secuencia · New · Quinteros Tomás
