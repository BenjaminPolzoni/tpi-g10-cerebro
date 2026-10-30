---
tags: [tpi, g10, sprint-4, plan, back, front, roadmap, graph-editor, deuda]
fecha: 2026-10-30
autor: Benjamin Polzoni
estado: propuesta - decisiones abiertas
repo: 2026-P4-BE/tpi-roadmap, 2026-PIV-TPI-FE
antecedentes: Front - editor de grafo unificado del roadmap, FE#1865
---

# Back+Front · Recorrido de las flechas y posición de secciones del roadmap

> **Autor / responsable del plan:** Benjamin Polzoni (`412056-1w3-Polzoni-Benjamin`)
> **Fecha:** 2026-10-30
> **Estado:** propuesta; nada implementado en el back. El front ya funciona con `localStorage` ([FE#1865](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/1865)).
> **Objetivo:** que el recorrido de cada flecha del canvas del editor de grafo (y la posición manual de las secciones) se guarde en el back y llegue con el mapa, en vez de vivir solo en el navegador de cada usuario.

## 1. Situación actual (front)

En el editor de grafo, el docente puede arrastrar los tramos de una flecha y elegir el lado donde conecta (izquierda, derecha, arriba o abajo). Hoy eso se guarda en `localStorage`, con clave por organización, usuario, curso y roadmap (`manualLayoutKey` en `graph-editor-page.component.ts`). Lo mismo pasa con la posición manual de las secciones. Consecuencias: no se ve en otro equipo ni lo ve otro docente, y se pierde al borrar el almacenamiento del navegador.

Código relevante: `domain/map-layout/edge-custom-route.ts` (construye y valida el recorrido), `ui/learning-map-canvas/learning-map-canvas.component.ts` (guarda y lee `edgeRoutes` y los desplazamientos de regiones). Hay un `TODO(tech-debt)` que apunta a esta nota.

## 2. Identidad de una flecha

Las relaciones `requires` **no tienen id propio**: salen de las reglas del nodo destino. Solo las relaciones informativas tienen `relationId`. Por eso la clave de una flecha tiene que ser compuesta:

`kind + sourceType + sourceId + targetType + targetId`

donde `sourceType`/`targetType` son `node` o `section`. Las flechas agrupadas del canvas (varias relaciones en un solo trazo hacia una región oculta) **no se persisten**: son un resultado de la vista, no de los datos.

## 3. Endpoints propuestos

| Método y ruta | Para qué |
| --- | --- |
| `GET /roadmaps/{roadmapId}/layout` | Devuelve `{ version, edges: [...], regions: [...] }`. Separado de `GET /roadmaps/{id}/graph` para poder cachearlo con `ETag`. |
| `PUT /roadmaps/{roadmapId}/layout/edges/{kind}/{sourceId}/{targetId}` | Crea o reemplaza el recorrido de una flecha (idempotente). |
| `DELETE /roadmaps/{roadmapId}/layout/edges/{kind}/{sourceId}/{targetId}` | Vuelve al recorrido automático de esa flecha. |
| `PUT /roadmaps/{roadmapId}/layout` | Guarda todo el layout de una vez con `If-Match: <version>` (lote al terminar un arrastre). |
| `DELETE /roadmaps/{roadmapId}/layout` | Restablece toda la vista. |
| `PUT` y `DELETE /roadmaps/{roadmapId}/layout/regions/{regionId}` | Posición manual de una sección. **Fase 2**, opcional. |

Cuerpo de una flecha:

```json
{
  "sourceType": "node", "targetType": "section",
  "sourceSide": "right", "targetSide": "left",
  "waypoints": [{ "x": 640, "y": 120 }, { "x": 640, "y": 420 }],
  "start": { "x": 480, "y": 120 },
  "end": { "x": 780, "y": 420 },
  "basis": { "source": { "x": 0, "y": 0, "width": 0, "height": 0 }, "target": { "x": 0, "y": 0, "width": 0, "height": 0 } }
}
```

Lados válidos: `left`, `right`, `top`, `bottom`. Las coordenadas son píxeles del mundo del canvas.

## 4. Modelo de datos (tpi-roadmap)

Tabla `roadmap_edge_route`:

| Columna | Detalle |
| --- | --- |
| `roadmap_id`, `kind`, `source_type`, `source_id`, `target_type`, `target_id` | Clave única compuesta |
| `source_side`, `target_side` | Enumerado de 4 lados |
| `waypoints`, `start`, `end`, `basis` | `jsonb` |
| `updated_by`, `updated_at` | Auditoría |

- Se borran en cascada las rutas de nodos o secciones que se eliminan, y las de reglas `requires` que dejan de existir.
- Migración Flyway: revisar la versión contra los PRs abiertos y contra `migration-vendor` antes de elegirla (ya nos pasó en `tpi-roadmap`).
- Permisos: lectura para quien ve el mapa; escritura solo para quien puede editar el roadmap.

## 5. Validaciones y errores

- `422` si: lado inválido, tramos no ortogonales, más de ~32 puntos, números no finitos o fuera de rango, o origen/destino que no existen en ese roadmap.
- `403` sin permiso de edición; `404` si el roadmap no existe.
- `409` si `If-Match` no coincide con la `version` actual (alguien guardó antes).
- Seguir el formato de errores del roadmap (`roadmap-error-message.ts`), con códigos propios tipo `ROADMAP_LAYOUT_*`.

## 6. Cambios en el front

1. Puerto: métodos nuevos en `data-access/roadmap/roadmap-data.port.ts`, con el adaptador HTTP y el adaptador en memoria (`in-memory-roadmap.adapter.ts`).
2. Cargar el layout junto con el grafo y alimentar `edgeRoutes` y los desplazamientos de regiones desde ahí.
3. Guardar con debounce al soltar un arrastre; el botón «Restablecer recorrido» llama al `DELETE` de esa flecha.
4. Migración única: si el back no tiene layout pero hay datos en `localStorage`, enviarlos una vez y borrar los locales.
5. Quitar el `TODO(tech-debt)` y el almacenamiento local al terminar.

## 7. Decisiones abiertas

> [!question] Para decidir antes de implementar
> 1. **¿Compartido o por usuario?** Recomendado: **compartido por roadmap**, porque es la forma del mapa. Implica `version` y manejo de conflictos (`409`) si dos docentes editan. Por usuario es más simple pero cada docente ve un mapa distinto.
> 2. **Coordenadas viejas.** Los puntos son píxeles absolutos y quedan obsoletos si cambia el layout. Propuesta: guardar `basis` (rectángulos de origen y destino al guardar) para que el front descarte la ruta si ya no coincide. Alternativa: guardar solo el lado y un desplazamiento relativo al ancla (más robusto, más trabajo).
> 3. **Clave por roadmap.** La clave es `roadmapId`, para que cada roadmap (y su comisión) pueda ordenar el mapa distinto aunque comparta contenido.

## 8. Fuera de alcance

- Persistir las flechas agrupadas de regiones ocultas.
- Zoom y desplazamiento del canvas (siguen siendo estado de la vista).
- Rutas para el mapa 3D.
