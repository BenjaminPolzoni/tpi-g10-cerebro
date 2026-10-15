# HU-02 / HU-13 — Baja de nodo con dependientes y arista huérfana (PROPUESTA)

> Estado: propuesta del equipo Roadmap, **no aprobada**. No implementar hasta
> que el PO / la cátedra la valide. Si se aprueba, agregar como criterio de
> aceptación de HU-02 (editor) y HU-13 (PATCH de reglas), y cargar en Taiga.

## Contexto
N3.3 exige a N3.2 como prerrequisito; N3.2 se da de baja. La arista queda
huérfana: quien ya había superado N3.2 conserva el desbloqueo (G10-E1), pero
quien no lo superó queda bloqueado para siempre salvo intervención.

## Criterio propuesto
1. El sistema **nunca convierte la ambigüedad estructural en decisión
   automática**: sin borrado en cascada de aristas y sin dar el prerrequisito
   por satisfecho (patrón HU-02 escenario 2 y RF-RNK-10: confirmación explícita
   del profesor).
2. Evaluación literal hasta que el profesor actúe: prerrequisito no superado =
   nodo bloqueado (`prerequisite_pending` en HU-15) con mensaje que orienta
   a la acción del profesor.
3. Desbloqueo solo por acción explícita del profesor: re-cablear la arista o
   confirmar la baja con dependientes en el editor (HU-02) / PATCH (HU-13).
4. Eliminar o modificar un desafío ya realizado invalida los intentos previos
   (`ATTEMPT_CANCELED`) **sin** quitar XP ni completados ya alcanzados:
   la anulación futura es un movimiento compensatorio append-only, nunca un
   update ni un borrado (RF-CFG-06, RF-NFR-01).

## Trazabilidad
- RF-NFR-01 (baja lógica sin excepciones, en toda entidad propia),
  RF-CUR-05, RF-CFG-06, G10-E1.
- `V9__course_cohort_and_soft_delete.sql` ya deja `deleted_at` en
  `completed_node` y `xp_movement` para este futuro.
