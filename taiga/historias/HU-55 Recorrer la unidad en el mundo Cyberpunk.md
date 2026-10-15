---
tags: [tpi, g10, taiga, hu]
codigo: HU-55
ref: 7388
estado: "Done"
responsable: "Benjamin Polzoni"
epicas: "[[epicas/EP-7340 Mundos (biomas) del roadmap|EP-7340]]"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/7388
---

# HU-55: Recorrer la unidad en el mundo Cyberpunk

> [!info] Generado desde Taiga (2026-10-15 16:54). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/7388) · Estado: **Done** · Responsable: **Benjamin Polzoni** · Sprint: **G10 - Sprint 2**
> Épica: [[epicas/EP-7340 Mundos (biomas) del roadmap|EP-7340]] · Tareas cerradas: **6/6**

[G10] — HU-55 — Recorrer la unidad en el mundo Cyberpunk
-------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ESTUDIANTE
*   **Quiero**: recorrer una unidad en el mundo Cyberpunk, con su propio terreno, decoración y ambiente
*   **Para**: que cada unidad se sienta como un lugar distinto y el recorrido sea más motivador

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: nuevo bioma del catálogo cerrado (valor nuevo en el enum `Biome` del back y en el front). Es solo visual: no toca el gate, el progreso ni el XP. Mismo layout que los demás biomas para la misma semilla (no cambiar el orden de `rand()` en `world-gen.ts`). Personajes que entregan anexos y desafío teórico como personaje: opcional, siguiendo la guía.
*   [ ] Validaciones: el bioma nuevo se acepta en el back (POST/PUT/PATCH de sección) y se rechaza cualquier valor fuera del catálogo.
*   [ ] Datos obligatorios: ninguno nuevo (usa `section.biome`, HU-50).
*   [ ] Performance (tiempos, volumen, límites): assets livianos y reutilizados (tinte/tamaño en vez de archivos nuevos); descarga de la unidad no más de un 10 % por encima de pradera.
*   [ ] Seguridad (roles, permisos, datos sensibles): solo el PROFESSOR dueño del curso elige el bioma (HU-50); sin datos sensibles.
*   [ ] Accesibilidad (WCAG/teclado/lectores): todo efecto de ambiente se apaga con la tecla X; luces de neón sin parpadeos rápidos (más de 3 por segundo); el bioma no transmite información del progreso.
*   [ ] Otros: guía `docs/roadmap/npc-world-biomes.md` y PRs de referencia (front 2026-P4-FE/2026-PIV-TPI-FE#303, back 2026-P4-BE/tpi-roadmap#146). Assets en minúscula `.glb` con su `LICENSE.txt`.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El profesor puede elegir "Cyberpunk" en el editor y queda guardado.
*   [ ] **CA2**: El alumno ve la unidad con el terreno, la decoración y el ambiente Cyberpunk.
*   [ ] **CA3**: Los efectos de ambiente se apagan con X y los mapas de los demás biomas no cambian.
*   [ ] **Extras (opcional)**: edificios propios en `BIOME_BUILDINGS` y personajes que entregan anexos.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Recorrido en el mundo Cyberpunk

**Escenario 1**  

*   **Dado**: una sección sin bioma elegido
*   **Cuando**: el profesor le elige Cyberpunk
*   **Entonces**: el alumno ve esa unidad en el mundo Cyberpunk

**Escenario 2**  

*   **Dado**: una unidad en el mundo Cyberpunk con efectos activos
*   **Cuando**: el alumno aprieta X
*   **Entonces**: se apagan los efectos de ambiente y el mapa sigue igual

**Escenario 3**  

*   **Dado**: un alumno con nodos desbloqueados
*   **Cuando**: el profesor cambia el bioma a Cyberpunk
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

- [x] #7408 T-55.1 Alta del bioma Cyberpunk en back y front · Closed · Benjamin Polzoni
- [x] #7409 T-55.2 Terreno, decoración y ambiente Cyberpunk · Closed · Benjamin Polzoni
- [x] #7410 T-55.3 Edificios Cyberpunk · Closed · Benjamin Polzoni
- [x] #7411 T-55.4 Personajes custodios y anexos (opcional) · Closed · Benjamin Polzoni
- [x] #7412 T-55.5 Tests · Closed · Benjamin Polzoni
- [x] #7413 T-55.6 Documentación del bioma · Closed · Benjamin Polzoni
