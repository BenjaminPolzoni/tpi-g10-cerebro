---
tags: [tpi, g10, taiga, epica]
ref: 8631
estado: "New"
responsable: "Sin asignar"
avance: "0/7"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/8631
---

# EP-8631: Correcciones de los profes

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/8631) · Estado: **New** · Responsable: **Sin asignar** · HU cerradas: **0/7**

[G10] — Correcciones de los profes
----------------------------------

* * *

Objetivo
--------

Resolver las correcciones que los profes marcaron como nuestras (2026-10-14).

* * *

Suposiciones y Restricciones
----------------------------

*   Suposiciones: Correcciones del documento de los profes (2026-10-14), solo las marcadas como nuestras.
*   Restricciones (legales/técnicas): Las que dependen de otros grupos (catálogo de permisos y usuarios demo de G07) se coordinan; no se implementa lo que es de ellos.

* * *

Criterios de Aceptación a nivel Épico
-------------------------------------

*   [ ] Cada corrección marcada como nuestra en 07 tiene su HU cerrada o una respuesta de los profes que la redefine.
*   [ ] La demo muestra un curso completo de inicio ("Bienvenidos") a fin ("Felicitaciones").
*   [ ] KPIs iniciales alcanzan: Correcciones nuestras resueltas: 11 de 11, o redefinidas con respuesta de los profes.
*   [ ] Sin regresiones críticas en: El ranking mantiene el anonimato (DEC-007). Migrar a permisos no deja ningún endpoint abierto.
*   [ ] Observabilidad y alertas configuradas: Errores del ranking por grupo; 403 por permisos mal asignados.
*   [ ] Documentación de uso y operación publicada: Documentación global del micro (HT-23).

* * *

Dependencias / Impactos
-----------------------

*   Servicios / APIs: Backoffice (permisos, dashboard), Users (usuarios demo), Courses.
*   Módulos afectados: Módulo graph, editor, ranking, mundo 3D, seguridad, seed.
*   Otros equipos: G06, G07, G01.
*   Impacto en datos / migraciones: START/END en roadmaps existentes; configuración de Archibaldo por curso; datos de demo.
*   Feature toggles / flags: Ninguno nuevo.


## Historias

| HU | Estado | Responsable | Sprint | Tareas |
|---|---|---|---|---|
| [[historias/HT-21 Seed de demo curado\|HT-21]] Seed de demo curado | New | Sin asignar | G10 - Sprint 03 | 0/4 |
| [[historias/HT-22 Permisos en vez de roles\|HT-22]] Permisos en vez de roles | New | Sin asignar | G10 - Sprint 03 | 0/4 |
| [[historias/HT-23 Documentación global del micro\|HT-23]] Documentación global del micro | New | Sin asignar | G10 - Sprint 03 | 0/2 |
| [[historias/HU-64 Nodos de inicio y fin obligatorios\|HU-64]] Nodos de inicio y fin obligatorios | New | Sin asignar | G10 - Sprint 03 | 0/5 |
| [[historias/HU-65 Relaciones con tipo\|HU-65]] Relaciones con tipo | New | Sin asignar | G10 - Sprint 03 | 0/4 |
| [[historias/HU-68 Obligatoriedad visible en la lista de nodos\|HU-68]] Obligatoriedad visible en la lista de nodos | New | Sin asignar | G10 - Sprint 03 | 2/4 |
| [[historias/HU-69 Archibaldo - Enter, avatar personalizable y destello\|HU-69]] Archibaldo - Enter, avatar personalizable y destello | New | Sin asignar | G10 - Sprint 03 | 0/4 |
