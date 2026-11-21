---
tags: [presentacion, roadmap]
---

# 3. El docente construye el camino

## Lo que decimos

«Estamos en el editor docente. Acá vemos la estructura de unidades y actividades, y podemos transformar una secuencia de contenidos en un recorrido con sentido. Vamos a tomar un ejemplo didáctico del cerebro del equipo: el contenido Variables, dos alternativas de evaluación y una Práctica integradora. Es un ejemplo simulado que nos sirve para explicar claramente las reglas.

Primero ubicamos los dos elementos que queremos relacionar. Elegimos el nodo que va a actuar como requisito y el nodo que depende de él. En la interacción del mapa conectamos ambos y seleccionamos el tipo de relación. Si elegimos Requiere, expresamos una condición de avance. Si elegimos Recomienda o Relacionado, agregamos contexto para entender el recorrido. Así, el docente puede comunicar tanto lo obligatorio como aquello que ayuda a estudiar.

> [!info]- Detalle técnico: catálogo de relaciones
> Backend: `requires` representa dependencia; `recommends`, `related_to`, `belongs_to` y `part_of` son informativas. El editor ofrece Requiere, Recomienda y Relacionado. Ver `B/java/com/utn/tpi/roadmap/graph/model/RelationType.java` y `F/app/features/roadmap/pages/graph-editor-page/graph-editor-page.component.ts`.

Para construir una condición más expresiva, abrimos la regla de la Práctica integradora. Queremos que el estudiante haya completado Variables y, además, que apruebe el Quiz de variables o el Quiz alternativo. En otras palabras: Variables y una de las dos evaluaciones. El ejemplo incorpora también un mínimo de cien puntos de experiencia. Esta combinación expresa una exigencia común con caminos alternativos, algo útil cuando un mismo objetivo puede alcanzarse mediante más de una actividad.

> [!info]- Detalle técnico: AND, OR y mínimo de XP
> La regla simulada `C/demo-neo4j/Regla - AND práctica.md` contiene Variables y el grupo `C/demo-neo4j/Regla - OR quizzes.md`, con mínimo 100 XP. `RuleEvaluator` evalúa grupos anidados y mínimo de XP; `RuleGap` conserva faltantes. La guía es ficticia, no datos cargados. Ver `B/java/com/utn/tpi/roadmap/rules/RuleEvaluator.java`.

Al conectar, el editor y el servidor protegen la consistencia. Revisan que los elementos pertenezcan al recorrido adecuado, que los extremos sean válidos y que la relación tenga sentido con su visibilidad. Evitan conectar un nodo consigo mismo o duplicar una relación del mismo tipo. En requisitos, revisan además que no se forme un ciclo: si A depende de B, y B ya depende de A directa o indirectamente, no existe un orden de avance válido. La validación evita guardar esa contradicción.

Cada sección tiene límites de inicio y fin que agrega el sistema. Esos puntos ayudan a estructurar el recorrido, mientras que el docente trabaja principalmente con las actividades académicas y sus requisitos. El editor también restringe qué nodos se pueden seleccionar como requisito; por ejemplo, distingue límites del sistema y actividades opcionales o de recuperación. Esto mantiene las reglas alineadas con el significado de cada elemento.

> [!info]- Detalle técnico: START, END y ciclos
> `BoundaryNodeService` crea límites por sección. `PrerequisiteEditor`, `GraphValidator` y el front verifican ciclos y extremos; el criterio DAG corresponde a dependencias, no a cualquier relación informativa. Ver `B/java/com/utn/tpi/roadmap/services/BoundaryNodeService.java`, `PrerequisiteEditor.java` y `F/app/features/roadmap/domain/prerequisite-policy.ts`.

Una vez armado el recorrido, podemos seguir reorganizándolo. El arrastre permite reordenar nodos y también solicitar el cambio de una actividad a otra sección. El servidor comprueba que el destino pertenezca al mismo roadmap y valida las condiciones de la operación. Las regiones y rutas del editor también tienen un diseño visual que puede guardarse y compartirse. Así separamos el orden académico del modo en que el docente acomoda la vista para trabajar.

> [!info]- Detalle técnico: movimiento y ETag
> `PATCH /nodes/{nodeId}/section` mueve de sección y el orden se guarda en edición. El layout de regiones usa `GET/PUT/DELETE`, `ETag` e `If-Match`, con respaldo local. El adaptador de coordenadas libres `moveNode(x,y)` responde 501 local; no afecta los otros mecanismos. Ver `B/java/com/utn/tpi/roadmap/controllers/GraphController.java`, `RoadmapLayoutController.java` y `F/app/features/roadmap/data-access/roadmap-http/http-roadmap.adapter.ts`.

Cuando cambia la estructura, también importa qué pasa con las dependencias. Una baja se evalúa teniendo en cuenta el camino de los demás nodos y las protecciones existentes. Durante la sincronización desde Courses, el sistema puede podar requisitos que quedaron fuera de visibilidad cuando dispone de la información necesaria para comprobarlo. Es una manera de mantener el recorrido consistente a medida que evoluciona, sin obligar al docente a reconstruirlo desde cero.

> [!info]- Detalle técnico: baja y poda
> La baja lógica retira aristas planas y aprobaciones del nodo; conserva hojas de reglas y recompensas y puede rechazarse si rompe caminos o elimina la última recuperación. Al evaluar se ignoran hojas de nodos dados de baja. La sync poda requisitos fuera de visibilidad solo si puede comprobar restricciones; si falla el origen, no poda. Ver `B/java/com/utn/tpi/roadmap/services/GraphService.java`, `PrerequisiteService.java` y `CourseSectionSyncService.java`.

Todo esto convierte al editor en una herramienta para expresar decisiones pedagógicas: qué se presenta, en qué orden, qué es obligatorio y qué alternativas existen. Y esas decisiones llegan después a la experiencia concreta de cada estudiante.

Al mirar la Práctica integradora, podemos explicar al alumno que no basta con llegar visualmente hasta ella: antes tiene que cumplir la lectura y una evaluación, además de reunir la experiencia requerida. Si elige el primer quiz, la alternativa ya cumplió su función; si elige el segundo, el resultado es equivalente para ese grupo de la regla. Ese ejemplo hace visible por qué usamos grupos anidados y no solo una lista plana. También ayuda al docente a revisar las consecuencias antes de guardar: qué actividad depende de cuál, quién podrá verla y qué sucede si cambia la organización de la unidad.

**Transición:** «Veamos ahora cómo esas reglas se convierten en una respuesta clara cuando el alumno quiere entrar a una actividad».»

## Qué se ve en pantalla
Mostrar dos nodos conectados y una relación informativa; abrir una regla con alternativa. Reordenar en copia de prueba y refrescar; intentar un ciclo solo si está ensayado. No prometer persistencia de coordenadas libres.

## Preguntas probables

**¿Todas las líneas bloquean?** No; Requiere expresa dependencia y otras relaciones son informativas.

**¿Puedo crear un ciclo?** Las validaciones de dependencias rechazan ciclos directos y transitivos.

**¿Qué ocurre al borrar un requisito?** Se valida la estructura; no se borran automáticamente todos sus dependientes.

**¿El reordenamiento siempre poda requisitos?** No; la sync poda fuera de visibilidad cuando logra verificar restricciones, y si no puede verificar no poda.

**¿Se guarda el arrastre?** Se implementaron orden y cambio de sección; el layout regional usa ETag. Coordenadas libres de nodo devuelven 501 local en el adaptador.

**¿Los datos del ejemplo existen en producción?** No; el ejemplo del cerebro es simulado.
