---
tags: [tpi, g10, sprint-3, historia, ht]
id: C08
tipo: HT
epica: "EP-S3-2"
capa: "Back"
esfuerzo: M
puntos: 5
prioridad: Must
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: [C01, C02, C04]
---

# C08: Seed de demo curado

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-2 Correcciones de los profes|EP-S3-2]] · **HT** · Capa: **Back** · **5 pts** · **Must** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HT-xx — Seed de demo curado** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: EQUIPO DE DESARROLLO
- **Quiero**: un seed de demo con un curso completo, curado y reproducible
- **Para**: levantar la demo siempre igual y mostrar todas las funciones

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Fuera del perfil productivo. Usa los usuarios demo de G07. Incluye START/END, tipos de relación, examen con ventana horaria y varias secciones.
- [ ] Validaciones: Correrlo dos veces no duplica datos.

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: Script o migración `demo` separada del perfil productivo.
- [ ] **CA2**: Un curso completo con todo lo del sprint.
- [ ] **CA3**: Usa los usuarios demo de G07.
- [ ] **CA4**: Es idempotente.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Seed de demo

**Escenario 1**

- **Dado**: un entorno vacío
- **Cuando**: se corre el seed
- **Entonces**: aparece el curso de demo completo

**Escenario 2**

- **Dado**: el seed ya corrido
- **Cuando**: se corre otra vez
- **Entonces**: no duplica datos

**Escenario 3**

- **Dado**: el perfil productivo
- **Cuando**: arranca el servicio
- **Entonces**: el seed no se ejecuta

* * *

## Prototipo

- **Capturas**: No aplica (sin pantalla).
- **URL Figma**: No aplica.
- **Storybook**: No aplica.
- **Mock API / Swagger**: No aplica.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 5
- **Prioridad (MoSCoW / Numérica)**: Must

* * *

## Dependencias / Impactos

- Servicios involucrados: Users (usuarios demo), Courses (curso de demo).
- Módulos afectados: Scripts de seed.
- Otros equipos / aprobaciones: G07, G01.
- Impacto en datos / migraciones: Datos de demo.
- Riesgos y mitigación (opcional): Depende de C01, C02 y C04.

## Tareas

- [ ] T-C08.1 Guion del curso de demo
- [ ] T-C08.2 Script idempotente
- [ ] T-C08.3 Probarlo en el entorno de demo

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

Los datos de ejemplo se sacaron del micro (HT-09).

### Depende de

- [[sprints/sprint-3/historias/C01 Nodos de inicio y fin obligatorios|C01]] Nodos de inicio y fin obligatorios
- [[sprints/sprint-3/historias/C02 Relaciones con tipo|C02]] Relaciones con tipo
- [[sprints/sprint-3/historias/C04 Nodo examen con ventana horaria|C04]] Nodo examen con ventana horaria

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|G7]]
- [[sprints/sprint-3/08-dudas|E4]]
