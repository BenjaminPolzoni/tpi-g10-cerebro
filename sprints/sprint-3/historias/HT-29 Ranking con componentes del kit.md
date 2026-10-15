---
tags: [tpi, g10, sprint-3, ht]
codigo: HT-29
estado: Propuesta
responsable: ""
epica: "Consistencia visual con la UI-KIT"
sprint: "G10 - Sprint 3"
puntos: 3
prioridad: Should
en_taiga: false
---

# HT-29: Ranking con componentes del kit

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Consistencia visual con la UI-KIT|Consistencia visual con la UI-KIT]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga.

[G10] — HT-29 — Ranking con componentes del kit
-----------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: el ranking con la misma tabla y chips que el resto de la plataforma
*   **Para**: leerlo igual que las otras tablas

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Se mantiene el anonimato de filas ajenas (DEC-007).
*   [ ] Validaciones: No aplica.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Tabla con `caption` y encabezados del kit.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: `generic-table` y `generic-badge` en `ranking/*`.
*   [ ] **CA2**: Anonimato intacto.
*   [ ] **CA3**: Tests visuales.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Ranking con el kit

**Escenario 1**  

*   **Dado**: el ranking
*   **Cuando**: se abre
*   **Entonces**: usa `generic-table`

**Escenario 2**  

*   **Dado**: una fila ajena
*   **Cuando**: se ve
*   **Entonces**: sigue sin datos personales

**Escenario 3**  

*   **Dado**: un lector de pantalla
*   **Cuando**: recorre la tabla
*   **Entonces**: lee el caption y los encabezados

* * *

Prototipo
---------

*   **Capturas**: Ranking.
*   **URL Figma**: No aplica.
*   **Storybook**: `generic-table`.
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

*   Servicios involucrados: Ninguno.
*   Módulos afectados: `ranking/*`.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Ninguno.

## Tareas

- [ ] T-29.1 Tabla y chips del kit
- [ ] T-29.2 Tests

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

El ranking tiene 3 `<table>` crudas y chips propios.

### Depende de

Ninguna.

### Dudas que la frenan

Ninguna.
