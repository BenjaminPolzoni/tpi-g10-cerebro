---
tags: [tpi, g10, taiga, epica]
ref: 69
estado: "New"
responsable: "Sin asignar"
avance: "3/3"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/69
---

# EP-69: Logros e insignias

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/69) · Estado: **New** · Responsable: **Sin asignar** · HU cerradas: **3/3**

[G10] — Logros e insignias
--------------------------

* * *

Objetivo
--------

Administrar el catálogo de insignias de cada curso y otorgarlas automáticamente al cumplirse su criterio, para dar reconocimiento visible al esfuerzo y alimentar el primer criterio de desempate del ranking (RF-RNK-11).

* * *

Suposiciones y Restricciones
----------------------------

*   Suposiciones: Roadmap es dueño del catálogo completo —nombre, ícono y criterio— y evalúa el criterio contra su propio progreso. Los criterios de XP se evalúan contra el ledger propio y los de vidas se consultan a Inventario, nunca con un dato inventado. La evaluación ocurre después de cada actualización relevante de progreso, no en un proceso nocturno. Una insignia se otorga una sola vez por alumno y el catálogo de tipos de criterio es cerrado. La racha de E5 es un criterio válido: por ejemplo, 50 días consecutivos otorgan una insignia.
*   Restricciones (legales/técnicas): las insignias son cosméticas y de prestigio, sin efecto mecánico sobre los desafíos, que es exclusivo del equipamiento (RF-REC-02 y RF-REC-03). No confundirlas con las insignias destacadas que el alumno elige mostrar en su perfil: eso es personalización y lo resuelve Mercado en Fase 2; nosotros llevamos el conteo real. El catálogo es por curso-cohorte.

* * *

Criterios de Aceptación a nivel Épico
-------------------------------------

*   [ ] Un profesor define una insignia con su criterio —por ejemplo, completar una unidad con todo el contenido obligatorio leído— y el sistema la otorga sola, sin intervención manual. Cumplir dos veces el mismo criterio la otorga una sola vez.
*   [ ] KPIs iniciales: ningún KPI de producto aplica. El indicador propio es de consistencia: el conteo de insignias por alumno coincide siempre con las efectivamente otorgadas, que es lo que consume el primer criterio de desempate del ranking (RF-RNK-11).
*   [ ] Sin regresiones críticas en E6: el desempate del ranking sigue ordenando igual después de cada otorgamiento, sin recalcular posiciones ya consolidadas.
*   [ ] Observabilidad y alertas: log de cada otorgamiento con alumno, insignia y criterio que lo disparó. Alerta si un mismo alumno recibe dos veces la misma insignia.
*   [ ] Documentación publicada: catálogo de tipos de criterio soportados en la Wiki y el evento BADGE\_AWARDED documentado según el envelope del PDF del bus (eventType en SNAKE inglés, decisión D-KAFKA) para Notificaciones.

* * *

Dependencias / Impactos
-----------------------

*   Servicios / APIs: Notificaciones (consume el evento BADGE\_AWARDED), Inventario (criterios basados en vidas; el XP sale del ledger propio), Mercado (insignias destacadas del perfil, Fase 2).
*   Módulos afectados: catálogo de insignias, evaluador de criterios, desempate del ranking.
*   Otros equipos: Notificaciones debe confirmar el topic y la key del evento (P-09). Mercado y nosotros debemos acordar el límite entre conteo real y destacadas de perfil.
*   Impacto en datos / migraciones: tablas insignia\_catalogo (con tipo de criterio y sus parámetros) e insignia\_otorgada. Sin datos históricos que migrar.
*   Feature toggles / flags: insignias-otorgamiento, que cubre la evaluación automática de criterios. Con el flag apagado se carga el catálogo pero no se otorga nada y el desempate cae al segundo criterio. Es seguro apagarlo porque el criterio se evalúa contra nuestro propio progreso: al encenderlo se otorgan retroactivamente las insignias ya ganadas, a diferencia del XP. Plan de retiro: se elimina cuando el evaluador sea estable en producción.


## Historias

| HU | Estado | Responsable | Sprint | Tareas |
|---|---|---|---|---|
| [[historias/HU-20 Definir el catálogo de insignias del curso\|HU-20]] Definir el catálogo de insignias del curso | Done | Benjamin Polzoni | G10 - Sprint 2 | 7/7 |
| [[historias/HU-21 Otorgar insignias automáticamente\|HU-21]] Otorgar insignias automáticamente | Done | Ludmila Mailen Cejas | G10 - Sprint 2 | 6/6 |
| [[historias/HU-22 Ver mis insignias\|HU-22]] Ver mis insignias | Done | Ludmila Mailen Cejas | G10 - Sprint 2 | 5/5 |
