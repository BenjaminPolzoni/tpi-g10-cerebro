---
tags: [tpi, g10, sprint-3, historia, hu]
id: B04
tipo: HU
epica: "EP-S3-0"
capa: "Back"
esfuerzo: M
estado: Propuesta
responsable: ""
taiga: "HU-48"
depende: []
---

# B04: Pre-chequeo de elegibilidad para el alumno (HU-48)

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-0 Deuda del Sprint 2|EP-S3-0]] · **HU** · Capa: **Back** · Esfuerzo: **M** · Taiga: [[taiga/historias/HU-48 Saber si puedo entrar a un desafío antes de abrirlo|HU-48]]
> Estado: **Propuesta**. Al cargarla en Taiga, completar `taiga` y `responsable` en las propiedades.

## Historia

Como alumno quiero saber antes de entrar a un desafío si puedo hacerlo y, si no, por qué.

## Qué hay hoy

El gate (`/eligibility`) solo lo puede llamar otro servicio. El front no tiene cómo preguntarlo con el JWT del alumno. `ProgressService.startChallenge` quedó como código muerto.

## Criterios de aceptación

- [ ] Existe un endpoint para el alumno con su JWT, sin `studentId` en la ruta (se toma de `X-User-Id`).
- [ ] Devuelve lo mismo que el gate (`eligible` y `reason`) usando el mismo evaluador.
- [ ] No crea intentos ni modifica nada.
- [ ] `ProgressService.startChallenge` borrado.
- [ ] Test BDD: alumno sin vidas → `eligible=false`, `reason=no_lives`.

## Depende de

Nada: se puede empezar ya.

## Dudas que la frenan

Ninguna.

## Deuda técnica que cierra

- [[deuda-tecnica|DT-04]]
