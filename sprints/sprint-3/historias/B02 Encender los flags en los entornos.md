---
tags: [tpi, g10, sprint-3, historia, ht]
id: B02
tipo: HT
epica: "EP-S3-0"
capa: "Infra"
esfuerzo: S
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: []
---

# B02: Encender los flags en los entornos

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-0 Deuda del Sprint 2|EP-S3-0]] · **HT** · Capa: **Infra** · Esfuerzo: **S** · Taiga: Sin cargar
> Estado: **Propuesta**. Al cargarla en Taiga, completar `taiga` y `responsable` en las propiedades.

## Historia

Como equipo quiero los flags `SECTIONS_SYNC_ENABLED` y `ROADMAP_BY_GROUP_ENABLED` encendidos en la mesh y en la demo para que funcione lo que ya está hecho.

## Qué hay hoy

Los dos flags están en `false` por defecto (DEC-004). Con eso apagado no andan HU-17, 18, 36, 44 y 45.

## Criterios de aceptación

- [ ] Los dos flags en `true` en el compose de la mesh y de la demo.
- [ ] Con los flags encendidos, el sync de secciones y el roadmap por comisión responden sin error en el entorno integrado.
- [ ] Si algo falla al encenderlos, queda anotado como bug con su HU.

## Depende de

Nada: se puede empezar ya.

## Dudas que la frenan

- [[sprints/sprint-3/08-dudas|E6]]

## Deuda técnica que cierra

- [[deuda-tecnica|DT-20]]
