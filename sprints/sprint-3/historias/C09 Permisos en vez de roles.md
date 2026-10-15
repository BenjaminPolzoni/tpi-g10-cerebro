---
tags: [tpi, g10, sprint-3, historia, ht]
id: C09
tipo: HT
epica: "EP-S3-2"
capa: "Back"
esfuerzo: M
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: []
---

# C09: Permisos en vez de roles

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-2 Correcciones de los profes|EP-S3-2]] · **HT** · Capa: **Back** · Esfuerzo: **M** · Taiga: Sin cargar
> Estado: **Propuesta**. Al cargarla en Taiga, completar `taiga` y `responsable` en las propiedades.

## Historia

Como equipo quiero autorizar por permisos y no por roles, con el catálogo de G06.

## Qué hay hoy

Las reglas usan `hasRole`/`hasAnyRole` en constantes por controller (`CAN_EDIT`, `CAN_VIEW`…), más chequeos a mano en `RankingController` y `requireOwner`. El gate acepta cualquier servicio sin validar el scope `roadmap.gate.read`.

## Criterios de aceptación

- [ ] Matriz rol → permisos escrita (DT-03) y acordada con G06.
- [ ] Cada `@PreAuthorize` usa `hasAuthority('roadmap.…')`.
- [ ] Los chequeos a mano pasan a permisos + chequeo de dueño del curso.
- [ ] El gate valida el scope `roadmap.gate.read` (DT-01).
- [ ] Tests de autorización por endpoint.

## Depende de

Nada: se puede empezar ya.

## Dudas que la frenan

- [[sprints/sprint-3/08-dudas|G2]]
- [[sprints/sprint-3/08-dudas|G6]]

## Deuda técnica que cierra

- [[deuda-tecnica|DT-01]]
- [[deuda-tecnica|DT-02]]
- [[deuda-tecnica|DT-03]]
