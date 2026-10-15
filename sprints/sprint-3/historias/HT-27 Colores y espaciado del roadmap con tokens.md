---
tags: [tpi, g10, sprint-3, ht]
codigo: HT-27
estado: Propuesta
responsable: ""
epica: "Consistencia visual con la UI-KIT"
sprint: "G10 - Sprint 3"
puntos: 5
prioridad: Could
en_taiga: false
---

# HT-27: Colores y espaciado del roadmap con tokens

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Consistencia visual con la UI-KIT|Consistencia visual con la UI-KIT]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga.

[G10] — HT-27 — Colores y espaciado del roadmap con tokens
----------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: EQUIPO DE DESARROLLO
*   **Quiero**: que el roadmap use los tokens del kit para colores, espaciado y tipografía
*   **Para**: que el tema claro y oscuro funcione igual que en el resto

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Se borra el puente `--color-*`. Quedan afuera `engine/` y el arte.
*   [ ] Validaciones: Regla de `stylelint` contra hex/rgb literales en las carpetas de G10.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): No aplica.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Puente `--color-*` borrado.
*   [ ] **CA2**: Sin colores literales fuera de `engine/` y arte.
*   [ ] **CA3**: Regla de `stylelint` activa.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Tokens del kit

**Escenario 1**  

*   **Dado**: el roadmap
*   **Cuando**: se cambia a tema oscuro
*   **Entonces**: todos los componentes cambian

**Escenario 2**  

*   **Dado**: un color literal nuevo
*   **Cuando**: se commitea
*   **Entonces**: `stylelint` falla

**Escenario 3**  

*   **Dado**: `engine/`
*   **Cuando**: tiene colores literales
*   **Entonces**: la regla no lo marca

* * *

Prototipo
---------

*   **Capturas**: Roadmap en tema claro y oscuro.
*   **URL Figma**: No aplica.
*   **Storybook**: Tokens del kit.
*   **Mock API / Swagger**: No aplica.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 5
*   **Prioridad (MoSCoW / Numérica)**: Could

**Formato tabla (opcional)**

| Puntos (Fibonacci) | Prioridad (MoSCoW / Numérica) |
| --- | --- |
| 5 | Could |

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: Ninguno.
*   Módulos afectados: CSS del roadmap.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Regresiones visuales; mitigación: tests visuales.

## Tareas

- [ ] T-27.1 Reemplazar colores
- [ ] T-27.2 Borrar el puente
- [ ] T-27.3 Regla de stylelint

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

316 colores hardcodeados y un puente de tokens `--color-*` propio.

### Depende de

- [[sprints/sprint-3/historias/HT-25 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs|HT-25]] Subir la UI-KIT a 0.8.0 y cerrar sus TODOs

### Dudas que la frenan

Ninguna.

### Deuda técnica que cierra

- [[deuda-tecnica|DT-15]]
