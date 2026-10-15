---
tags: [tpi, g10, sprint-3, historia, hu]
id: B06
tipo: HU
epica: "EP-S3-0"
capa: "Back"
esfuerzo: M
estado: Propuesta
responsable: ""
taiga: "HU-15, HU-16"
depende: []
---

# B06: Gate con origen no disponible y dato stale (HU-15 y HU-16)

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-0 Deuda del Sprint 2|EP-S3-0]] · **HU** · Capa: **Back** · Esfuerzo: **M** · Taiga: [[taiga/historias/HU-15 Impedir la entrega en un nodo bloqueado (gate, vocabulario v3)|HU-15]], [[taiga/historias/HU-16 Integración real con Inventario para las vidas del gate|HU-16]]
> Estado: **Propuesta**. Al cargarla en Taiga, completar `taiga` y `responsable` en las propiedades.

## Historia

Como alumno quiero un motivo claro cuando no puedo entrar porque otro servicio está caído.

## Qué hay hoy

Si Accounting o Courses no responden, el gate devuelve 503 en vez del motivo `origen_no_disponible`. La pantalla de inventario usa el último dato de 24 h con `stale`, pero el gate no (y no debe usarlo para habilitar).

## Criterios de aceptación

- [ ] Con Accounting caído y sin caché vigente, el gate responde `eligible=false`, `reason=origen_no_disponible` (fail-closed, DEC-003).
- [ ] El gate nunca habilita con un dato `stale`.
- [ ] Tests para Accounting caído, Courses caído y caché vencida.

## Depende de

Nada: se puede empezar ya.

## Dudas que la frenan

- [[sprints/sprint-3/08-dudas|E9]]
