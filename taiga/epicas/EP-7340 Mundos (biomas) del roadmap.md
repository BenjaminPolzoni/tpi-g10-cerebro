---
tags: [tpi, g10, taiga, epica]
ref: 7340
estado: "New"
responsable: "Sin asignar"
avance: "7/7"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/7340
---

# EP-7340: Mundos (biomas) del roadmap

> [!info] Generado desde Taiga (2026-10-14 20:45). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/7340) · Estado: **New** · Responsable: **Sin asignar** · HU cerradas: **7/7**

[G10] — Mundos (biomas) del roadmap
----------------------------------

* * *

Objetivo
--------

Que cada sección del roadmap se recorra en un mundo (bioma) que elige el PROFESOR, con identidad visual y de juego propia, sin cambiar el progreso, los desbloqueos ni el XP del alumno.

* * *

Suposiciones y Restricciones
----------------------------

*   Suposiciones: el mapa hexagonal (`/roadmap/play`) es la única vista del recorrido vigente; el grafo de nodos, el detalle y la lectura de contenido y el progreso ya existen (HU-01, HU-05, HU-06, HU-19).
*   Restricciones (legales/técnicas): el bioma es solo visual (no toca gate, progreso ni XP); catálogo cerrado de biomas; assets con licencia libre (CC0) cuidando el peso del repo; todo efecto de ambiente se apaga con la tecla X; 100 % escritorio (RF-NFR-05); solo el PROFESSOR dueño del curso elige el bioma (RF-CUR-04).

* * *

Criterios de Aceptación a nivel Épico
-------------------------------------

*   [ ] El conjunto mínimo de historias permite que el profesor elija el bioma de una sección y que todos sus alumnos recorran esa unidad en ese mundo, de punta a punta (HU-50 + una HU por bioma).
*   [ ] KPIs iniciales alcanzan: ningún KPI de producto aplica. Indicador propio: la descarga de una unidad en un bioma nuevo no supera en más de un 10 % a la de pradera (hoy Espacio ~5,7 MB vs pradera ~6,0 MB).
*   [ ] Sin regresiones críticas en el recorrido del alumno: elegir o cambiar un bioma no altera el progreso, los desbloqueos ni el XP, y el layout de los mapas de los demás biomas no cambia.
*   [ ] Observabilidad y alertas configuradas (logs, métricas, traces): no aplica (cambio visual y un campo nuevo en la sección, cubierto por el log de edición existente).
*   [ ] Documentación de uso y operación publicada: guía para sumar un bioma (`docs/roadmap/npc-world-biomes.md` en el front) y contrato OpenAPI con `biome`.

* * *

Dependencias / Impactos
-----------------------

*   Servicios / APIs: tpi-roadmap (`section.biome` en POST/PUT/PATCH de sección y en `GET /courses/{courseId}`); Motor de Desafíos (abrir el intento desde el personaje).
*   Módulos afectados: back `GraphService`, `SectionEntity`, `GraphDtos`; front mapa hexagonal (`world-gen`, `world-3d.service`, `hex-world-page`), editor del profesor y hub de islas.
*   Otros equipos: ninguno bloqueante.
*   Impacto en datos / migraciones: columna `section.biome` nullable (V22); sin bioma = pradera.
*   Feature toggles / flags: no. `?biome=` queda solo como previsualización.
*   Historias previstas: HU-50 (elegir el mundo de una sección), HU-51 (mundo Espacio), y una HU por cada bioma nuevo: Cementerio, Isla pirata, Japón y dos más a definir.
*   PRs de referencia: front 2026-P4-FE/2026-PIV-TPI-FE#303, back 2026-P4-BE/tpi-roadmap#146.

## Historias

| HU | Estado | Responsable | Sprint | Tareas |
|---|---|---|---|---|
| [[historias/HU-50 Elegir el mundo (bioma) de una sección\|HU-50]] Elegir el mundo (bioma) de una sección | Done | Ludmila Mailen Cejas | G10 - Sprint 2 | 5/5 |
| [[historias/HU-51 Recorrer la unidad en el mundo Espacio (Luna)\|HU-51]] Recorrer la unidad en el mundo Espacio (Luna) | Done | Ludmila Mailen Cejas | G10 - Sprint 2 | 7/7 |
| [[historias/HU-52 Recorrer la unidad en el mundo Cementerio\|HU-52]] Recorrer la unidad en el mundo Cementerio | Done | Iker Alonso | G10 - Sprint 2 | 5/5 |
| [[historias/HU-53 Recorrer la unidad en el mundo Isla pirata\|HU-53]] Recorrer la unidad en el mundo Isla pirata | Done | Lautaro Jesus Diego | G10 - Sprint 2 | 6/6 |
| [[historias/HU-54 Recorrer la unidad en el mundo Japón\|HU-54]] Recorrer la unidad en el mundo Japón | Done | Mateo Delgado Costa | G10 - Sprint 2 | 6/6 |
| [[historias/HU-55 Recorrer la unidad en el mundo Cyberpunk\|HU-55]] Recorrer la unidad en el mundo Cyberpunk | Done | Benjamin Polzoni | G10 - Sprint 2 | 6/6 |
| [[historias/HU-56 Recorrer la unidad en el mundo Apocalipsis zombie\|HU-56]] Recorrer la unidad en el mundo Apocalipsis zombie | Done | Fenoglio Santino | G10 - Sprint 2 | 5/5 |
