---
tags: [tpi, g10, taiga, hu]
codigo: HU-46
ref: 5375
estado: "Done"
responsable: "Fenoglio Santino"
epicas: "[[epicas/EP-593 Nodos de contenido y lectura previa|EP-593]]"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/5375
---

# HU-46: Ver en los nodos y en el Templo el material teórico de Courses

> [!info] Generado desde Taiga (2026-10-15 16:54). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/5375) · Estado: **Done** · Responsable: **Fenoglio Santino** · Sprint: **G10 - Sprint 2**
> Épica: [[epicas/EP-593 Nodos de contenido y lectura previa|EP-593]] · Tareas cerradas: **5/5**

[G10] — HU-46 — Ver en los nodos y en el Templo el material teórico de Courses
------------------------------------------------------------------------------


* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: ALUMNO
*   **Quiero**: abrir el material teórico de mi unidad (PDF, video o enlace) desde el roadmap
*   **Para**: estudiar sin salir del recorrido


* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: El material lo guarda Courses en la plataforma Garage y Roadmap se lo pide (D-03, P-30); Roadmap no guarda ni sube archivos. En una unidad bloqueada se lista sin poder abrirse (misma regla que HU-05). Marcar como leído desde el Templo o desde el nodo registra una sola lectura (HU-06) y actualiza el gate. Un material despublicado o dado de baja se ve «no disponible» y las lecturas quedan intactas.
*   [ ] Validaciones: Solo material del curso-cohorte del alumno; alumno matriculado.
*   [ ] Datos obligatorios: Curso-cohorte (alumno del token).
*   [ ] Performance (tiempos, volumen, límites): Una llamada a Courses por curso; menos de 500 ms para 20 unidades (RF-NFR-03).
*   [ ] Seguridad (roles, permisos, datos sensibles): Token técnico hacia Courses por el Gateway; URL de acceso al archivo provista por Courses (por ejemplo firmada y con vencimiento).
*   [ ] Accesibilidad (WCAG/teclado/lectores): Estado leído/pendiente/bloqueado en texto; operable por teclado.
*   [ ] Otros: Reemplaza EXAMPLE_SECTIONS de materials-page (Templo, /student/materials). No confundir con theory-bank-page (banco de preguntas de Desafíos Teóricos, de otro equipo). Se integra a #593 (D-04). HU-47 retirada el 02/10: la carga del material es de Cursos (G01). Dependencias: G01 (bloqueante: guardar el material en Garage, habilitar actividades FILE y LINK —hoy solo se crea QUIZ— y exponer por lote los metadatos y una URL de acceso). Garage todavía no aparece en tpi-course ni en tpi-system-compose (relevado el 02/10). Relacionadas: HU-04, HU-42, HU-19. Posible superposición con HU-42 (P-31). Preguntas abiertas: P-30, P-31.


* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El Templo muestra el material real agrupado por unidad.
*   [ ] **CA2**: En una unidad bloqueada el material se ve pero no se abre.
*   [ ] **CA3**: El material se abre en el visor embebido.
*   [ ] **CA4**: Un material despublicado se ve «no disponible».


* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Material teórico del curso en el roadmap

**Escenario 1**  

*   **Dado**: una unidad desbloqueada con un PDF en Courses
*   **Cuando**: el alumno abre el Templo
*   **Entonces**: ve el PDF y lo puede abrir

**Escenario 2**  

*   **Dado**: una unidad bloqueada
*   **Cuando**: abre el Templo
*   **Entonces**: ve que hay material pero no puede abrirlo

**Escenario 3**  

*   **Dado**: un material despublicado
*   **Cuando**: lo abre
*   **Entonces**: ve «no disponible»

* * *
Prototipo
---------

*   **Capturas**: materials-page (Templo, /student/materials) y visor embebido existente (toEmbedUrl: YouTube, Vimeo, Drive y visor de Office para PPT).
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente.
*   **Mock API / Swagger**: Endpoint de material teórico por unidad (a definir) sobre la lectura por lote de Courses.


## Tareas

- [x] #5427 T-46.1 Material teórico por unidad desde Courses (lote) con estado bloqueado · Closed · Fenoglio Santino
- [x] #5428 T-46.2 materials-page con datos reales; quitar EXAMPLE_SECTIONS · Closed · Fenoglio Santino
- [x] #5429 T-46.3 Abrir en el visor embebido y marcar leído (misma lectura que HU-06) · Closed · Fenoglio Santino
- [x] #5430 T-46.4 BDD material teórico · Closed · Fenoglio Santino
- [x] #5431 T-46.5 Wiki, OpenAPI y diagrama de secuencia · Closed · Franco Maximiliano Amarilla
