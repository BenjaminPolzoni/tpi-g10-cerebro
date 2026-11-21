---
tags: [presentacion, roadmap]
---

# A3. Decisiones comprobadas en código

| Decisión | Alcance verificable | Referencia |
|---|---|---|
| Fuente transaccional y proyección | Postgres es fuente; Neo4j es proyección reconstruible, no sincronía instantánea garantizada | `C/decisiones/DEC-016-neo4j-para-la-estructura-del-roadmap.md`, `DEC-021-postgres-fuente-de-verdad-neo4j-proyeccion.md`; `B/java/com/utn/tpi/roadmap/graph/sync/RoadmapProjector.java` |
| Relaciones y reglas | Dependencias bloqueantes y relaciones informativas; árbol AND/OR | `C/decisiones/DEC-018-catalogo-de-relaciones-y-tipos-de-nodo.md`; `B/java/com/utn/tpi/roadmap/rules/RuleEvaluator.java` |
| Gate falla cerrado | Origen necesario indisponible no habilita | `B/java/com/utn/tpi/roadmap/services/GateService.java` |
| Eventos con outbox | Cambio y encolado local transaccional; publicación posterior | `B/java/com/utn/tpi/roadmap/events/outbox/OutboxService.java` |
| Resultado desde Motor | XP recibido y ledger con idempotencia; rectificaciones por delta | `B/java/com/utn/tpi/roadmap/services/ProgressService.java` |
| Ranking y presentación | Back comparte puestos; front usa numeración consecutiva y sus zonas | `C/decisiones/DEC-022-ranking-front-vistas-y-desempate.md`; `B/java/com/utn/tpi/roadmap/services/RankingRules.java`; `F/app/features/ranking/domain/ranking.rules.ts` |
| Múltiples recorridos | Principal y alternativas con configuración, audiencia y archivo | `B/java/com/utn/tpi/roadmap/services/RoadmapManagementService.java` |

Los documentos históricos describen intención; solo el código inspeccionado demuestra presencia, no despliegue o integración. La demo de `C/demo-neo4j/` es sintética y no está sincronizada con bases.
