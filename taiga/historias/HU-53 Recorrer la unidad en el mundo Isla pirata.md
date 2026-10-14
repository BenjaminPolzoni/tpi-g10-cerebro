---
tags: [tpi, g10, taiga, hu]
codigo: HU-53
ref: 7386
estado: "Done"
responsable: "Lautaro Jesus Diego"
epicas: "[[epicas/EP-7340 Mundos (biomas) del roadmap|EP-7340]]"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/7386
---

# HU-53: Recorrer la unidad en el mundo Isla pirata

> [!info] Generado desde Taiga (2026-10-14 20:45). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/7386) · Estado: **Done** · Responsable: **Lautaro Jesus Diego** · Sprint: **G10 - Sprint 2**
> Épica: [[epicas/EP-7340 Mundos (biomas) del roadmap|EP-7340]] · Tareas cerradas: **6/6**

[G10] — HU-53 — Recorrer la unidad en el mundo Isla pirata
---------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ESTUDIANTE
*   **Quiero**: recorrer una unidad en el mundo Isla pirata, con su propio terreno, decoración y ambiente
*   **Para**: que cada unidad se sienta como un lugar distinto y el recorrido sea más motivador

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: nuevo bioma del catálogo cerrado (valor nuevo en el enum `Biome` del back y en el front). Es solo visual: no toca el gate, el progreso ni el XP. Mismo layout que los demás biomas para la misma semilla (no cambiar el orden de `rand()` en `world-gen.ts`). Personajes que entregan anexos y desafío teórico como personaje: opcional, siguiendo la guía.
*   [ ] Validaciones: el bioma nuevo se acepta en el back (POST/PUT/PATCH de sección) y se rechaza cualquier valor fuera del catálogo.
*   [ ] Datos obligatorios: ninguno nuevo (usa `section.biome`, HU-50).
*   [ ] Performance (tiempos, volumen, límites): assets livianos y reutilizados (tinte/tamaño en vez de archivos nuevos); descarga de la unidad no más de un 10 % por encima de pradera.
*   [ ] Seguridad (roles, permisos, datos sensibles): solo el PROFESSOR dueño del curso elige el bioma (HU-50); sin datos sensibles.
*   [ ] Accesibilidad (WCAG/teclado/lectores): todo efecto de ambiente se apaga con la tecla X; el bioma no transmite información del progreso.
*   [ ] Otros: guía `docs/roadmap/npc-world-biomes.md` y PRs de referencia (front 2026-P4-FE/2026-PIV-TPI-FE#303, back 2026-P4-BE/tpi-roadmap#146). Assets en minúscula `.glb` con su `LICENSE.txt`.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El profesor puede elegir "Isla pirata" en el editor y queda guardado.
*   [ ] **CA2**: El alumno ve la unidad con el terreno, la decoración y el ambiente de la Isla pirata.
*   [ ] **CA3**: Los efectos de ambiente se apagan con X y los mapas de los demás biomas no cambian.
*   [ ] **Extras (opcional)**: edificios propios en `BIOME_BUILDINGS` y personajes que entregan anexos.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Recorrido en el mundo Isla pirata

**Escenario 1**  

*   **Dado**: una sección sin bioma elegido
*   **Cuando**: el profesor le elige Isla pirata
*   **Entonces**: el alumno ve esa unidad en el mundo Isla pirata

**Escenario 2**  

*   **Dado**: una unidad en el mundo Isla pirata con efectos activos
*   **Cuando**: el alumno aprieta X
*   **Entonces**: se apagan los efectos de ambiente y el mapa sigue igual

**Escenario 3**  

*   **Dado**: un alumno con nodos desbloqueados
*   **Cuando**: el profesor cambia el bioma a Isla pirata
*   **Entonces**: ningún estado de nodo ni el XP cambian

* * *

Prototipo
---------

*   **Capturas**: [PEGAR AQUÍ]
*   **URL Figma**: no aplica.
*   **Storybook**: no aplica.
*   **Mock API / Swagger**: [PATCH /api/roadmap/sections/{sectionId}] con el `biome` nuevo; [GET /api/roadmap/courses/{courseId}].

* * *

Estimación / Prioridad
----------------------

**Formato rápido**

*   **Puntos (Fibonacci)**: [a estimar por el equipo]
*   **Prioridad (MoSCoW / Numérica)**: Should

* * *

Dependencias / Impactos
-----------------------

*   Servicios involucrados: front Angular; tpi-roadmap (enum `Biome`).
*   Módulos afectados: front `world-types`, `world-gen`, `world-3d.service`, editor del profesor, mapeos de bioma; back `Biome`.
*   Otros equipos / aprobaciones: ninguno.
*   Impacto en datos / migraciones: ninguno (el bioma se guarda como texto en `section.biome`).
*   Riesgos y mitigación (opcional): conflictos con los otros biomas en los mismos archivos → coordinar el alta de los 6 biomas en un solo PR. Depende de HU-50.

## Tareas

- [x] #7396 T-53.1 Alta del bioma Isla pirata en back y front · Closed · Lautaro Jesus Diego
- [x] #7397 T-53.2 Terreno, decoración y ambiente de la Isla pirata · Closed · Lautaro Jesus Diego
- [x] #7398 T-53.3 Edificios de la Isla pirata · Closed · Lautaro Jesus Diego
- [x] #7399 T-53.4 Personajes custodios y anexos (opcional) · Closed · Lautaro Jesus Diego
- [x] #7400 T-53.5 Tests · Closed · Lautaro Jesus Diego
- [x] #7401 T-53.6 Documentación del bioma · Closed · Lautaro Jesus Diego
