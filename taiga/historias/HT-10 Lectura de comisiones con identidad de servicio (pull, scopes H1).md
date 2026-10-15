---
tags: [tpi, g10, taiga, ht]
codigo: HT-10
ref: 7538
estado: "Done"
responsable: "Mateo Delgado Costa"
epicas: "Sin épica"
sprint: "G10 - Sprint 2"
url: https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/7538
---

# HT-10: Lectura de comisiones con identidad de servicio (pull, scopes H1)

> [!info] Generado desde Taiga (2026-10-15 16:54). No editar a mano: correr `scripts/taiga_sync.py`.
> [Abrir en Taiga](https://tree.taiga.io/project/tup_santoro_exequiel-plataforma-de-aprendizaje-gamificado-de-programacion/us/7538) · Estado: **Done** · Responsable: **Mateo Delgado Costa** · Sprint: **G10 - Sprint 2**
> Épica: Sin épica · Tareas cerradas: **2/2**

Lectura por PULL (M2M) de comisiones y membresías alumno-comisión con scope course.groups.read y course.enrollment.read. Sin evento ni almacén local. Solo PROFESSOR/MANAGER asignan el grupo de cada alumno; Roadmap solo lee. Reemplaza a #5372 (deprecada).

## Tareas

- [x] #7539 Membresías del alumno por pull (participants) — sin tabla local ni evento · Closed · Mateo Delgado Costa
- [x] #7540 Cliente pull de comisiones — course.groups.read · Closed · Mateo Delgado Costa
