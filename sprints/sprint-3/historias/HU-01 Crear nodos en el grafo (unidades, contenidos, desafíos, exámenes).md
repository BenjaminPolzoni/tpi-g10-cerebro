---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-01
estado: Propuesta
responsable: ""
epica: "Deuda del Sprint 2"
sprint: "G10 - Sprint 3"
puntos: 3
prioridad: Should
en_taiga: true
---

# HU-01: Crear nodos en el grafo (unidades, contenidos, desafíos, exámenes)

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Deuda del Sprint 2|Deuda del Sprint 2]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Ya existe en Taiga: [[taiga/historias/HU-01 Crear nodos en el grafo (unidades, contenidos, desafíos, exámenes)|HU-01]] (épica EP-56). En el Sprint 3 se **reabre** con lo que falta.

[G10] — HU-01 — Crear nodos en el grafo (unidades, contenidos, desafíos, exámenes)
----------------------------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: enterarme cuando el Motor da de baja el desafío de un nodo
*   **Para**: reemplazarlo antes de que un alumno choque con un desafío inexistente

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: CA8 de HU-01: al recibir la baja de un desafío del Motor, el nodo queda marcado como «desafío no disponible». No se borra el nodo ni el progreso.
*   [ ] Validaciones: El evento se procesa de forma idempotente.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): No aplica.
*   [ ] Otros: Lo demás de HU-01 está hecho; las posiciones del grafo (`moveNode` 501) van en HU-62.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Se consume el evento de baja de desafío del Motor.
*   [ ] **CA2**: El nodo queda marcado y el profesor lo ve en el editor.
*   [ ] **CA3**: El gate responde con un motivo claro para ese nodo.
*   [ ] **CA4**: Test con el evento repetido.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Baja de desafío del Motor

**Escenario 1**  

*   **Dado**: un nodo con un desafío
*   **Cuando**: el Motor publica la baja del desafío
*   **Entonces**: el nodo queda marcado como «desafío no disponible»

**Escenario 2**  

*   **Dado**: el mismo evento
*   **Cuando**: llega dos veces
*   **Entonces**: el nodo queda marcado una sola vez

**Escenario 3**  

*   **Dado**: un nodo marcado
*   **Cuando**: un alumno intenta entrar
*   **Entonces**: el gate responde con el motivo

* * *

Prototipo
---------

*   **Capturas**: No aplica (sin pantalla).
*   **URL Figma**: No aplica.
*   **Storybook**: No aplica.
*   **Mock API / Swagger**: No aplica.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 3
*   **Prioridad (MoSCoW / Numérica)**: Should

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 3 | Should |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Motor.
*   Módulos afectados: Listener de eventos del Motor, entidad de nodo, editor.
*   Otros equipos / aprobaciones: G09 (evento de baja).
*   Impacto en datos / migraciones: Columna o estado del nodo.
*   Riesgos y mitigación (opcional): Que G09 no publique el evento; mitigación: confirmar el contrato.

## Tareas

- [ ] T-01.9 Consumir la baja de desafío
- [ ] T-01.10 Marca en el nodo y en el editor
- [ ] T-01.11 Tests

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

No se consume la baja de desafío del Motor (CA8). El resto de HU-01 está hecho.

### Depende de

Nada: se puede empezar ya.

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|G8]] Sí: `node_id` único global, también después de clonar.
