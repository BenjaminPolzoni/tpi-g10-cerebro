---
tags: [tpi, g10, taiga, epica]
ref: 8630
estado: "New"
responsable: "Sin asignar"
avance: "0/2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/8630
---

# EP-8630: Consistencia visual con la UI-KIT

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/8630) · Estado: **New** · Responsable: **Sin asignar** · HU cerradas: **0/2**

[G10] — Consistencia visual con la UI-KIT
-----------------------------------------

* * *

Objetivo
--------

Que las pantallas del roadmap y del ranking usen la UI-KIT (`@2026-p4-fe/ui`) en vez de controles y colores propios, y aportar al kit el componente de grafo.

* * *

Suposiciones y Restricciones
----------------------------

*   Suposiciones: El front ya usa la UI-KIT `@2026-p4-fe/ui` 0.8.0 (PR #567).
*   Restricciones (legales/técnicas): Quedan afuera `engine/` (three.js) y el arte. Lo que falta en el kit se aporta al kit, no se hace local.

* * *

Criterios de Aceptación a nivel Épico
-------------------------------------

*   [ ] El front está en la UI-KIT 0.8.0 sin TODOs pendientes del kit.
*   [ ] Las pantallas de G10 no tienen `<button>`, `<input>` ni `<select>` crudos ni colores hardcodeados (salvo `engine/` y arte).
*   [ ] El componente de grafo existe en el kit (HT-34) y lo usa la vista de grafo (HU-62).
*   [ ] KPIs iniciales alcanzan: Colores hardcodeados en el roadmap: de 316 a 0 fuera de `engine/` y arte. TODOs del kit: de 9 a 0.
*   [ ] Sin regresiones críticas en: Tests visuales sin diferencias no esperadas en pantallas de otros grupos.
*   [ ] Observabilidad y alertas configuradas: Regla de `stylelint` en el CI contra colores literales.
*   [ ] Documentación de uso y operación publicada: README del kit con el componente de grafo.

* * *

Dependencias / Impactos
-----------------------

*   Servicios / APIs: Ninguno.
*   Módulos afectados: Pantallas del roadmap y del ranking; repo de la UI-KIT.
*   Otros equipos: Equipo de la UI-KIT; resto de los grupos del front (bump).
*   Impacto en datos / migraciones: Sin migración.
*   Feature toggles / flags: Ninguno.


## Historias

| HU | Estado | Responsable | Sprint | Tareas |
|---|---|---|---|---|
| [[historias/HT-26 Adopción de la UI-KIT en el roadmap\|HT-26]] Adopción de la UI-KIT en el roadmap | New | Sin asignar | G10 - Sprint 03 | 0/7 |
| [[historias/HT-34 Componente de grafo en la UI-KIT\|HT-34]] Componente de grafo en la UI-KIT | New | Sin asignar | G10 - Sprint 03 | 0/2 |
