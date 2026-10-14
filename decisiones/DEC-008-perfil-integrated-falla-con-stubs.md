---
tags: [tpi, g10, decision, integracion, ht-09]
fecha: 2026-10-03
estado: aceptada
reemplaza: ""
---

# DEC-008: El perfil `integrated` no arranca si queda algún cliente en stub

## Contexto
HT-09 ("sin simulaciones en el micro"): los dobles en memoria y los datos demo ocultaban fallas de integración reales en los entornos compartidos. Antes de T-09.3 los dobles de clientes vivían en `src/main`.

## Decisión
Los clientes externos usan `mode=http` por defecto. Con el perfil `integrated`, `IntegratedClientsValidator` (`ApplicationRunner`) **aborta el arranque** nombrando cada `app.clients.*.mode` distinto de `http` (lost-lives, motor, courses, course-sections, course-materials, course-groups, course-restrictions, course-participants, user-profiles). Los dobles viven en `src/test`; fuera de tests `mode=stub` no publica ningún cliente. Inventario es siempre HTTP, sin modo stub. Se eliminaron simulación, datos demo e `init-mvp` con valores por defecto (fail-closed).

## Alternativas descartadas
- **Dejar los stubs como respaldo silencioso**: oculta indisponibilidades reales (HT-09 regla 3: sin credenciales el cliente degrada con error explícito).
- **Dobles de clientes en `src/main`**: se movieron a `src/test` (T-09.3).

## Consecuencias
- Positivas: las fallas de integración aparecen al arrancar, no en la demo.
- Negativas / deuda:
  - Levantar el micro en integrado exige audience y scope de cada destino configurados.
  - Quedan `@DefaultValue("stub")` en varias `*Properties` sin efecto (limpiar).
  - `ProgressService.startChallenge` quedó sin callers.
  - El mock necesita re-verificarse cuando cambian `clients/`, `events/` o `application.properties`.

## Referencias
- Código / PR / doc: `47dac41` (2026-10-03), `bc2e3d3` (dobles a `src/test`, T-09.3, 2026-10-04), `a639c6e` (`init-mvp` fail-closed, T-09.4, 2026-10-05), `c1ff417` (Inventory sin stub, T-09.5, 2026-10-09), `5560b00` (sin simulación, 2026-10-11), `9de9d7b` (PR #190, 2026-10-12), `clients/IntegratedClientsValidator`.
- `tpi-roadmap/docs/T-03-5-DOBLES-CLIENTES.md`, `Mock_back_micros/tpi-roadmap-mocks/DEUDA.md`.
- Relacionadas: [[acuerdos/plataforma-gateway-kafka|Plataforma]], [[decisiones/DEC-004-flags-apagados-por-defecto|DEC-004]].
