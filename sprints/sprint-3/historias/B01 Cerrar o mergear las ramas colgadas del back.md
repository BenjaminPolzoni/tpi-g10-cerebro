---
tags: [tpi, g10, sprint-3, historia, ht]
id: B01
tipo: HT
epica: "EP-S3-0"
capa: "Back"
esfuerzo: S
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: []
---

# B01: Cerrar o mergear las ramas colgadas del back

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-0 Deuda del Sprint 2|EP-S3-0]] · **HT** · Capa: **Back** · Esfuerzo: **S** · Taiga: Sin cargar
> Estado: **Propuesta**. Al cargarla en Taiga, completar `taiga` y `responsable` en las propiedades.

## Historia

Como equipo quiero decidir cada rama sin mergear del back para que develop sea la única fuente de verdad.

## Qué hay hoy

Hay ramas sin decidir: `feature/t-21-7-roadmap-events-topic` (redundante con #134), `fix/account-not-found-gate` (a revisar contra #193), `bypass-desafio-11-10` (flag de demo) y `revert-130-feature/5390-ranking-rules-parity` (deja el ranking sin tests).

## Criterios de aceptación

- [ ] `feature/t-21-7-roadmap-events-topic` cerrada sin mergear.
- [ ] `fix/account-not-found-gate` probada en el entorno integrado: se mergea si aporta algo que #193 no cubre, o se cierra.
- [ ] `bypass-desafio-11-10` cerrada, o su flag documentado como solo-demo y apagado por defecto.
- [ ] `revert-130-…` cerrada sin mergear.

## Depende de

Nada: se puede empezar ya.

## Dudas que la frenan

- [[sprints/sprint-3/08-dudas|E5]]

## Deuda técnica que cierra

- [[deuda-tecnica|DT-17]]
