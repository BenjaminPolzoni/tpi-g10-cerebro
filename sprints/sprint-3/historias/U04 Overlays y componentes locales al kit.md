---
tags: [tpi, g10, sprint-3, historia, ht]
id: U04
tipo: HT
epica: "EP-S3-3"
capa: "Front"
esfuerzo: M
puntos: 5
prioridad: Should
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [U01]
---

# U04: Overlays y componentes locales al kit

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-3 Consistencia visual con la UI-KIT|EP-S3-3]] · **HT** · Capa: **Front** · **5 pts** · **Should** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HT-xx — Overlays y componentes locales al kit** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: USUARIO
- **Quiero**: diálogos y componentes del roadmap accesibles y consistentes con el kit
- **Para**: usar el mundo con teclado y lector de pantalla

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: `streak` se saca de la UI o se conecta a datos reales (hoy muestra 7 fijo, DT-13).
- [ ] Accesibilidad (WCAG/teclado/lectores): Los diálogos del kit manejan el foco y Escape.

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: `npc-dialogue` y `shop-interior` con `generic-modal`/`generic-drawer`.
- [ ] **CA2**: `lives`, `level-hud`, `inventory-item-card` y `role-switch` con componentes del kit.
- [ ] **CA3**: `streak` sacado o conectado a datos reales.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Componentes del kit

**Escenario 1**

- **Dado**: el diálogo de un NPC
- **Cuando**: se abre
- **Entonces**: el foco entra y Escape lo cierra

**Escenario 2**

- **Dado**: las vidas del alumno
- **Cuando**: se muestran
- **Entonces**: usan `generic-progress [hearts]`

**Escenario 3**

- **Dado**: la racha
- **Cuando**: se mira el HUD
- **Entonces**: no muestra un número falso

* * *

## Prototipo

- **Capturas**: HUD y diálogos del mundo.
- **URL Figma**: No aplica.
- **Storybook**: `generic-modal`, `generic-xp-bar`, `generic-item-tile`.
- **Mock API / Swagger**: No aplica.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 5
- **Prioridad (MoSCoW / Numérica)**: Should

* * *

## Dependencias / Impactos

- Servicios involucrados: Ninguno.
- Módulos afectados: Componentes listados.
- Otros equipos / aprobaciones: Ninguno.
- Impacto en datos / migraciones: Sin migración.
- Riesgos y mitigación (opcional): Ninguno.

## Tareas

- [ ] T-U04.1 Diálogos
- [ ] T-U04.2 HUD
- [ ] T-U04.3 Racha

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

`npc-dialogue` y `shop-interior` tienen su propio `role="dialog"`. `lives`, `streak`, `role-switch`, `inventory-item-card` y `level-hud` son componentes propios.

### Depende de

- [[sprints/sprint-3/historias/U01 Subir la UI-KIT a 0.8.0 y cerrar sus TODOs|U01]] Subir la UI-KIT a 0.8.0 y cerrar sus TODOs

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|E12]]

### Deuda técnica que cierra

- [[deuda-tecnica|DT-13]]
