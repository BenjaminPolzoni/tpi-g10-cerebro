---
tags: [presentacion, roadmap]
---

# A5. Glosario

| Término | En una frase | Referencia |
|---|---|---|
| Cohorte | Cursada identificada por `courseId`; no necesariamente comisión | `B/docs/API-ENDPOINTS.md` |
| Roadmap | Variante del recorrido de una cohorte | `B/java/com/utn/tpi/roadmap/services/RoadmapManagementService.java` |
| Nodo | Actividad o límite de estructura | `B/java/com/utn/tpi/roadmap/models/NodeType.java` |
| Gate | Consulta de elegibilidad previa al intento | `B/java/com/utn/tpi/roadmap/controllers/GateController.java` |
| AND / OR | Todas las condiciones / alguna alternativa | `B/java/com/utn/tpi/roadmap/rules/RuleEvaluator.java` |
| Neo4j / proyección | Base orientada a grafos / copia derivada de lectura | `B/java/com/utn/tpi/roadmap/graph/sync/RoadmapProjector.java` |
| Kafka / outbox | Transporte de eventos / registro local transaccional para publicarlos | `B/java/com/utn/tpi/roadmap/events/outbox/OutboxService.java` |
| ETag | Versión usada para controlar escritura concurrente de layout | `B/java/com/utn/tpi/roadmap/controllers/RoadmapLayoutController.java` |
| M2M | Comunicación autorizada entre identidades de servicio | `B/java/com/utn/tpi/roadmap/common/security/RoadmapServiceScopes.java` |
| Ledger / XP | Registro de movimientos de experiencia | `B/java/com/utn/tpi/roadmap/entities/XpMovementEntity.java` |
| reached_first | Fecha registrada para desempatar, no necesariamente instante real del logro | `B/java/com/utn/tpi/roadmap/services/RankingService.java` |
| DLT | Destino de mensajes fallidos según política del mecanismo | `B/java/com/utn/tpi/roadmap/events/outbox/OutboxPoller.java` |
| Zona | Región visual del mundo o clasificación relativa de ranking; no confundir | `F/app/features/roadmap/domain/world-gen/from-nodes.ts`; `B/java/com/utn/tpi/roadmap/services/RankingRules.java` |
