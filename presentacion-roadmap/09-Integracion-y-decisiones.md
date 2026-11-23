---
tags: [presentacion, roadmap]
---

# 9. Cómo se integra y por qué lo diseñamos así

## Lo que decimos

«Ya vimos el recorrido desde tres lugares: la configuración docente, la experiencia del alumno y el seguimiento. Para cerrar, queremos mostrar cómo se conectan esas capacidades con el resto de la plataforma y qué decisiones sostienen nuestra solución.

Primero, Roadmap ofrece una API para consultar y gestionar recorridos, progreso, ranking, elegibilidad y otras capacidades. La aplicación compartida usa esas operaciones para construir las pantallas que acabamos de recorrer. También existen operaciones pensadas para identidades de servicio, con permisos técnicos y contexto de organización. Un ejemplo central es la consulta de elegibilidad que integra nuestro recorrido con el Motor antes de iniciar un desafío.

> [!info]- Detalle técnico: API y M2M
> Las rutas privadas usan el prefijo `/api/roadmap`. En comunicación entre servicios se comprueban scopes y contexto de organización; el gate tiene contrato documentado con Motor. Ver `B/java/com/utn/tpi/roadmap/common/security/RoadmapServiceScopes.java`, `controllers/GateController.java` y [[A2-Endpoints-y-eventos]].

Segundo, intercambiamos eventos mediante Kafka. Courses comunica matrículas, bajas y archivo de cohorte. El Motor comunica resultados y rectificaciones; Accounting aporta señales relacionadas con vidas. Roadmap procesa esos hechos y actualiza su propio estado. A su vez, puede publicar eventos como una actividad completada, un desbloqueo o una insignia obtenida. Esto permite que otros componentes reaccionen a hechos del recorrido sin concentrar toda la lógica en una sola aplicación.

> [!info]- Detalle técnico: Kafka y outbox
> Los listeners despachan eventos. El outbox guarda eventos de dominio en la transacción local y un poller publica y reintenta, con tratamiento de fallos y DLT; idempotencia y entrega se gestionan por mecanismo. Ver `B/java/com/utn/tpi/roadmap/events/outbox/OutboxService.java`, `OutboxPoller.java` y `events/RoadmapEventListener.java`.

Backoffice integra eventos de Roadmap para reporting; no identificamos en su backend un cliente HTTP que consulte salud, resumen o timeline. Es la pantalla de Courses la que consulta el resumen y la evolución de experiencia.

> [!info]- Detalle técnico: consumo comprobado en código
> `_presentacion-src/tpi-backoffice/src/main/java/ar/edu/utn/frc/tup/p4/reporting/consumers/RoadmapEventConsumer.java:11` y `_presentacion-src/fe/src/app/features/courses/data-access/cohort-dashboard.service.ts:37`. El consumidor Kafka depende de configuración y no demuestra tráfico efectivo.

Tercero, elegimos mantener una fuente transaccional de verdad en PostgreSQL y contar con una proyección de estructura en Neo4j para consultas de grafo. Esta separación hace explícito dónde se escriben los datos y cómo se construye una representación orientada a relaciones. La sincronización y la reconciliación son parte del diseño que vincula ambas perspectivas.

> [!info]- Detalle técnico: Neo4j y proyección
> `GraphChangeListener` registra cambios, `RoadmapProjector` sincroniza la proyección y `GraphReadSwitch` selecciona lectura. Las escrituras nativas pueden requerir reconciliación; la convergencia no es instantánea garantizada. Ver `B/java/com/utn/tpi/roadmap/graph/sync/` y `graph/read/`.

La decisión de separar responsabilidades se repite en toda la solución: el docente expresa reglas, Roadmap evalúa el recorrido, el Motor resuelve intentos y Courses conserva la información académica. Sobre esa base construimos una experiencia navegable que combina aprendizaje, juego y seguimiento. Ese es el valor que queremos dejarles: convertir una cursada en un camino claro, visible y acompañado.

En la práctica, esa arquitectura acompaña el viaje que mostramos: una decisión del docente se guarda como parte del recorrido; una consulta evalúa las condiciones de acceso; el Motor comunica un resultado; y Roadmap actualiza los datos que luego ve el alumno o consulta el docente. Cada intercambio tiene una responsabilidad concreta. Eso también facilita explicar de dónde proviene cada dato y qué equipo mantiene la capacidad correspondiente, algo esencial cuando varios servicios participan de una misma experiencia de usuario.

Cada integración aporta una pieza concreta a la experiencia que acabamos de mostrar.

**Transición al cierre:** «Con esto terminamos la demostración y abrimos el espacio para sus preguntas».»

## Qué se ve en pantalla
Volver al mapa y, si hay tiempo, mostrar el diagrama del ecosistema. No simular tráfico real ni presentar el grafo de ejemplo del cerebro como datos de producción.

## Preguntas probables

**¿Neo4j es la fuente de verdad?** No; PostgreSQL es fuente y Neo4j proyección de lectura.

**¿La proyección se actualiza instantáneamente?** No hay garantía de sincronía instantánea; existe reconciliación.

**¿Hay entrega exactamente una vez?** No se garantiza globalmente; hay outbox e idempotencia en caminos específicos.

**¿La existencia de un endpoint prueba consumo externo?** No; hay que comprobar tráfico y configuración en el ambiente.

**¿Qué ocurre si falla una fuente del gate?** Una dependencia necesaria indisponible bloquea el acceso.

**¿El grafo del cerebro es una base en vivo?** No; es una demostración documental con datos simulados.
