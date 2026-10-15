---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-41
estado: Propuesta
responsable: ""
epica: "Deuda del Sprint 2"
sprint: "G10 - Sprint 3"
puntos: 3
prioridad: Must
en_taiga: true
---

# HU-41: CA2 pendiente: reintentos y política de vidas

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Deuda del Sprint 2|Deuda del Sprint 2]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Ya existe en Taiga: [[taiga/historias/HU-41 Editar un nodo del roadmap de forma individual|HU-41]] (épica EP-4232). En el Sprint 3 se **reabre** con lo que falta.

[G10] — HU-41 — Editar un nodo del roadmap de forma individual
--------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: definir cuántos reintentos tiene un desafío y editar un nodo sin perder su configuración
*   **Para**: controlar la dificultad sin sorpresas al guardar

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: `reintentos_permitidos` va de 0 al tope del parámetro PAR-13 de Backoffice. Un PUT que no trae `lives_policy` conserva la actual.
*   [ ] Validaciones: Reintentos fuera de rango: 400.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): ADMIN, GESTOR o PROFESSOR dueño.
*   [ ] Accesibilidad (WCAG/teclado/lectores): No aplica.
*   [ ] Otros: Si HT-18 pasa los nodos a Neo4j, el campo vive ahí.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Campo de reintentos en el nodo, validado contra PAR-13.
*   [ ] **CA2**: Un PUT sin `lives_policy` no resetea el nodo a STANDARD.
*   [ ] **CA3**: El editor de nodo muestra y guarda los reintentos.
*   [ ] **CA4**: Tests de ambos casos.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Edición segura de nodos

**Escenario 1**  

*   **Dado**: un nodo con `lives_policy=RECOVERY`
*   **Cuando**: el profesor hace PUT sin ese campo
*   **Entonces**: el nodo sigue en RECOVERY

**Escenario 2**  

*   **Dado**: PAR-13 = 3
*   **Cuando**: el profesor pone 5 reintentos
*   **Entonces**: recibe 400

**Escenario 3**  

*   **Dado**: PAR-13 = 3
*   **Cuando**: el profesor pone 2 reintentos
*   **Entonces**: se guarda

* * *

Prototipo
---------

*   **Capturas**: Editor de nodo.
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-input` numérico.
*   **Mock API / Swagger**: PUT/PATCH /api/roadmap/nodes/{nodeId}.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 3
*   **Prioridad (MoSCoW / Numérica)**: Must

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 3 | Must |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Backoffice (PAR-13).
*   Módulos afectados: Entidad y servicio de nodos, `GraphController`, editor de nodo.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: Migración: columna de reintentos.
*   Riesgos y mitigación (opcional): Solaparse con HT-18; mitigación: hacerlo antes y migrarlo junto con el grafo.

## Tareas

- [ ] T-41.7 Columna y validación de reintentos
- [ ] T-41.8 Corregir el PUT que resetea `lives_policy`
- [ ] T-41.9 Editor de nodo
- [ ] T-41.10 Tests

---

## Contexto del Sprint 3 (no va a Taiga)

### Criterios de la HU original (Taiga)

Verificados contra `origin/develop` (back `fc1917e`, front `67cbad4a`) el 2026-10-15. ✅ cumple · ❌ no cumple · ⚠️ hecho pero no anda de punta a punta.

- [x] ✅ **CA1**: El profesor abre un nodo y ve sus datos vigentes. — `NodeDetailService`
- [ ] ❌ **CA2**: Al cambiar obligatoriedad, reintentos o reglas, el gate usa el valor nuevo en la próxima consulta. — no existe el campo de reintentos y un PUT sin `lives_policy` vuelve el nodo a STANDARD
- [x] ✅ **CA3**: Una edición que cierra un ciclo se rechaza sin cambios. — 409 por ciclo
- [x] ✅ **CA4**: Un alumno que ya desbloqueó el nodo conserva el desbloqueo tras la edición. — los desbloqueos están en `node_unlock` y la edición no los toca
- [x] ✅ **CA5**: Un profesor que no es dueño recibe 403 sin efectos. — `requireOwner`
- [x] ✅ **CA6**: Cada edición deja un log con autor, fecha, campos y cantidad de alumnos afectados. — `NodeEditLogService` con `affected_students`

### Qué hay hoy en el código

No existe el campo de reintentos. Un PUT sin `lives_policy` resetea el nodo a STANDARD.

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

Ninguna.
