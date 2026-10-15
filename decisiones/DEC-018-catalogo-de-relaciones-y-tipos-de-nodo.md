---
tags: [tpi, g10, decision]
fecha: 2026-10-15
estado: aceptada
reemplaza: ""
---

# DEC-018: Catálogo cerrado de relaciones y de tipos de nodo

## Contexto
Los profes pidieron relaciones con tipo ("4 niveles") y que todo sea "completamente personalizable". No estaba claro cuáles eran los tipos de relación (P4), si había subsecciones (P6), si hacían falta reglas combinadas (P7) ni si "personalizable" incluía campos libres o tipos de nodo nuevos (P8).

## Decisión
**Relaciones** (5, cada una con `label` visible y `visible` configurable):
- `requires`: la única que afecta el desbloqueo. El profesor elige si la condición es AND/OR, XP mínimo o las dos, y admite **reglas combinadas** (`A y (B o C)`).
- `recommends`: sugerida, no bloquea.
- `belongs_to`, `related_to` y `part_of`: informativas.

**Tipos de nodo** (cerrados, el profesor no crea tipos nuevos): desafío teórico, desafío práctico, desafío de IA, desafío de recuperación de vida, examen, contenido teórico, inicio y fin. **Inicio y fin son obligatorios** en el curso y en cada unidad/sección.

**Personalizable** = nombre, ícono, descripción y reglas. No hay campos libres (clave-valor).

Las **dependencias** pueden definirse también entre **subsecciones**.

## Alternativas descartadas
- `is_a`, `instance_of`, `located_in`, `has_property` y `causes`: no aportan al recorrido del curso.
- Propiedades libres clave-valor en nodos y secciones: los profes no las piden.
- Solo AND/OR + XP mínimo sin anidar: los profes piden reglas combinadas.

## Consecuencias
- Positivas: el esquema de Neo4j es cerrado y validable; el gate solo evalúa `requires`.
- Negativas / deuda: el código actual (`UNIT`, `CONTENT`, `THEORETICAL_CHALLENGE`, `PRACTICAL_CHALLENGE`, `EXAM`) no tiene desafío de IA, recuperación de vida, `START` ni `END`. HU-60 se redefine y HU-64 se amplía a unidades/secciones.

## Referencias
- Respuestas del 2026-10-15 en [[sprints/sprint-3/08-dudas|08-dudas]] (P4, P6, P7, P8) y el catálogo de relaciones de esa nota.
- [[sprints/sprint-3/04-base-de-grafos|04-base-de-grafos]], [[sprints/sprint-3/historias/HU-65 Relaciones con tipo|HU-65]], [[sprints/sprint-3/historias/HU-64 Nodos de inicio y fin obligatorios|HU-64]], [[sprints/sprint-3/historias/HU-60 Propiedades personalizadas en nodos y secciones|HU-60]].
