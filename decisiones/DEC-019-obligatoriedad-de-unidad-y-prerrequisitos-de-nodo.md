---
tags: [tpi, g10, decision]
fecha: 2026-10-23
estado: aceptada
reemplaza: "Interpretación de HU-11 que hacía implícita la lectura obligatoria como gate de todos los desafíos de la unidad"
---

# DEC-019: Obligatoriedad de unidad y prerrequisitos de nodo

## Contexto

El contrato Roadmap–Motor v1.5 y una lectura anterior de HU-11 trataban la lectura de todo contenido obligatorio como condición para iniciar cualquier desafío de la unidad. Eso mezclaba dos reglas distintas: completar una unidad y habilitar un nodo. También podía dejar en desacuerdo el estado del gate, el progreso de nodos y la niebla del mundo.

## Decisión

La política de elegibilidad y desbloqueo pertenece al equipo Roadmap. La marca `mandatory` determina qué nodos cuentan para completar una unidad: se debe leer el contenido obligatorio y superar los desafíos obligatorios. Por sí sola no crea dependencias entre nodos.

El acceso a cada nodo se determina por sus prerrequisitos explícitos (incluidos grupos AND/OR, prerrequisitos de unidad y XP mínimo) y por las demás validaciones independientes del Gate. Una lectura satisface un prerrequisito de tipo `CONTENT`; un prerrequisito de desafío requiere su finalización registrada. Si leer un contenido debe habilitar un desafío, el docente configura esa dependencia.

`content_not_read` se conserva en el vocabulario del contrato y en los enums por compatibilidad, pero no se emite por contenido obligatorio pendiente. Cuando falta una dependencia explícita, el bloqueo es `prerequisite_pending` o `unit_prerequisite_pending`, según corresponda. La misma regla debe reflejarse en el progreso y en la niebla del frontend.

Motor consume `eligible` y reenvía `reason` como texto opaco. No interpreta obligatoriedad ni calcula elegibilidad; esta decisión no cambia el contrato de cable ni requiere una aprobación de implementación de Motor. El equipo Roadmap puede actualizar su propia política y contrato.

## Trazabilidad

- HT-20 / T-20.1 (#9030): Gate y progreso con reglas combinadas.
- HU-19 / T-19.1 (#4282): finalización de unidad por lecturas obligatorias.
- HU-59 / T-59.1 (#9155): reglas explícitas de desbloqueo.
- HU-11 y HU-15: alcance de obligatoriedad y evaluación del Gate; esta decisión reemplaza la interpretación implícita anterior.
- PR Roadmap [#324](https://github.com/2026-P4-BE/tpi-roadmap/pull/324).
- PR frontend coordinada [#1162](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/1162).

## Consecuencias

- Un desafío sin prerrequisito de contenido puede iniciarse aunque haya contenido obligatorio sin leer.
- Un desafío que exige explícitamente ese contenido permanece bloqueado hasta que se registre la lectura.
- La finalización de unidad sigue considerando todos los nodos obligatorios.
- El progreso, el Gate y la niebla deben derivar el bloqueo de las mismas dependencias explícitas.
- El contrato v1.7 mantiene los campos y motivos reconocidos por Motor.

## Referencias

- [[contratos/roadmap-motor-gate-v1]]
- [[sprints/sprint-3/historias/HT-20 Gate y progreso con reglas combinadas y XP mínimo]]
- [[sprints/sprint-3/historias/HU-11 Configurar qué contenidos son de lectura obligatoria]]
