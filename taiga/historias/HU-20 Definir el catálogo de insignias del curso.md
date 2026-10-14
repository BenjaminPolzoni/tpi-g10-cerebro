---
tags: [tpi, g10, taiga, hu]
codigo: HU-20
ref: 4243
estado: "Done"
responsable: "Benjamin Polzoni"
epica: "[G10] — Logros e insignias"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4243
---

# HU-20: Definir el catálogo de insignias del curso

> [!info] Generado desde Taiga (2026-10-14 18:47). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/4243) · Estado: **Done** · Responsable: **Benjamin Polzoni** · Sprint: **G10 - Sprint 2**

[G10] — HU-20 — Definir el catálogo de insignias del curso
----------------------------------------------------------


* * *
Descripción (Como / Quiero / Para)
----------------------------------

*   **Como**: PROFESOR
*   **Quiero**: ver las insignias del sistema y crear las de mi curso con su criterio
*   **Para**: premiar los logros que me importan


* * *
Notas / Observaciones
---------------------

*   [ ] Reglas de negocio: Insignias del sistema (fijas) más las del profesor por curso-cohorte, CROSS_CUTTING o PER_NODE, con criterio, valor e ícono. Los tipos de criterio dependen de la decisión #4 del PO (4 o 10). Baja lógica; una insignia ya otorgada no se borra.
*   [ ] Validaciones: Nombre único por curso; criterio del catálogo; ícono de GENERIC_ICONS; solo PROFESSOR dueño.
*   [ ] Otros: Rutas en la convención del back (/api/roadmap/courses/{courseId}/badges), no las rutas en español que asume el front. Dependencias / impactos: Relacionadas: HU-21, HU-22, HU-25. Preguntas abiertas: decisión #4 del PO.


* * *
Criterios de Aceptación (CA)
----------------------------

*   [ ] **CA1**: El profesor ve las insignias del sistema y las de su curso.
*   [ ] **CA2**: Crea una insignia con criterio válido y queda guardada.
*   [ ] **CA3**: Un criterio fuera del catálogo se rechaza.
*   [ ] **CA4**: El front deja de usar localStorage.


* * *
BDD (mínimo 3 escenarios)
-------------------------

**Característica:** Catálogo de insignias del curso

**Escenario 1**  

*   **Dado**: un profesor dueño
*   **Cuando**: crea una insignia MIN_XP con valor 500
*   **Entonces**: queda en el catálogo del curso

**Escenario 2**  

*   **Dado**: un criterio inexistente
*   **Cuando**: intenta guardarla
*   **Entonces**: rechazo con mensaje

**Escenario 3**  

*   **Dado**: otro profesor
*   **Cuando**: intenta crear en ese curso
*   **Entonces**: 403

* * *
Prototipo
---------

*   **Capturas**: Pendiente.
*   **URL Figma**: Pendiente de publicar.
*   **Storybook**: Pendiente.
*   **Mock API / Swagger**: badges-catalog-page existente.


## Tareas

- [x] #4296 T-20.1 Esquema badge y badge_award (migración V16) · Closed · Ludmila Mailen Cejas
- [x] #4297 T-20.2 Endpoints de catálogo en la convención del back · Closed · Benjamin Polzoni
- [x] #5393 T-20.3 Tipos de criterio: los 10 que apruebe el PO · Closed · Ludmila Mailen Cejas
- [x] #5394 T-20.4 HttpBadgesAdapter para el catálogo; quitar localStorage · Closed · Benjamin Polzoni
- [x] #5395 T-20.5 BDD catálogo de insignias · Closed · Benjamin Polzoni
- [x] #5396 T-20.6 Wiki, OpenAPI y diagrama de secuencia · Closed · Quinteros Tomás
- [x] #6237 T-20.7 Cargar las 12 insignias del sistema (migración V17) · Closed · Ludmila Mailen Cejas
