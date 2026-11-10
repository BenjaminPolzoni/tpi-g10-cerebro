---
tags: [tpi, g10, decision]
fecha: 2026-10-23
estado: aceptada
reemplaza: "La interpretación de HU-11 que hacía implícita la lectura obligatoria como gate de todos los desafíos de la unidad"
---

# DEC-023: Obligatoriedad de unidad y prerrequisitos de nodo

## Contexto

La interpretación previa de HU-11 y del contrato del Gate trataba la lectura de todo contenido obligatorio como condición para iniciar cualquier desafío de la unidad. Eso mezclaba dos reglas: completar una unidad y habilitar un nodo. Además, podía dejar en desacuerdo el Gate, el progreso de nodos y la niebla del mundo.

## Decisión

La política de elegibilidad y desbloqueo pertenece al equipo Roadmap. La marca `mandatory` determina qué nodos cuentan para completar una unidad: se debe leer el contenido obligatorio y superar los desafíos obligatorios. Por sí sola no crea dependencias entre nodos.

El acceso a cada nodo se determina por sus prerrequisitos explícitos (incluidos grupos AND/OR, prerrequisitos de unidad y XP mínimo) y las demás validaciones independientes del Gate. Una lectura satisface un prerrequisito de tipo `CONTENT`; un prerrequisito de desafío requiere su finalización registrada. Si leer un contenido debe habilitar un desafío, el docente configura esa dependencia.

El cálculo consulta el tipo actual del nodo: una lectura histórica satisface un prerrequisito solo mientras el nodo sea de tipo `CONTENT`; si ahora es un desafío, requiere una finalización exitosa. La misma regla aplica a evaluaciones individuales y por lotes.

`content_not_read` se conserva en el vocabulario por compatibilidad, pero no se emite porque quede contenido obligatorio sin leer. Una dependencia explícita pendiente se informa como `prerequisite_pending` o `unit_prerequisite_pending`, según corresponda.

## Coordinación del contrato

Roadmap define y evalúa la elegibilidad. La decisión no cambia la ruta, el envelope, los campos ni los valores que Motor debe poder deserializar; Motor sigue consumiendo `eligible` y reenviando `reason` como texto opaco. No se requiere un cambio de código en Motor.

El cambio sí modifica la semántica de `eligible`. Dado que G09 participó de la revisión de las versiones anteriores del contrato, Roadmap debe notificarle la v1.6 y pedir su revisión como consumidor. La coordinación está pendiente; esta decisión no afirma que G09 ya la haya aprobado.

## Consecuencias

- Un desafío sin prerrequisito de contenido puede iniciarse aunque haya contenido obligatorio sin leer.
- Un desafío que exige explícitamente ese contenido permanece bloqueado hasta que se registre la lectura.
- La finalización de unidad sigue considerando todos los nodos obligatorios.
- Gate, progreso y niebla derivan el bloqueo de las mismas dependencias explícitas.
- El contrato conserva `content_not_read` por compatibilidad, aunque la regla de obligatoriedad ya no lo emite.

## Trazabilidad

- HT-20 / T-20.1 (#9030): Gate y progreso con reglas combinadas.
- HU-19 / T-19.1 (#4282): finalización de unidad por lecturas obligatorias.
- HU-59 / T-59.1 (#9155): reglas explícitas de desbloqueo.
- HU-11 y HU-15: alcance de obligatoriedad y evaluación del Gate; esta decisión reemplaza la interpretación implícita anterior.
- Backend [PR #324](https://github.com/2026-P4-BE/tpi-roadmap/pull/324).
- Frontend [PR #1162](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/1162).

## Referencias

- [[contratos/roadmap-motor-gate-v1]]
- [[sprints/sprint-3/historias/HT-20 Gate y progreso con reglas combinadas y XP mínimo]]
- [[sprints/sprint-3/historias/HU-11 Configurar qué contenidos son de lectura obligatoria]]
