---
tags: [tpi, g10, decision, grafo, xp]
fecha: 2026-09-21
estado: aceptada
reemplaza: ""
---

# DEC-011: Se quita el umbral de XP de las secciones (V8): se desbloquea por prerrequisitos

## Contexto
RF-CUR-06 originalmente permitía desbloquear una sección al alcanzar un umbral de XP (`section.xp_threshold`, tabla `section_unlock` de V3). Backoffice expone además PAR-08 ("XP por defecto para desbloqueo", 500) pensado para ese uso. No había usuarios activos con datos que migrar.

## Decisión
RF-CUR-06 se reescribe: el desbloqueo es **solo por prerrequisitos AND/OR** (RF-CUR-06). V6 elimina `section_unlock` y V8 elimina `section.xp_threshold`, para no dejar columnas muertas. **PAR-08 queda fuera de alcance**: no se agrega a la configuración ni se consume.

## Alternativas descartadas
- **Mantener el umbral de XP junto a los prerrequisitos**: columna y tabla sin lectores ni escritores.
- **Consumir PAR-08**: decisión explícita de no hacerlo, documentada en el contrato con Backoffice.

## Consecuencias
- Positivas: un solo mecanismo de desbloqueo, simple de explicar y validar (ciclos, alcance).
- Negativas / deuda:
  - El valor de PAR-08 en Backoffice no tiene consumidor en Roadmap.
  - Quien quiera "desbloquear por XP" tendría que reintroducirlo.

## Referencias
- Código / PR / doc: `54a9e28` (2026-09-21), `V6__drop_section_unlock.sql`, `V8__drop_section_xp_threshold.sql`.
- `tpi-roadmap/docs/contracts/backoffice-par.md` (PAR-08), `docs/contexto.md` §5.1.
- Relacionadas: [[acuerdos/backoffice|Backoffice]], [[decisiones/DEC-010-prerrequisitos-por-seccion-v25|DEC-010]].
