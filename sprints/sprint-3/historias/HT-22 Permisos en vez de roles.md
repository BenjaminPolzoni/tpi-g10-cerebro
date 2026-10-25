---
tags: [tpi, g10, sprint-3, ht]
codigo: HT-22
estado: New
responsable: "Sin asignar"
epica: "Correcciones de los profes"
sprint: "G10 - Sprint 3"
puntos: 5
prioridad: Should
en_taiga: true
ref: 8605
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8605
responsables_tareas: ["Gabriela Camacho", "Baltasar Rodriguez Teruel"]
tareas_cerradas: "0/4"
---

# HT-22: Permisos en vez de roles

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Correcciones de los profes|Correcciones de los profes]] · Estado: **New** · Responsable de la historia: **Sin asignar** · Tareas: **0/4** · Sprint: **G10 - Sprint 3**
> Cargada en Taiga: [[taiga/historias/HT-22 Permisos en vez de roles|HT-22]] ([abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8605)) · Épica en Taiga: [[epicas/EP-8631 Correcciones de los profes|EP-8631]] · Responsables de las tareas: [[sprints/sprint-3/12-responsables#Gabriela Camacho|Gabriela Camacho]] (2), [[sprints/sprint-3/12-responsables#Baltasar Rodriguez Teruel|Baltasar Rodriguez Teruel]] (2).

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

> [!info] Espejo de Taiga (sync 2026-10-15). Cerradas: **0/4**. Historia en Taiga: [[taiga/historias/HT-22 Permisos en vez de roles|HT-22]] · [abrir](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/8605)

- [ ] [#9090](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9090) **T-22.1 Escribir la matriz de permisos** · Back · New · [[sprints/sprint-3/12-responsables#Gabriela Camacho|Gabriela Camacho]]
    - **Qué:** listar cada endpoint del micro con el permiso que va a pedir (por ejemplo `roadmap.graph.edit`, `roadmap.ranking.read`) y qué roles lo tienen hoy. Sale de las constantes `CAN_EDIT`, `CAN_VIEW`… de cada controller. Cierra DT-03.
    - **Listo cuando:** la matriz está en el Obsidian y en `docs/` del back.
    - ✅ **Hecha (2026-10-23):** [[arquitectura/T-22-1-matriz-permisos]] y `docs/T-22-1-MATRIZ-PERMISOS.md` (rama `feature/t-22-1-matriz-permisos`). Falta cerrarla en Taiga. Dejó hallazgos para T-22.3: el GESTOR no tiene el mismo acceso en todos los controllers, y un profesor lee progreso, XP e insignias de cualquier curso sin chequeo de dueño.
- [ ] [#9091](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9091) **T-22.2 Acordar los nombres de permisos con Users (G07)** · Coordinación · New · [[sprints/sprint-3/12-responsables#Gabriela Camacho|Gabriela Camacho]]
    - **Qué:** mandar la matriz a G07, que es dueño del catálogo (G2), y acordar nombres y cómo llegan en el token o en los headers del Gateway. Mientras no haya respuesta se sigue con `PROFESSOR`/`GESTOR` (G6).
    - **Listo cuando:** la respuesta de G07 está en `acuerdos/users`.
    - 🟡 **En curso (2026-10-25):** los nombres ya los define [tpi-roadmap#294](https://github.com/2026-P4-BE/tpi-roadmap/pull/294) (7 permisos `roadmap.*` y `roadmap.gate.read`). Las dos preguntas pendientes (Gateway y catálogo de Compose, con el pedido de que GESTOR tenga `badge.write`/`progress.read`) se abrieron como [tpi-users#215](https://github.com/2026-P4-BE/tpi-users/issues/215), sin respuesta todavía. El detalle está en [[acuerdos/users#Pendiente / próximos pasos|acuerdos/users]].
- [ ] [#9092](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9092) **T-22.3 Autorizar por permisos en todos los controllers** · Back · New · [[sprints/sprint-3/12-responsables#Baltasar Rodriguez Teruel|Baltasar Rodriguez Teruel]]
    - **Qué:** reemplazar `hasRole`/`hasAnyRole` por `hasAuthority('roadmap.…')` en los 12 controllers y sacar los chequeos de rol a mano de `RankingController` y `requireOwner`. El chequeo de dueño del curso se mantiene.
    - **Listo cuando:** no queda `hasRole` en el código y hay tests de autorización por endpoint (permitido y 403).
- [ ] [#9093](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/task/9093) **T-22.4 Exigir el scope del gate** · Back · New · [[sprints/sprint-3/12-responsables#Baltasar Rodriguez Teruel|Baltasar Rodriguez Teruel]]
    - **Qué:** el endpoint del gate pide el scope `roadmap.gate.read` al servicio que llama (DT-01).
    - **Dónde:** `SecurityConfig`, `ServiceIdentity`.
    - **Listo cuando:** un servicio sin el scope recibe 403 y el Motor con el scope sigue funcionando. Hay test.

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

Las reglas usan `hasRole`/`hasAnyRole` en constantes por controller (`CAN_EDIT`, `CAN_VIEW`…), más chequeos a mano en `RankingController` y `requireOwner`. El gate acepta cualquier servicio sin validar el scope `roadmap.gate.read`.

### Depende de

- G07 Users: catálogo de permisos (G2). Bloquea T-22.2 a T-22.4.
- T-22.1 (la matriz) se puede empezar ya.

### Dudas resueltas (2026-10-15)

- ✅ [[sprints/sprint-3/08-dudas|G6]] Ya no habrá roles sino permisos; mientras tanto vale `PROFESSOR`/`GESTOR`.

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|G2]] Catálogo de permisos: es de Users (G07) y todavía no está definido.

### Posible cambio cercano: el Gateway deja de mandar el rol (2026-10-17)

> [!warning] Aviso del equipo (2026-10-17)
> El Gateway va a dejar de inyectar el rol (`X-User-Roles`) y va a mandar **los permisos** del usuario. Todavía no hay fecha ni nombre de header confirmados: anotado como posible cambio en un futuro no muy lejano.

- **Qué rompe (verificado en `develop`, `3317456`):** `GatewayHeadersFilter` arma las authorities solo desde `X-User-Roles`. Sin ese header autentica al usuario **sin authorities** (`roles(null)` → lista vacía), así que todo `hasRole`/`hasAnyRole` responde **403**. No degrada: corta todos los endpoints de usuario.
- **Dónde hay chequeos por rol hoy:** las constantes `CAN_*` de cada controller, `Roles.isPlatformStaff` (ADMIN/GESTOR), `requireOwner` y las ramas de `RankingController` (alumno / profesor dueño / staff).
- **Sumado el 2026-10-17 en T-45.9:** el `GESTOR` ve el ranking como ADMIN (`CAN_VIEW_RANKING` + `Roles.isPlatformStaff`). Es un chequeo más para migrar.
- **Qué hacer cuando se confirme:** leer el header de permisos en `GatewayHeadersFilter` y pasar los `@PreAuthorize` a `hasAuthority('roadmap.…')` con la matriz de T-22.1 ([[deuda-tecnica|DT-02 y DT-03]]). Hasta entonces seguir con roles, como dice G6.
