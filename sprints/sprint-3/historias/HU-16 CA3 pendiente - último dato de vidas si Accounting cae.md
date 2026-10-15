---
tags: [tpi, g10, sprint-3, hu]
codigo: HU-16
estado: Propuesta
responsable: ""
epica: "Deuda del Sprint 2"
sprint: "G10 - Sprint 3"
puntos: 3
prioridad: Should
en_taiga: true
---

# HU-16: CA3 pendiente - último dato de vidas si Accounting cae

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Deuda del Sprint 2|Deuda del Sprint 2]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Ya existe en Taiga: [[taiga/historias/HU-16 Integración real con Inventario para las vidas del gate|HU-16]] (épica EP-60). En el Sprint 3 se **reabre** con lo que falta.

[G10] — HU-16 — Integración real con Inventario para las vidas del gate
-----------------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: que la pantalla de inventario me muestre el último dato conocido si Accounting está caído, sin que el gate lo use para habilitarme
*   **Para**: ver mis vidas aunque haya una caída, sin que se me habilite algo por un dato viejo

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: La pantalla muestra el último dato conocido con `stale: true` (retención 24 h por defecto). El gate nunca habilita con un dato `stale`.
*   [ ] Validaciones: Pasadas las 24 h el dato se descarta.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): El aviso de dato desactualizado se muestra en texto.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: La pantalla de inventario muestra el último dato con aviso si Accounting no responde.
*   [ ] **CA2**: Pasadas 24 h el dato no se muestra.
*   [ ] **CA3**: El gate nunca habilita con un dato `stale`.
*   [ ] **CA4**: Tests de caché vigente, vencida y sin caché.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Dato desactualizado de inventario

**Escenario 1**  

*   **Dado**: Accounting caído y un dato de hace 2 h
*   **Cuando**: el alumno abre el inventario
*   **Entonces**: ve sus vidas con el aviso «dato desactualizado»

**Escenario 2**  

*   **Dado**: el mismo caso
*   **Cuando**: el Motor consulta el gate
*   **Entonces**: el gate no habilita con ese dato

**Escenario 3**  

*   **Dado**: un dato de hace 25 h
*   **Cuando**: el alumno abre el inventario
*   **Entonces**: no se muestra y aparece el error

* * *

Prototipo
---------

*   **Capturas**: Pantalla de inventario con aviso.
*   **URL Figma**: Pendiente.
*   **Storybook**: `generic-alert`.
*   **Mock API / Swagger**: GET /api/roadmap/courses/{courseId}/inventory → `stale`.

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

*   Servicios involucrados: Accounting.
*   Módulos afectados: `InventoryService`, `GateService`, pantalla de inventario.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Ninguno.

## Tareas

- [ ] T-16.6 Retención de 24 h
- [ ] T-16.7 El gate ignora datos `stale`
- [ ] T-16.8 Tests

---

## Contexto del Sprint 3 (no va a Taiga)

### Criterios de la HU original (Taiga)

Verificados contra `origin/develop` (back `fc1917e`, front `67cbad4a`) el 2026-10-15. ✅ cumple · ❌ no cumple · ⚠️ hecho pero no anda de punta a punta.

- [x] ✅ **CA1**: El gate usa las vidas que devuelve Accounting. — `InventoryClient.fetchLives`
- [x] ✅ **CA2**: Con 0 vidas la entrega se rechaza con motivo «sin vidas». — `no_lives`
- [ ] ❌ **CA3**: Con Accounting caído se usa el último dato conocido marcado como desactualizado. — el gate no usa el último dato; el cache `lastKnown` solo lo usa la pantalla de inventario
- [x] ✅ **CA4**: Sin ningún dato conocido la respuesta es 503, no «habilitado». — 503 `inventory.unavailable`

### Qué hay hoy en el código

La pantalla de inventario ya usa `lastKnown` + `stale`; falta asegurar la retención de 24 h y que el gate nunca use ese dato.

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

Ninguna.
