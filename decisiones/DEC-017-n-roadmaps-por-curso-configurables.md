---
tags: [tpi, g10, decision]
fecha: 2026-10-15
estado: aceptada
reemplaza: ""
---

# DEC-017: N roadmaps por curso, con el alcance configurable por el profesor

## Contexto
Las correcciones de los profes decían "el mapa es el curso", y eso chocaba con el pedido de que un curso tenga 1 o más roadmaps (P1 en [[sprints/sprint-3/08-dudas|08-dudas]]). Además no estaba definido si XP, vidas, nivel y ranking eran por curso o por roadmap (P2), cómo se usaban las secciones de Courses (P3), qué roadmaps ve el alumno (P5) ni cómo quedaba el `node_id` que manda el Motor (G8).

## Decisión
Un curso tiene **N roadmaps** y cada uno es un mapa distinto del mismo curso (por grupos, secciones, subsecciones, etc.). El profesor configura por roadmap:
- si XP, vidas, nivel y ranking son **por curso** (compartidos) o **por roadmap** (P2);
- si usa **secciones de Courses** o **secciones propias** (P3);
- si lo ven **todos los alumnos** del curso o se asigna **por comisión** (P5);
- si el **ranking** ordena por **XP** o por **notas** del Motor de desafíos (P14);
- sus **restricciones**, y puede **clonar** el roadmap con ellas para otro grupo o curso (G4).

El `node_id` es **único global**, también después de clonar: la copia genera ids nuevos (G8).

## Alternativas descartadas
- Un solo mapa por curso: descartado por la respuesta a P1.
- Fijar XP, vidas, nivel y ranking por curso o por roadmap: los profes quieren que lo elija el profesor.
- Reusar el `node_id` en los clones: rompería el evento de cierre del Motor, que identifica el nodo solo con `id_course` + `id_node`.

## Consecuencias
- Positivas: HT-17, HU-57, HU-61, HT-19 y HU-66 mantienen su alcance; el contrato con el Motor no cambia.
- Negativas / deuda: varios ajustes nuevos por roadmap que el gate, el ranking y el nivel tienen que respetar. Clonar roadmaps es trabajo nuevo ([[sprints/sprint-3/historias/HU-71 Clonar un roadmap con sus restricciones|HU-71]]).

## Referencias
- Respuestas del 2026-10-15 en [[sprints/sprint-3/08-dudas|08-dudas]] (P1, P2, P3, P5, P14, G4, G8).
- [[sprints/sprint-3/historias/HT-17 Modelo 1 a N de curso a roadmaps|HT-17]], [[sprints/sprint-3/historias/HT-19 Contratos con Courses y el Motor para el modelo 1 a N|HT-19]], [[sprints/sprint-3/historias/HU-61 El alumno elige qué roadmap recorrer|HU-61]].
