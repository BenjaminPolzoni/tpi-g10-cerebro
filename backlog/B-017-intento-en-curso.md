# B-017 — Intento en curso sobre nodo dado de baja (PROPUESTA)

> Estado: propuesta del equipo Roadmap, **no aprobada**. No implementar hasta
> que el PO / la cátedra la valide. Si se aprueba, volcar el criterio a la HU
> que corresponda y a Taiga.

## Contexto
Nodo habilitado (ni completado ni bloqueado) con un intento en curso en el
motor, cuando el profesor da de baja el nodo o el desafío se elimina/modifica.
Sin regla en PRD ni backlog: ¿el intento queda huérfano, se redirige al alumno
o pierde el camino?

## Criterio propuesto
1. La API responde error (el nodo dado de baja no existe para el roadmap:
   `404 node.not-found` vía baja lógica; no se inventa un `410`).
2. El cliente redirige al roadmap y muestra el error. Nada queda huérfano en
   silencio.
3. XP y desbloqueos ya alcanzados se conservan (G10-E1, RF-CFG-06: todo rige
   hacia adelante, nunca retroactivo).

## Trazabilidad
- RF-NFR-01 (baja lógica, sin borrado físico), RF-CUR-05 (editable aun en uso),
  RF-CFG-06 (sin recálculo retroactivo), criterio G10-E1.
- Evento relacionado: `ATTEMPT_CANCELED` del motor (el intento pierde validez;
  ver propuesta HU-02/HU-13).

## Pregunta residual
Correlación del cancel con el intento original (`attempt_number` vs referencia
explícita) y orden de llegada con at-least-once: a acordar con el equipo motor
en #9.
