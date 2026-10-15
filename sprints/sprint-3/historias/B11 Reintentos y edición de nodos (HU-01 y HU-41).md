---
tags: [tpi, g10, sprint-3, historia, hu]
id: B11
tipo: HU
epica: "EP-S3-0"
capa: "Back"
esfuerzo: M
estado: Propuesta
responsable: ""
taiga: "HU-01, HU-41"
depende: []
---

# B11: Reintentos y edición de nodos (HU-01 y HU-41)

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-0 Deuda del Sprint 2|EP-S3-0]] · **HU** · Capa: **Back** · Esfuerzo: **M** · Taiga: [[taiga/historias/HU-01 Crear nodos en el grafo (unidades, contenidos, desafíos, exámenes)|HU-01]], [[taiga/historias/HU-41 Editar un nodo del roadmap de forma individual|HU-41]]
> Estado: **Propuesta**. Al cargarla en Taiga, completar `taiga` y `responsable` en las propiedades.

## Historia

Como profesor quiero definir cuántos reintentos tiene un desafío y editar un nodo sin perder su configuración.

## Qué hay hoy

No existe el campo `reintentos_permitidos`. Un PUT sin `lives_policy` resetea el nodo a STANDARD. No se consume la baja de desafío del Motor (CA8 de HU-01).

## Criterios de aceptación

- [ ] Campo de reintentos (0..PAR-13) en el nodo, validado.
- [ ] Un PUT que no trae `lives_policy` conserva el valor actual.
- [ ] Si el Motor da de baja un desafío, el nodo queda marcado y el profesor lo ve.
- [ ] Coordinar con M03: si el nodo pasa a Neo4j, el campo va ahí.

## Depende de

Nada: se puede empezar ya.

## Dudas que la frenan

Ninguna.
