---
tags: [tpi, g10, indice]
---

# Cerebro G10 — roadmap-service

Todo lo que el grupo necesita saber sin tener que preguntarle a nadie: qué está hecho, qué falta, qué se acordó con otros grupos y por qué se decidió cada cosa.

```mermaid
flowchart LR
  T[Taiga] -->|scripts/taiga_sync.py| TG[taiga/]
  TG --> S[sprints/]
  A[acuerdos/] --> S
  D[decisiones/] --> S
  M[minutas/] --> A
  M --> D
```

## Secciones

| Carpeta | Qué hay | Quién la mantiene |
|---|---|---|
| [[taiga/README\|taiga/]] | Épicas, historias y tareas de G10, con estado y responsable | **Generada** por `scripts/taiga_sync.py`. No editar a mano |
| [[sprints/sprint-3/00-indice\|sprints/]] | Planificación y análisis por sprint. Hoy: propuesta del Sprint 3 | El equipo |
| [[acuerdos/README\|acuerdos/]] | Una nota por grupo o servicio con el que integramos: qué se acordó, contrato, pendientes | El equipo, cada vez que se acuerda algo |
| [[decisiones/README\|decisiones/]] | Decisiones técnicas (DEC-xxx): contexto, alternativas y consecuencias | El equipo |
| [[arquitectura/cors-topics-rutas\|arquitectura/]] | Cómo funciona el micro por dentro: CORS, topics de Kafka y rutas que manejamos hoy | El equipo, cuando cambie el código |
| `minutas/` | Notas de reuniones (daily, profes, otros grupos) | Quien estuvo en la reunión |
| [[deuda-tecnica]] | Deuda técnica general (no son HU): código muerto, mocks, seguridad, docs, ramas. Vive entre sprints | El equipo |
| [[equipo]] | Integrantes, áreas que conoce cada uno | El equipo |
| `plantillas/` | Plantillas para acuerdo, decisión y minuta | — |

## Lo urgente ahora

- [[sprints/sprint-3/02-pendientes|Pendientes del Sprint 2]]: historias en Done que no lo están.
- [[deuda-tecnica|Deuda técnica]]: lo que hay que limpiar aunque no sea una HU. Empezar por las 🔴.
- [[sprints/sprint-3/08-dudas|Dudas del sprint]]: para los profes, otros grupos y el equipo. Empezar por las 🔴.
- [[sprints/sprint-3/07-correcciones-profes|Correcciones de los profes]]: qué piden y qué ya estaba planteado.
- [[decisiones/DEC-016-neo4j-para-la-estructura-del-roadmap|DEC-016: Neo4j para la estructura del roadmap]].

## Reglas del cerebro

1. **Si se acordó algo con otro grupo, va a `acuerdos/`** el mismo día, con link al contrato o al mensaje.
2. **Si se decidió algo técnico que alguien podría cuestionar después, va a `decisiones/`.**
3. **Taiga es la fuente de verdad del estado de las HU.** Para actualizar `taiga/`, correr el script. No editar esas notas.
4. **Los contratos técnicos viven en el repo del back** (`tpi-roadmap/docs/contracts/`). Acá se enlazan y se resumen, no se copian.
5. Antes de preguntar en el grupo, buscar acá (`Ctrl/Cmd + Shift + F`).
   - ¿Qué es CORS, qué topics usamos, cómo son las rutas? → [[arquitectura/cors-topics-rutas]].

Cómo instalarlo y sincronizarlo: [[COMO-USAR]].
