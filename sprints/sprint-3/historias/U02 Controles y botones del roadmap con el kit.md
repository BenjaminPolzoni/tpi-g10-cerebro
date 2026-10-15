---
tags: [tpi, g10, sprint-3, historia, ht]
id: U02
tipo: HT
epica: "EP-S3-3"
capa: "Front"
esfuerzo: S
puntos: 3
prioridad: Should
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [U01]
---

# U02: Controles y botones del roadmap con el kit

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-3 Consistencia visual con la UI-KIT|EP-S3-3]] · **HT** · Capa: **Front** · **3 pts** · **Should** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HT-xx — Controles y botones del roadmap con el kit** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: USUARIO
- **Quiero**: formularios y botones del roadmap iguales al resto de la plataforma
- **Para**: una experiencia consistente y accesible

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Reemplazar controles crudos por los del kit.
- [ ] Accesibilidad (WCAG/teclado/lectores): Labels, foco y estados de error del kit.

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: `entity-editor-dialog`, `badges-catalog-page` y `avatar-panel` con controles del kit.
- [ ] **CA2**: Botones y headings sueltos de `course-editor-page`, `section-nodes`, `course-map-page`, `hex-world-page` y `feedback-toast` con el kit.
- [ ] **CA3**: Sin `::ng-deep` nuevos.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Controles del kit

**Escenario 1**

- **Dado**: el editor de entidades
- **Cuando**: se abre
- **Entonces**: usa `generic-input`, `generic-select` y `genericButton`

**Escenario 2**

- **Dado**: un campo con error
- **Cuando**: se valida
- **Entonces**: muestra el error del kit

**Escenario 3**

- **Dado**: la navegación con teclado
- **Cuando**: se recorre el formulario
- **Entonces**: el foco sigue el orden visual

* * *

## Prototipo

- **Capturas**: Pantallas listadas.
- **URL Figma**: No aplica.
- **Storybook**: Componentes de formulario del kit.
- **Mock API / Swagger**: No aplica.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 3
- **Prioridad (MoSCoW / Numérica)**: Should

* * *

## Dependencias / Impactos

- Servicios involucrados: Ninguno.
- Módulos afectados: Pantallas listadas.
- Otros equipos / aprobaciones: Ninguno.
- Impacto en datos / migraciones: Sin migración.
- Riesgos y mitigación (opcional): Ninguno.

## Tareas

- [ ] T-U02.1 Formularios
- [ ] T-U02.2 Botones y headings

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

`entity-editor-dialog`, `badges-catalog-page` y `avatar-panel` usan `<input>`, `<select>` y `<button>` crudos. Hay botones y headings sueltos en `course-editor-page`, `section-nodes`, `course-map-page`, `hex-world-page` y `feedback-toast`.

### Depende de

- [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs|U01]] Subir la UI-KIT a 0.8.0 y cerrar sus TODOs

### Dudas que la frenan

Ninguna.
