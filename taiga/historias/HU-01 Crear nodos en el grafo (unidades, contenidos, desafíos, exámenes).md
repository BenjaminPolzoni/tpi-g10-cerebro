---
tags: [tpi, g10, taiga, hu]
codigo: HU-01
ref: 76
estado: "Done"
responsable: "Mateo Delgado Costa"
epicas: "[[epicas/EP-56 Estructura del roadmap como grafo de nodos|EP-56]]"
sprint: "G10 - Sprint 1"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/76
---

# HU-01: Crear nodos en el grafo (unidades, contenidos, desafíos, exámenes)

> [!info] Generado desde Taiga (2026-10-14 20:43). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/76) · Estado: **Done** · Responsable: **Mateo Delgado Costa** · Sprint: **G10 - Sprint 1**
> Épica: [[epicas/EP-56 Estructura del roadmap como grafo de nodos|EP-56]] · Tareas cerradas: **8/8**

[G10] — HU-01 — Crear nodos en el grafo (unidades, contenidos, desafíos, exámenes)
----------------------------------------------------------------------------------

* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: organizar mi curso creando unidades y agregando nodos de contenido, desafío o examen con prerrequisitos
*   **Para**: que el alumno recorra la materia en la secuencia pedagógica que defino, con un grafo acíclico

* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: La unidad y el nodo pertenecen a un curso-cohorte. Se pueden crear y editar aun con el curso activo (RF-CUR-05) y la baja es lógica (RF-NFR-01). Una UNIDAD contiene nodos CONTENIDO, DESAFIO o EXAMEN. El orden es explícito y con desplazamiento. La arista se rechaza si cierra un ciclo. DESAFIO y EXAMEN referencian el catálogo del Motor; CONTENIDO referencia un contenido_id. La obligatoriedad es sí o no y los reintentos van de 0 a PAR-13. Si el Motor da de baja un desafío, el nodo queda no disponible sin borrar progreso.
*   [ ] Validaciones: Unidad: nombre de 3 a 80 caracteres, único entre las activas del curso-cohorte, posición mayor o igual a 1. Nodos: el desafío o examen debe estar publicado, la unidad activa y del curso-cohorte, sin autociclos, reintentos entre 0 y PAR-13.
*   [ ] Datos obligatorios: Unidad: curso-cohorte, nombre y posición, más descripción opcional. Nodo: unidad, tipo, referencia y posición, más obligatoriedad y reintentos. Arista: origen y destino.
*   [ ] Performance (tiempos, volumen, límites): Alta en menos de 500 ms con 20 unidades, incluyendo la validación de ciclos y la consulta al catálogo.
*   [ ] Seguridad (roles, permisos, datos sensibles): Solo el PROFESSOR dueño del curso, validado contra Courses. El catálogo del Motor se consulta con token técnico.
*   [ ] Accesibilidad (WCAG/teclado/lectores): Formularios operables por teclado, estados anunciados en texto, y el grafo se puede armar por formulario mientras el editor gráfico esté detrás del flag (RF-CUR-04).
*   [ ] Otros: El campo reintentos_permitidos lo consume el gate de HU-15 (motivo sin_reintentos en validación interna). Trazabilidad: RF-CUR-01, RF-CUR-05, RF-CUR-06, PAR-13, RF-NFR-01. Dependencias: Motor (catálogo y aviso de baja), Courses (propiedad del curso) y Gateway; el Motor confirma el endpoint de catálogo y el aviso de baja el día 5. Datos: crea unidad, nodo y arista_prerrequisito, sin migración de datos. Riesgo: que el catálogo no esté disponible a tiempo; mitigación, catálogo simulado en la semilla de HT-02.

* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: Una unidad creada en una posición ocupada desplaza a las siguientes.
*   [ ] **CA2**: Un nombre repetido se rechaza sin crear nada.
*   [ ] **CA3**: Un profesor que no es dueño queda bloqueado y nada cambia.
*   [ ] **CA4**: Dar de baja una unidad con alumnos avanzando no les hace perder progreso.
*   [ ] **CA5**: Un nodo se crea en la unidad y posición indicadas.
*   [ ] **CA6**: Una arista que cierra un ciclo se rechaza.
*   [ ] **CA7**: Una referencia inexistente al catálogo se rechaza.
*   [ ] **CA8**: Un desafío dado de baja deja el nodo no disponible sin tocar el progreso.
*   [ ] **CA9**: Un profesor que no es dueño no puede agregar nodos ni aristas.

* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Estructura del roadmap como grafo de unidades y nodos

**Escenario 1**  

*   **Dado**: existe una unidad en la posición 2
*   **Cuando**: creo una unidad en la posición 2
*   **Entonces**: la nueva queda en la 2 y la anterior pasa a la 3

**Escenario 2**  

*   **Dado**: la unidad Fundamentos ya existe
*   **Cuando**: creo otra con el mismo nombre
*   **Entonces**: se rechaza con mensaje y no se crea

**Escenario 3**  

*   **Dado**: soy profesor de otro curso
*   **Cuando**: intento crear una unidad o un nodo
*   **Entonces**: se rechaza por permiso y nada cambia

**Escenario 4**  

*   **Dado**: A es prerrequisito de B
*   **Cuando**: conecto B como prerrequisito de A
*   **Entonces**: se rechaza por ciclo y no se crea la conexión

* * *
Prototipo
---------

*   **Capturas**: Boceto Editor de unidades y nodos (profesor).
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente: formularios de alta y selector de prerrequisitos.
*   **Mock API / Swagger**: POST, PATCH y DELETE /api/roadmap/unidades; POST /api/roadmap/nodos; POST /api/roadmap/prerrequisitos; catálogo del Motor vía gateway.


## Tareas

- [x] #409 T-01.1 — Endpoints de alta de unidad y nodo con validaciones · Closed · Mateo Delgado Costa
- [x] #410 T-01.4 — Reposicionamiento, no disponible y permiso de dueño · Closed · Mateo Delgado Costa
- [x] #411 T-01.2 — Persistencia con reposicionamiento automático · Closed · Mateo Delgado Costa
- [x] #412 T-01.5 — Frontend: formularios y conexión de prerrequisitos · Closed · Mateo Delgado Costa
- [x] #414 T-01.6 — Tests de escenarios BDD · Closed · Mateo Delgado Costa
- [x] #2080 T-01.3 — Arista de prerrequisito con validación acíclica · Closed · Mateo Delgado Costa
- [x] #2081 T-01.7 — Vista lista de unidades y nodos con estados (profesor) · Closed · Mateo Delgado Costa
- [x] #3574 T-01.8 Cliente HTTP real del catalogo del Motor via Gateway · Closed · Mateo Delgado Costa
