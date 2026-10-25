---
tags: [tpi, g10, sprint-3, ht]
codigo: HT-31
estado: New
responsable: "Sin asignar"
epica: "Deuda del Sprint 2"
sprint: "G10 - Sprint 3"
puntos: 8
prioridad: Must
prioridad_sprint: 1
en_taiga: true
ref: 9270
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/9270
responsables_tareas: ["Gabriela Camacho", "Quinteros Tomás"]
tareas_cerradas: "6/7"
---

# HT-31: Gate y vidas pendientes de HU-15, HU-16 y HU-48

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Deuda del Sprint 2|Deuda del Sprint 2]] · Estado: **New** · Responsable de la historia: **Sin asignar** · Tareas: **6/7** · Sprint: **G10 - Sprint 3**
> Cargada en Taiga: [[taiga/historias/HT-31 Gate y vidas pendientes de HU-15, HU-16 y HU-48|HT-31]] ([abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/9270)) · Épica en Taiga: [[epicas/EP-8632 Deuda del Sprint 2|EP-8632]] · Responsables de las tareas: [[sprints/sprint-3/12-responsables#Gabriela Camacho|Gabriela Camacho]] (6), [[sprints/sprint-3/12-responsables#Quinteros Tomás|Quinteros Tomás]] (1). Sale de dividir por tema la HT de criterios pendientes (2026-10-15): ver [[sprints/sprint-3/historias/HT-30 Insignias pendientes de HU-20 y HU-21|HT-30]]. Las HU originales quedan en Done en su sprint; cada tarea dice a qué HU y a qué CA corresponde.

> [!important] Prioridad 1 del sprint (2026-10-15)
> Va después de las insignias (HT-30). Son criterios que ya se dieron por terminados y no se cumplen.

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

> [!info] Espejo de Taiga (sync 2026-10-15). Cerradas: **0/7**. Historia en Taiga: [[taiga/historias/HT-31 Gate y vidas pendientes de HU-15, HU-16 y HU-48|HT-31]] · [abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/9270)

- [x] [#9287](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9287) **T-31.1 HU-15 CA5 · El gate responde origen_no_disponible en vez de 503** · Back · New · [[sprints/sprint-3/12-responsables#Gabriela Camacho|Gabriela Camacho]]
    - **Qué:** si Accounting o Courses no responden y no hay caché vigente, el gate responde `eligible=false` con `reason=origen_no_disponible` (fail-closed, DEC-003).
    - **Dónde:** `GateService`, `GateEvaluator`, `InventoryClient`, clientes de Courses.
    - **Listo cuando:** hay tests con Accounting caído y con Courses caído, y ninguno devuelve 503.
    - ✅ **Hecha:** `tpi-roadmap#234` (mergeada 2026-10-16), vocabulario en inglés `origin_unavailable` ([[decisiones/DEC-020-gate-origen-no-disponible-en-vez-de-503|DEC-020]]). Tests en `GateControllerTest`, `GateEligibilityBddSteps`.
- [x] [#9288](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9288) **T-31.2 HU-15 CA5 · Acordar el cambio con el Motor y mostrar el motivo** · Coordinación + Front · New · [[sprints/sprint-3/12-responsables#Gabriela Camacho|Gabriela Camacho]]
    - **Qué:** pasar de 503 a 200 con motivo cambia el contrato: actualizar el acta del gate (`roadmap-motor-gate-v1.md`) con G09 antes de mergear. En el front, agregar el texto del motivo en `roadmapLabels.blockReason`.
    - **Listo cuando:** G09 aprobó el acta y el alumno ve el motivo en palabras.
    - ✅ **Hecha:** acta v1.4 aprobada por G09 el 2026-10-16 ([[contratos/roadmap-motor-gate-v1]]). Front: [FE#624](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/624) (en `develop` del front, `src/app/features/roadmap/ui/labels.ts`: `roadmapLabels.blockReason.origin_unavailable`).
**HU-16 CA3: último dato de vidas si Accounting cae** ([us/4237](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4237))
- [x] [#9289](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9289) **T-31.3 HU-16 CA3 · Mostrar el último dato de vidas con aviso durante 24 h** · Back + Front · New · [[sprints/sprint-3/12-responsables#Gabriela Camacho|Gabriela Camacho]]
    - **Qué:** la pantalla de inventario usa el último dato conocido marcado `stale` con una retención configurable de 24 h; pasado ese tiempo no se muestra. El front avisa que el dato está desactualizado.
    - **Dónde:** `InventoryService`, `InventoryController`, pantalla de inventario.
    - **Listo cuando:** con Accounting caído se ve el último dato con aviso, y a las 24 h deja de verse. Hay test.
    - ✅ **Hecha:** back en `tpi-roadmap#234` (`InventoryServiceTest`, caso T-31.3). Front en `src/app/features/roadmap/ui/inventory-hud/` (`develop` del front, [FE#624](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/624)).
- [x] [#9290](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9290) **T-31.4 HU-16 CA3 · El gate nunca habilita con un dato viejo** · Back · New · [[sprints/sprint-3/12-responsables#Gabriela Camacho|Gabriela Camacho]]
    - **Qué:** `GateService` ignora el dato `stale` de vidas y responde como en T-31.1.
    - **Listo cuando:** hay tests con caché vigente, vencida y sin caché.
    - ✅ **Hecha:** `tpi-roadmap#234`, test `GateStaleLivesTest` (caché vigente, vencida y sin caché).
**HU-48: pre-chequeo con el JWT del alumno** ([us/7206](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/7206))
- [x] [#9291](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9291) **T-31.5 HU-48 CA1 · Endpoint para que el alumno pregunte si puede entrar a un desafío** · Back · New · [[sprints/sprint-3/12-responsables#Gabriela Camacho|Gabriela Camacho]]
    - **Qué:** `GET /api/roadmap/courses/{courseId}/nodes/{nodeId}/eligibility` con el JWT del alumno, que use el mismo `GateService` y vocabulario que el gate del Motor y no cree intentos. Hoy `/eligibility` está reservado a `ServiceIdentity` en `SecurityConfig` y al alumno le da 403. Borrar de paso `ProgressService.startChallenge` (código muerto) y actualizar OpenAPI.
    - **Listo cuando:** un alumno sin la lectura obligatoria recibe `content_not_read`. Hay BDD.
    - ✅ **Hecha:** `tpi-roadmap#234`, `GateController.eligibility(...)` sin `studentId` en el path, resuelto con el id del token. BDD en `GateEligibilityBddSteps`.
- [x] [#9292](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9292) **T-31.6 HU-48 CA1 · Que el front pregunte con el endpoint del alumno** · Front · New · [[sprints/sprint-3/12-responsables#Gabriela Camacho|Gabriela Camacho]]
    - **Qué:** `challenge-attempt.service` llama al endpoint nuevo, muestra el motivo si está bloqueado y, si está habilitado, abre el intento como hoy (con su `attempt_type`).
    - **Listo cuando:** se cumplen los CA1 a CA3 originales de HU-48 de punta a punta.
    - ✅ **Hecha:** `src/app/features/roadmap/data-access/challenge-attempt/challenge-attempt.service.ts` llama a `/roadmap/courses/{courseId}/nodes/{nodeId}/eligibility`, muestra el motivo bloqueado y abre el intento con su `attemptType` si está habilitado (`develop` del front, [FE#624](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/624)).
- [ ] [#9342](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9342) **T-31.7 Wiki, OpenAPI y diagrama de secuencia** · New · [[sprints/sprint-3/12-responsables#Quinteros Tomás|Quinteros Tomás]]
    - Tarea de documentación agregada en Taiga por el equipo; no estaba en la propuesta.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Verificado contra `origin/develop` (back `fc1917e`, front `67cbad4a`) el 2026-10-15.

| HU original | Sprint | CA que falta | Estado hoy |
|---|---|---|---|
| [[taiga/historias/HU-15 Impedir la entrega en un nodo bloqueado (gate, vocabulario v3)\|HU-15]] | 1 | ❌ CA5: `origen_no_disponible` si un origen no responde | Devuelve 503 |
| [[taiga/historias/HU-16 Integración real con Inventario para las vidas del gate\|HU-16]] | 2 | ❌ CA3: último dato conocido si Accounting cae | `lastKnown` solo lo usa la pantalla de inventario |
| [[taiga/historias/HU-48 Saber si puedo entrar a un desafío antes de abrirlo\|HU-48]] | 2 | ❌ CA1 y ⚠️ CA2, CA3 | `/eligibility` está reservada a `ServiceIdentity`: con el JWT del alumno da 403 |

### Depende de

- G09 Motor: aprobar el cambio del acta del gate (solo para mergear T-31.1 y T-31.2).

### Deuda técnica que cierra

- [[deuda-tecnica|DT-04]]

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|E9]] Con Backoffice caído se usan los valores en caché (HU-15).
