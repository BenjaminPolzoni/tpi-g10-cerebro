---
tags: [tpi, g10, taiga, epica]
ref: 56
estado: "New"
responsable: "Benjamin Polzoni"
avance: "1/1"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/56
---

# EP-56: Estructura del roadmap como grafo de nodos

> [!info] Generado desde Taiga (2026-10-15 16:55). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/epic/56) · Estado: **New** · Responsable: **Benjamin Polzoni** · HU cerradas: **1/1**

[G10] — Estructura del roadmap como grafo de nodos
--------------------------------------------------

* * *

Objetivo
--------

Permitir que el PROFESOR represente su materia como un grafo de unidades, cada una con nodos de contenido, desafío y examen conectados por prerrequisitos. Es la estructura sobre la que se apoyan la lectura previa, el desbloqueo, la racha y el ranking: sin grafo no hay nada que recorrer ni sobre qué medir avance.

* * *

Suposiciones y Restricciones
----------------------------

*   Suposiciones: el curso-cohorte ya existe y lo administra el equipo Courses. El padrón está cargado antes de que haya alumnos avanzando (RF-USR-05c). El catálogo de desafíos y exámenes lo administra el Motor de Desafíos: nosotros guardamos la referencia, nunca el enunciado. El material de estudio lo almacena Courses y guardamos el contenido\_id. Un nodo tiene exactamente uno de cuatro tipos: UNIDAD, CONTENIDO, DESAFIO o EXAMEN.
*   Restricciones (legales/técnicas): cursos y desafíos son editables aun publicados y en uso (RF-CUR-05). No existe borrado real, la baja es lógica (RF-NFR-01). Toda entidad lleva la clave curso-cohorte. El grafo es acíclico: la arista que cierra un ciclo se rechaza en el alta. Ninguna llamada saliente directa a otro microservicio, todo va por API Gateway. 100% escritorio (RF-NFR-05).

* * *

Criterios de Aceptación a nivel Épico
-------------------------------------

*   [ ] Un profesor construye un roadmap de al menos tres unidades, agrega nodos de los cuatro tipos, los conecta como prerrequisitos, reordena una unidad y da de baja un nodo con alumnos avanzando, sin que ninguno pierda progreso ni desbloqueos.
*   [ ] KPIs iniciales: ningún KPI de producto aplica a esta épica. El indicador propio es de servicio: la lectura completa del grafo responde en menos de 500 ms con 20 unidades, 120 nodos y 120 inscriptos (RF-NFR-03).
*   [ ] Sin regresiones críticas en E3: ningún cambio de grafo revierte un desbloqueo ya alcanzado (RF-CFG-06).
*   [ ] Observabilidad y alertas: log de toda edición de grafo sobre cursos activos con autor, fecha y alumnos afectados. Alerta si se rechaza una arista por ciclo N veces seguidas, señal de que el profesor no entiende el modelo.
*   [ ] Documentación publicada: página de Wiki con el modelo de datos y los endpoints del grafo publicados en OpenAPI.

* * *

Dependencias / Impactos
-----------------------

*   Servicios / APIs: Courses (curso-cohorte, estado y material), Motor de Desafíos (identificador de desafío y de examen), API Gateway.
*   Módulos afectados: grafo de unidades y nodos, aristas de prerrequisito, editor del profesor, lectura del recorrido.
*   Otros equipos: el Motor de Desafíos debe publicar su catálogo consultable antes de que se puedan vincular nodos de desafío y examen.
*   Impacto en datos / migraciones: tablas unidad, nodo y arista\_prerrequisito, todas con curso-cohorte y baja lógica. Sin migración de datos.
*   Feature toggles / flags: editor-grafico-roadmap. Con el flag apagado el profesor arma el grafo por formularios, que es el camino del MVP (RF-CUR-04). Plan de retiro: se elimina cuando el editor gráfico sea estable en producción.


## Historias

| HU | Estado | Responsable | Sprint | Tareas |
|---|---|---|---|---|
| [[historias/HU-01 Crear nodos en el grafo (unidades, contenidos, desafíos, exámenes)\|HU-01]] Crear nodos en el grafo (unidades, contenidos, desafíos, exámenes) | Done | Mateo Delgado Costa | G10 - Sprint 1 | 8/8 |
