---
tags: [tpi, g10, taiga, epica]
ref: 60
estado: "Done"
responsable: "Mateo Delgado Costa"
avance: "5/5"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/60
---

# EP-60: Progreso y desbloqueo

> [!info] Generado desde Taiga (2026-10-14 20:45). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/60) · Estado: **Done** · Responsable: **Mateo Delgado Costa** · HU cerradas: **5/5**

[G10] — Progreso y desbloqueo
-----------------------------

* * *

Objetivo
--------

Que el avance del alumno esté gobernado por reglas únicas y verificables —prerrequisitos AND/OR, contenido obligatorio leído y vidas— consultables como gate bloqueante por los tres equipos de desafíos antes de aceptar una entrega. El XP se suma al ledger propio; las vidas se leen a Inventario; el cálculo lo hace el Motor. Nada se calcula ni se emite acá.

* * *

Suposiciones y Restricciones
----------------------------

*   Suposiciones: el desbloqueo se produce por desafío específico aprobado, con bifurcación, y el profesor elige AND/OR por nodo (D-01, RF-CUR-06 reescrito). PAR-08 queda retirado. El gate es bloqueante y responde con el vocabulario v3: no\_inscripto, contenido\_no\_leido, prerrequisito\_pendiente, sin\_vidas y recuperacion\_pendiente (breaking change acordado con Grupo 09, D-HU15). Sin vidas sólo se permite el desafío de recuperación (RF-REC-04) y los desafíos LLM. Roadmap NO calcula ni emite XP: el Motor envía xpOtorgado ya calculado, con el bonus de ítem si aplica, y nosotros lo sumamos a xp\_movement. Degradación: si Inventario o Accounting no responden, el gate responde habilitado:false con motivo origen\_no\_disponible (extensión pendiente de acuerdo con G09, F5; excepción documentada a RF-NFR-04).
*   Restricciones (legales/técnicas): P95 ≤ 200 ms con 120 consultas concurrentes (RF-NFR-03). El gate es bloqueante, no un aviso. Los desbloqueos alcanzados no se revierten (RF-CFG-06) y los ajustes posteriores del Motor (REQ-MOT-04) generan un movimiento nuevo, nunca una edición. El consumo del bus es idempotente por eventId: el replay con auto-offset-reset earliest es no-op, y esRepeticion=true se descarta conservando la primera solución (REQ-MOT-03). Sin hardcodeo de parámetros.

* * *

Criterios de Aceptación a nivel Épico
-------------------------------------

*   [ ] Un alumno sin la lectura obligatoria recibe contenido\_no\_leido; sin el prerrequisito, prerrequisito\_pendiente; sin vidas, sin\_vidas salvo que sea recuperación; y sin respuesta del origen externo, no habilitado. Nunca un error genérico. Reprocesar diez veces el mismo evento de XP deja el ledger idéntico a procesarlo una vez.
*   [ ] KPIs iniciales: ningún KPI de producto aplica. El indicador propio es la latencia del gate, P95 por debajo de 200 ms con 120 consultas concurrentes, porque está en el camino crítico de toda entrega de la plataforma.
*   [ ] Sin regresiones críticas en E1 y E2: cambiar el grafo, la obligatoriedad de un contenido o un prerrequisito no altera ningún movimiento de XP existente ni revierte desbloqueos ya alcanzados.
*   [ ] Observabilidad y alertas: contadores de respuestas del gate por motivo y latencia P95, más contador de eventos consumidos, deduplicados y enviados a DLQ. Alerta ante degradación de un origen externo y ante latencia por encima de 200 ms: un gate caído bloquea las entregas de toda la plataforma, no sólo las nuestras.
*   [ ] Documentación publicada: los cinco motivos publicados como contrato versionado en OpenAPI y acordados por escrito con los tres equipos de desafíos, más el envelope del bus documentado en la Wiki.

* * *

Dependencias / Impactos
-----------------------

*   Servicios / APIs: Inventario (vidas), Motor de Desafíos, Prácticos y Teóricos (consumidores del gate), Backoffice (PAR-09 y PAR-12), API Gateway.
*   Módulos afectados: reglas de desbloqueo por nodo, estado de progreso por alumno, gate de habilitación, ledger xp\_movement, consumidor Kafka.
*   Otros equipos: los equipos dependientes de desafío deben integrar el gate antes de cerrar su ciclo de entrega — es su bloqueante. Inventario y Accounting son el nuestro. El delta/total de los ajustes posteriores queda pendiente de acuerdo con Grupo 09.
*   Impacto en datos / migraciones: reglas por nodo, estado por alumno y caché con expiración. Ledger xp\_movement append-only. Sin tablas propias nuevas salvo seleccion\_item. Consumo del bus con group-id roadmap-service y DLQ según P-09.
*   Feature toggles / flags: el gate en sí no se apaga. Lo que hay es un kill-switch que fuerza no-habilitado si se rompe el contrato con un origen externo. Un flag que dejara pasar entregas no sería reversible: RF-CFG-06 no permite recalcular hacia atrás, así que el XP mal otorgado quedaría. Plan de retiro: el kill-switch es permanente, es un control de operación y no un toggle de release.


## Historias

| HU | Estado | Responsable | Sprint | Tareas |
|---|---|---|---|---|
| [[historias/HU-13 Configurar las reglas de desbloqueo de una unidad (prerrequisitos AND-OR)\|HU-13]] Configurar las reglas de desbloqueo de una unidad (prerrequisitos AND-OR) | Done | Ludmila Mailen Cejas | G10 - Sprint 1 | 6/6 |
| [[historias/HU-15 Impedir la entrega en un nodo bloqueado (gate, vocabulario v3)\|HU-15]] Impedir la entrega en un nodo bloqueado (gate, vocabulario v3) | Done | Baltasar Rodriguez Teruel | G10 - Sprint 1 | 8/8 |
| [[historias/HU-03 Consumir el resultado del Motor y registrar XP y progreso\|HU-03]] Consumir el resultado del Motor y registrar XP y progreso | Done | Benjamin Polzoni | G10 - Sprint 1 | 5/5 |
| [[historias/HU-16 Integración real con Inventario para las vidas del gate\|HU-16]] Integración real con Inventario para las vidas del gate | Done | Lautaro Jesus Diego | G10 - Sprint 2 | 5/5 |
| [[historias/HU-48 Saber si puedo entrar a un desafío antes de abrirlo\|HU-48]] Saber si puedo entrar a un desafío antes de abrirlo | Done | Mateo Delgado Costa | Backlog | 4/8 |
