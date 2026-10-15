---
tags: [tpi, g10, taiga, epica]
ref: 70
estado: "New"
responsable: "Sin asignar"
avance: "1/1"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/70
---

# EP-70: Visualización del recorrido

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/70) · Estado: **New** · Responsable: **Sin asignar** · HU cerradas: **1/1**

[G10] — Visualización del recorrido
-----------------------------------

* * *

Objetivo
--------

Que el alumno vea su recorrido como un mapa navegable del grafo, con el estado de cada nodo y la comparativa con su cohorte. Es la misma información que entrega E3, presentada de la forma en que el PRD describe el producto: un mapa a explorar (RF-CUR-01).

* * *

Suposiciones y Restricciones
----------------------------

*   Suposiciones: el grafo ya existe, lo arma el profesor en E1 con nodos, aristas y posiciones. El estado de cada nodo por alumno ya lo calcula E3: el mapa dibuja, no decide, y el estado se valida en el servidor al abrir un nodo. El canvas es propio y queda preparado para extraerse a la librería compartida si se confirma la co-propiedad con Grupo 02.
*   Restricciones (legales/técnicas): 100% escritorio (RF-NFR-05); el canvas no se degrada en móvil, informa que esa sección requiere una computadora. El mapa es una vista, no una fuente de verdad, y no puede habilitar un nodo que la lista no habilita. El MVP entrega el recorrido como lista de unidades con estado (HU-14), que cubre la necesidad funcional sin el costo del grafo interactivo.

* * *

Criterios de Aceptación a nivel Épico
-------------------------------------

*   [ ] El alumno abre su mapa, ve el estado de cada nodo y puede abrir uno habilitado para iniciar su desafío, sin pasar por la lista de unidades.
*   [ ] KPIs iniciales: ningún KPI de producto aplica. El indicador propio es que el mapa se dibuja en menos de 2 segundos con 20 unidades y 120 nodos.
*   [ ] Sin regresiones críticas en E3: el mapa es otra vista del mismo estado de desbloqueo. Abrirlo no altera ningún progreso ni habilita nodos que la lista no habilitaba.
*   [ ] Observabilidad y alertas: métrica de tiempo de render y de errores del canvas en el cliente. Sin alertas de servicio: es una vista, no un endpoint crítico.
*   [ ] Documentación publicada: página de Wiki con la equivalencia entre el mapa y la lista de HU-14, y los componentes del canvas documentados.

* * *

Dependencias / Impactos
-----------------------

*   Servicios / APIs: Usuarios (datos de cohorte para las comparativas), API Gateway.
*   Módulos afectados: vista del recorrido, canvas de grafo, HUD de progreso.
*   Otros equipos: Grupo 02, si se confirma la co-propiedad del canvas dentro de la librería compartida.
*   Impacto en datos / migraciones: ninguno propio. Es una vista sobre entidades que ya existen.
*   Feature toggles / flags: mapa-navegable, un toggle de release que oculta el mapa mientras se construye. Con el flag apagado el alumno usa la lista de unidades de HU-14: los dos muestran exactamente el mismo estado de desbloqueo, el mapa es otra vista y no otra lógica. Plan de retiro: se elimina cuando el mapa sea estable en producción.


## Historias

| HU | Estado | Responsable | Sprint | Tareas |
|---|---|---|---|---|
| [[historias/HU-14 Ver mi recorrido como lista con sus bloqueos\|HU-14]] Ver mi recorrido como lista con sus bloqueos | Done | Fenoglio Santino | G10 - Sprint 2 | 5/5 |
