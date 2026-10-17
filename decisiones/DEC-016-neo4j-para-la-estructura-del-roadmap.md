---
tags: [tpi, g10, decision]
fecha: 2026-10-14
estado: aceptada
reemplaza: ""
---

# DEC-016: Neo4j para la estructura del roadmap

> [!warning] Precisada por [[decisiones/DEC-021-postgres-fuente-de-verdad-neo4j-proyeccion|DEC-021]] (2026-10-17)
> La estructura se **consulta** en Neo4j, pero se **escribe** en Postgres, que es la fuente de verdad. Neo4j es una proyección que se rearma desde Postgres. Las tablas de estructura y sus claves foráneas se mantienen.

## Contexto
Los profes pidieron que el roadmap sea un grafo totalmente configurable: N roadmaps por curso, nodos de inicio y fin, relaciones con tipo (4 niveles) y reglas de desbloqueo combinadas. En las correcciones del 2026-10-14 piden **explícitamente** usar una BD de grafos (ej. Neo4j) en vez de tablas relacionales.

## Decisión
La **estructura** del roadmap (roadmaps, secciones, nodos, relaciones con tipo, reglas y posiciones) pasa a **Neo4j**, en un módulo `graph` dentro de `roadmap-service`. El **estado del alumno** (progreso, XP, vidas, lecturas, insignias, outbox) **se queda en Postgres**. Las dos bases comparten los UUID que genera la app.

## Alternativas descartadas
- Postgres extendido (`jsonb` + CTE): menor riesgo, pero no cumple el pedido de los profes.
- Apache AGE: requiere otra imagen de Postgres en la plataforma y no tiene soporte de Spring Data.
- Micro aparte para el grafo: suma un salto de red en el gate (P95 < 200 ms) y obliga a integrarlo otra vez con el gateway, Eureka y la autenticación.

## Consecuencias
- Positivas: propiedades libres, relaciones con tipo y reglas como subgrafo, todo natural en Neo4j, con consultas de recorrido simples.
- Negativas / deuda: escritura en dos bases sin transacción común (mitigación: solo baja lógica, ids compartidos, job de reconciliación). Infra nueva en la plataforma. Hay que portar los tests de reglas, ciclos y retroactividad.

## Referencias
- [[sprints/sprint-3/04-base-de-grafos]] (análisis y diseño)
- [[sprints/sprint-3/07-correcciones-profes]] (pedido de los profes)
