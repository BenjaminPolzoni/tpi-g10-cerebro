---
tags: [tpi, g10, taiga, hu]
codigo: HU-56
ref: 7389
estado: "Done"
responsable: "Fenoglio Santino"
epica: "[G10] — Mundos (biomas) del roadmap"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/7389
---

# HU-56: Recorrer la unidad en el mundo Apocalipsis zombie

> [!info] Generado desde Taiga (2026-10-14 18:48). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/7389) · Estado: **Done** · Responsable: **Fenoglio Santino** · Sprint: **G10 - Sprint 2**

[G10] — HU-56 — Recorrer la unidad en el mundo Apocalipsis zombie
----------------------------------------------------------------

* * *

Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ESTUDIANTE
*   **Quiero**: recorrer una unidad en el mundo Apocalipsis zombie, con su propio terreno, decoración y ambiente
*   **Para**: que cada unidad se sienta como un lugar distinto y el recorrido sea más motivador

* * *

Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: nuevo bioma del catálogo cerrado (valor nuevo en el enum `Biome` del back y en el front). Es solo visual: no toca el gate, el progreso ni el XP. Mismo layout que los demás biomas para la misma semilla (no cambiar el orden de `rand()` en `world-gen.ts`). Personajes que entregan anexos y desafío teórico como personaje: opcional, siguiendo la guía.
*   [ ] Validaciones: el bioma nuevo se acepta en el back (POST/PUT/PATCH de sección) y se rechaza cualquier valor fuera del catálogo.
*   [ ] Datos obligatorios: ninguno nuevo (usa `section.biome`, HU-50).
*   [ ] Performance (tiempos, volumen, límites): assets livianos y reutilizados (tinte/tamaño en vez de archivos nuevos); descarga de la unidad no más de un 10 % por encima de pradera.
*   [ ] Seguridad (roles, permisos, datos sensibles): solo el PROFESSOR dueño del curso elige el bioma (HU-50); sin datos sensibles.
*   [ ] Accesibilidad (WCAG/teclado/lectores): todo efecto de ambiente se apaga con la tecla X; sin contenido gráfico violento (estética apta para todo público); el bioma no transmite información del progreso.
*   [ ] Otros: guía `docs/roadmap/npc-world-biomes.md` y PRs de referencia (front 2026-P4-FE/2026-PIV-TPI-FE#303, back 2026-P4-BE/tpi-roadmap#146). Assets en minúscula `.glb` con su `LICENSE.txt`.

* * *

Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El profesor puede elegir "Apocalipsis zombie" en el editor y queda guardado.
*   [ ] **CA2**: El alumno ve la unidad con el terreno, la decoración y el ambiente del Apocalipsis zombie.
*   [ ] **CA3**: Los efectos de ambiente se apagan con X y los mapas de los demás biomas no cambian.
*   [ ] **Extras (opcional)**: edificios propios en `BIOME_BUILDINGS` y personajes que entregan anexos.

* * *

BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Recorrido en el mundo Apocalipsis zombie

**Escenario 1**  

*   **Dado**: una sección sin bioma elegido
*   **Cuando**: el profesor le elige Apocalipsis zombie
*   **Entonces**: el alumno ve esa unidad en el mundo Apocalipsis zombie

**Escenario 2**  

*   **Dado**: una unidad en el mundo Apocalipsis zombie con efectos activos
*   **Cuando**: el alumno aprieta X
*   **Entonces**: se apagan los efectos de ambiente y el mapa sigue igual

**Escenario 3**  

*   **Dado**: un alumno con nodos desbloqueados
*   **Cuando**: el profesor cambia el bioma a Apocalipsis zombie
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

- [x] #7414 T-56.1 Alta del bioma Apocalipsis zombie en back y front · Closed · Fenoglio Santino
- [x] #7415 T-56.2 Terreno, decoración y ambiente del Apocalipsis zombie · Closed · Fenoglio Santino
- [x] #7416 T-56.3 Edificios del Apocalipsis zombie · Closed · Fenoglio Santino
- [x] #7418 T-56.5 Tests · Closed · Fenoglio Santino
- [x] #7419 T-56.6 Documentación del bioma · Closed · Fenoglio Santino
