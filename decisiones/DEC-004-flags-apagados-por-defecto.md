---
tags: [tpi, g10, decision, flags, configuracion]
fecha: 2026-10-06
estado: aceptada
reemplaza: ""
---

# DEC-004: Funcionalidad con dependencias externas, apagada por defecto

## Contexto
La sincronización de unidades con Courses (HU-36/17/18) y el roadmap por comisión (HU-44/45) dependían de scopes de servicio, endpoints de Courses y decisiones de producto todavía en curso. Había que poder mergear a `develop` sin cambiar el comportamiento de los entornos que aún no estaban listos.

## Decisión
Cada capacidad con dependencia externa vive detrás de un flag que **arranca apagado**:
- `SECTIONS_SYNC_ENABLED` → `app.sections.sync-enabled=false`: el endpoint `POST /courses/{courseId}/sections/sync` no existe mientras esté apagado.
- `ROADMAP_BY_GROUP_ENABLED` → `app.features.roadmap-by-group.enabled=false`: recorrido, avance, gate (`group_restricted`/`date_restricted`), inicio de desafío y lectura por comisión. Apagado, el gate responde exactamente como la v1.0.
- `KAFKA_TOPIC_CHALLENGE_RESULT_ENABLED` → `app.kafka.topics.challenge-result.enabled=false`: listener legado v1/v2.
Se enciende por entorno, no en código.

## Alternativas descartadas
- **Encender por defecto**: no hay alternativa documentada; el comentario de `application.properties` fija "apagado = comportamiento actual" y que la reconciliación "sigue opt-in hasta habilitarla por entorno".
- **Topic de salida vacío por defecto** (`KAFKA_TOPIC_ROADMAP`): era el mismo patrón, pero se revirtió el 2026-10-11 (default `roadmap.events`).

## Consecuencias
- Positivas: merges seguros, sin romper entornos; el comportamiento previo se conserva.
- Negativas / deuda:
  - **Funcionalidad hecha que no se ve en la demo** si nadie enciende los flags (P0 #3 de la auditoría de Sprint 3: HU-17, 18, 36, 44, 45).
  - Hay que documentar y probar ambas posiciones del flag (`SectionSyncDisabledTest`, `RoadmapGroupPropertiesTest`).
  - Falta decidir cuándo el default pasa a `true`.

## Referencias
- Código / PR / doc: `application.properties` (`app.sections.sync-enabled`, `app.features.roadmap-by-group.enabled`); `6594b26` (2026-10-06); `5560b00` (sync pasa a `app.sections.sync-enabled`, 2026-10-11); `services/groups/RoadmapGroupProperties`.
- `tpi-roadmap/docs/contracts/roadmap-motor-gate-v1.md` (§ historial de versiones), `docs/contracts/courses.md` §7.8.
- Relacionadas: [[acuerdos/courses-g01|Courses]], [[decisiones/DEC-014-comisiones-modelo-b-evaluacion-en-roadmap|DEC-014]].

> [!warning] Pendiente
> La auditoría de Sprint 3 pide encender los flags en la mesh y en la demo. Registrar aquí el cambio de default cuando ocurra.
