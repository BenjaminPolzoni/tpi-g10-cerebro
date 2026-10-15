---
tags: [tpi, g10, taiga, hu]
codigo: HU-50
ref: 7341
estado: "Done"
responsable: "Ludmila Mailen Cejas"
epicas: "[[epicas/EP-7340 Mundos (biomas) del roadmap|EP-7340]]"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/7341
---

# HU-50: Elegir el mundo (bioma) de una sección

> [!info] Generado desde Taiga (2026-10-15 16:54). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/7341) · Estado: **Done** · Responsable: **Ludmila Mailen Cejas** · Sprint: **G10 - Sprint 2**
> Épica: [[epicas/EP-7340 Mundos (biomas) del roadmap|EP-7340]] · Tareas cerradas: **5/5**

[G10] — HU-50 — Elegir el mundo (bioma) de una sección
-----------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: elegir el mundo (bioma) en el que se recorre cada sección del roadmap
*   **Para**: que todos mis alumnos vean esa unidad en ese mundo, en cualquier dispositivo

* * *

Notas / Observaciones
---------------------

*   [x] Reglas de negocio: el bioma se guarda como clave de un catálogo cerrado (`MEADOW`, `DESERT`, `SNOW`, `LAVA`, `SPACE`), igual que el ícono de HU-43. Sin bioma elegido = pradera. Es solo visual: no toca el gate, el progreso ni el XP. El PUT de sección es reemplazo completo; el PATCH sin bioma no lo toca.
*   [x] Validaciones: bioma perteneciente al catálogo (400 si no); solo el PROFESSOR dueño del curso.
*   [x] Datos obligatorios: ninguno nuevo; `biome` es opcional en el alta y la edición de sección.
*   [x] Performance (tiempos, volumen, límites): el bioma viaja en el `SectionResponse` del grafo (`GET /courses/{courseId}`), sin llamada extra (menos de 200 ms).
*   [x] Seguridad (roles, permisos, datos sensibles): solo el PROFESSOR dueño del curso edita; sin datos sensibles.
*   [x] Accesibilidad (WCAG/teclado/lectores): el selector de bioma del editor es un `<select>` nativo con etiqueta y emoji + texto; el bioma no transmite información del progreso.
*   [x] Otros: el front manda el bioma en crear, editar y **mover** (los tres son escrituras de sección). La sincronización con Courses (HU-36) nunca pisa el bioma. Cierra la deuda D4 del front para el bioma. `?biome=` queda solo como previsualización.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [x] **CA1**: El profesor elige un bioma para una sección y queda guardado.
*   [x] **CA2**: El alumno ve la sección en ese mundo, sin parámetros en la URL.
*   [x] **CA3**: Un bioma fuera del catálogo se rechaza con 400 y sin cambios.
*   [x] **Extras (opcional)**: sin bioma elegido se ve pradera; renombrar, mover o sincronizar la sección no le cambia el bioma.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Bioma de la sección

**Escenario 1**  

*   **Dado**: una sección sin bioma elegido
*   **Cuando**: el profesor le elige Luna
*   **Entonces**: queda guardado y al reabrir el roadmap sigue en Luna

**Escenario 2**  

*   **Dado**: un bioma que no existe en el catálogo
*   **Cuando**: el profesor intenta guardarlo
*   **Entonces**: rechazo 400, y la sección sigue sin bioma elegido

**Escenario 3**  

*   **Dado**: una sección con el bioma Lava
*   **Cuando**: el profesor la renombra
*   **Entonces**: sigue con el bioma Lava

* * *

Prototipo
---------

*   **Capturas**: selector "🚀 Luna" en el editor de la sección; capturas en el PR 2026-P4-FE/2026-PIV-TPI-FE#303.
*   **URL Figma**: no aplica (reusa el selector de bioma existente del editor).
*   **Storybook**: no aplica.
*   **Mock API / Swagger**: [POST /api/roadmap/courses/{courseId}/sections], [PUT/PATCH /api/roadmap/sections/{sectionId}] y [GET /api/roadmap/courses/{courseId}] con `biome` (enum de 5 valores) en `docs/api_doc/swagger.json`.

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: 3
*   **Prioridad (MoSCoW / Numérica)**: Should

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: tpi-roadmap, front Angular.
*   Módulos afectados: back `GraphService`, `SectionEntity`, `Section`, `GraphDtos` y `CourseSectionsReconciliationService` (sin cambios, test nuevo); front `roadmap-mapper`, `http-roadmap.adapter`, `backend-roadmap.dto`, hub de islas.
*   Otros equipos / aprobaciones: ninguno (campo aditivo y opcional; eventos de Kafka sin cambios).
*   Impacto en datos / migraciones: V22, columna `section.biome` VARCHAR(16) nullable; las secciones existentes quedan en NULL (pradera).
*   Riesgos y mitigación (opcional): un PUT sin bioma lo resetea → el front lo manda en toda escritura (test que lo fija). Implementación: back 2026-P4-BE/tpi-roadmap#146, front 2026-P4-FE/2026-PIV-TPI-FE#303.

## Tareas

- [x] #7348 T-50.1 Migración, campo y validación contra el catálogo · Closed · Ludmila Mailen Cejas
- [x] #7349 T-50.2 Exponer y guardar biome en los endpoints de sección · Closed · Ludmila Mailen Cejas
- [x] #7350 T-50.3 Guardar y leer el bioma desde el front · Closed · Ludmila Mailen Cejas
- [x] #7351 T-50.4 Tests BDD · Closed · Ludmila Mailen Cejas
- [x] #7352 T-50.5 OpenAPI y documentación · Closed · Ludmila Mailen Cejas
