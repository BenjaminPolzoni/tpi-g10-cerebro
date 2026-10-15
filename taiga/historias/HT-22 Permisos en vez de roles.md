---
tags: [tpi, g10, taiga, ht]
codigo: HT-22
ref: 8605
estado: "New"
responsable: "Sin asignar"
epicas: "[[epicas/EP-8631 Correcciones de los profes|EP-8631]]"
sprint: "G10 - Sprint 03"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8605
---

# HT-22: Permisos en vez de roles

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8605) · Estado: **New** · Responsable: **Sin asignar** · Sprint: **G10 - Sprint 03**
> Épica: [[epicas/EP-8631 Correcciones de los profes|EP-8631]] · Tareas cerradas: **0/4**

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

- [ ] #9090 T-22.1 Escribir la matriz de permisos · New · Gabriela Camacho
- [ ] #9091 T-22.2 Acordar los nombres de permisos con Users (G07) · New · Gabriela Camacho
- [ ] #9092 T-22.3 Autorizar por permisos en todos los controllers · New · Baltasar Rodriguez Teruel
- [ ] #9093 T-22.4 Exigir el scope del gate · New · Baltasar Rodriguez Teruel
