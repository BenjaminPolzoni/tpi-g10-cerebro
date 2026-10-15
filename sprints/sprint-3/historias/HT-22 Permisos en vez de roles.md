---
tags: [tpi, g10, sprint-3, ht]
codigo: HT-22
estado: Propuesta
responsable: ""
epica: "Correcciones de los profes"
sprint: "G10 - Sprint 3"
puntos: 5
prioridad: Should
en_taiga: false
---

# HT-22: Permisos en vez de roles

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Correcciones de los profes|Correcciones de los profes]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga.

[G10] — HT-22 — Permisos en vez de roles
----------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: autorizar por permisos y no por roles, con el catálogo Users (G07)
*   **Para**: que los permisos se configuren desde los parámetros globales sin cambiar código

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Matriz rol → permisos escrita (DT-03) y acordada con G07: el catálogo es de Users, no de Backoffice (G2). Mientras no exista, se usan `PROFESSOR`/`GESTOR` (G6). Los chequeos de dueño del curso se mantienen.
*   [ ] Validaciones: No aplica.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): Cada `@PreAuthorize` usa `hasAuthority('roadmap.…')`. El gate valida el scope `roadmap.gate.read` (DT-01).
*   [ ] Accesibilidad (WCAG/teclado/lectores): No aplica.
*   [ ] Otros: Las reglas ya están en constantes por controller (`CAN_EDIT`, `CAN_VIEW`…): en gran parte es reemplazarlas.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Matriz rol → permisos escrita y acordada con G07.
*   [ ] **CA2**: Todos los `@PreAuthorize` usan permisos.
*   [ ] **CA3**: `RankingController` y `requireOwner` sin chequeos de rol a mano.
*   [ ] **CA4**: El gate valida su scope.
*   [ ] **CA5**: Tests de autorización por endpoint.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Permisos

**Escenario 1**  

*   **Dado**: un usuario con el permiso `roadmap.graph.edit`
*   **Cuando**: edita un nodo de su curso
*   **Entonces**: puede

**Escenario 2**  

*   **Dado**: un usuario sin ese permiso
*   **Cuando**: edita un nodo
*   **Entonces**: recibe 403

**Escenario 3**  

*   **Dado**: un servicio sin `roadmap.gate.read`
*   **Cuando**: consulta el gate
*   **Entonces**: recibe 403

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

*   **Puntos (Fibonacci)**: 5
*   **Prioridad (MoSCoW / Numérica)**: Should

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 5 | Should |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Users (catálogo de permisos), API Gateway (cómo llegan).
*   Módulos afectados: Todos los controllers, `SecurityConfig`, `GatewayHeadersFilter`.
*   Otros equipos / aprobaciones: G07 Users (bloqueante).
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Que G07 no tenga el catálogo; mitigación: proponer los nombres nosotros.

## Tareas

- [ ] T-22.1 Matriz rol → permisos
- [ ] T-22.2 Acordar con G07
- [ ] T-22.3 Migrar los `@PreAuthorize`
- [ ] T-22.4 Scope del gate
- [ ] T-22.5 Tests de autorización

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Las reglas usan `hasRole`/`hasAnyRole` en constantes por controller (`CAN_EDIT`, `CAN_VIEW`…), más chequeos a mano en `RankingController` y `requireOwner`. El gate acepta cualquier servicio sin validar el scope `roadmap.gate.read`.

### Depende de

Nada: se puede empezar ya.

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|G6]] Ya no habrá roles sino permisos; mientras tanto vale `PROFESSOR`/`GESTOR`.

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|G2]] Catálogo de permisos: es de Users (G07) y todavía no está definido.
