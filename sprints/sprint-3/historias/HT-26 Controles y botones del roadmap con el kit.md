---
tags: [tpi, g10, sprint-3, ht]
codigo: HT-26
estado: Propuesta
responsable: ""
epica: "Consistencia visual con la UI-KIT"
sprint: "G10 - Sprint 3"
puntos: 3
prioridad: Should
en_taiga: false
---

# HT-26: Controles y botones del roadmap con el kit

> [!info] Sprint 3 · Épica: [[sprints/sprint-3/epicas/G10 — Consistencia visual con la UI-KIT|Consistencia visual con la UI-KIT]] · Estado: **Propuesta** · Responsable: **a definir** · Sprint: **G10 - Sprint 3**
> Nueva: todavía no está cargada en Taiga.

[G10] — HT-26 — Controles y botones del roadmap con el kit
----------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: USUARIO
*   **Quiero**: formularios y botones del roadmap iguales al resto de la plataforma
*   **Para**: una experiencia consistente y accesible

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Reemplazar controles crudos por los del kit.
*   [ ] Validaciones: No aplica.
*   [ ] Datos obligatorios: No aplica.
*   [ ] Performance (tiempos, volumen, límites): No aplica.
*   [ ] Seguridad (roles, permisos, datos sensibles): No aplica.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Labels, foco y estados de error del kit.
*   [ ] Otros: No aplica.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: `entity-editor-dialog`, `badges-catalog-page` y `avatar-panel` con controles del kit.
*   [ ] **CA2**: Botones y headings sueltos de `course-editor-page`, `section-nodes`, `course-map-page`, `hex-world-page` y `feedback-toast` con el kit.
*   [ ] **CA3**: Sin `::ng-deep` nuevos.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Controles del kit

**Escenario 1**  

*   **Dado**: el editor de entidades
*   **Cuando**: se abre
*   **Entonces**: usa `generic-input`, `generic-select` y `genericButton`

**Escenario 2**  

*   **Dado**: un campo con error
*   **Cuando**: se valida
*   **Entonces**: muestra el error del kit

**Escenario 3**  

*   **Dado**: la navegación con teclado
*   **Cuando**: se recorre el formulario
*   **Entonces**: el foco sigue el orden visual

* * *

Prototipo
---------

*   **Capturas**: Pantallas listadas.
*   **URL Figma**: No aplica.
*   **Storybook**: Componentes de formulario del kit.
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
*   Módulos afectados: Pantallas listadas.
*   Otros equipos / aprobaciones: Ninguno.
*   Impacto en datos / migraciones: Sin migración.
*   Riesgos y mitigación (opcional): Ninguno.

## Tareas

- [ ] T-26.1 Formularios
- [ ] T-26.2 Botones y headings

---

## Contexto del Sprint 3 (no va a Taiga)

### Qué hay hoy en el código

`entity-editor-dialog`, `badges-catalog-page` y `avatar-panel` usan `<input>`, `<select>` y `<button>` crudos. Hay botones y headings sueltos en `course-editor-page`, `section-nodes`, `course-map-page`, `hex-world-page` y `feedback-toast`.

### Depende de

Ninguna.

### Dudas que la frenan

Ninguna.
