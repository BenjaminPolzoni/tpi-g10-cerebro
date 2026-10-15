---
tags: [tpi, g10, sprint-3, historia, bug]
id: C06
tipo: Bug
epica: "EP-S3-2"
capa: "Back + Front"
esfuerzo: M
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [B02]
---

# C06: Ranking por grupo con error

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-2 Correcciones de los profes|EP-S3-2]] · **Bug** · Capa: **Back + Front** · Esfuerzo: **M** · Taiga: Sin cargar
> Estado: **Propuesta**. Al cargarla en Taiga, completar `taiga` y `responsable` en las propiedades.

## Historia

Como alumno o profesor quiero ver el ranking sin errores, por curso por defecto y filtrable por comisión.

## Qué hay hoy

El back solo tiene ranking por curso (`GET /courses/{id}/ranking`); el avance por grupo es otro endpoint. El front no tiene selector de grupo. El error no está reproducido.

## Criterios de aceptación

- [ ] Error reproducido y documentado (request y respuesta) (E1).
- [ ] El ranking muestra por defecto el del curso.
- [ ] Filtro opcional por comisión.
- [ ] Test que cubre el caso que fallaba.

## Depende de

- [[sprints/sprint-3/historias/B02 Encender los flags en los entornos|B02]] Encender los flags en los entornos

## Dudas que la frenan

- [[sprints/sprint-3/08-dudas|E1]]
- [[sprints/sprint-3/08-dudas|P10]]
- [[sprints/sprint-3/08-dudas|P14]]
