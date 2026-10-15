---
tags: [tpi, g10, sprint-3, historia, ht]
id: B02
tipo: HT
epica: "EP-S3-0"
capa: "Infra"
esfuerzo: S
puntos: 2
prioridad: Must
estado: Propuesta
responsable: ""
taiga: "Sin cargar"
depende: []
---

# B02: Encender los flags en los entornos

> [!info] Épica [[sprints/sprint-3/epicas/EP-S3-0 Deuda del Sprint 2|EP-S3-0]] · **HT** · Capa: **Infra** · **2 pts** · **Must** · Taiga: Sin cargar
> **Para cargar en Taiga:** título = la línea de abajo; descripción = desde *Descripción* hasta *Dependencias / Impactos*; cada línea de *Tareas* es una tarea. Lo que está debajo de la línea final es contexto del cerebro y no va a Taiga.

**[G10] — HT-xx — Encender los flags en los entornos** *(reemplazar `xx` por el número que asigne Taiga)*

* * *

## Descripción (Como / Quiero / Para)

- **Como**: EQUIPO DE DESARROLLO
- **Quiero**: encender `SECTIONS_SYNC_ENABLED` y `ROADMAP_BY_GROUP_ENABLED` en la mesh y en el entorno de la demo
- **Para**: que funcionen en la demo el sync de secciones con Courses y el roadmap por comisión, que ya están hechos

* * *

## Notas / Observaciones

- [ ] Reglas de negocio: Los flags están apagados por defecto por DEC-004; el default del código no cambia, se encienden por entorno.
- [ ] Validaciones: Con los flags encendidos, el sync manual y el roadmap por comisión responden sin error en el entorno integrado.
- [ ] Otros: Si algo falla al encenderlos, se abre un bug en la HU correspondiente (HU-17, 18, 36, 44 o 45).

* * *

## Criterios de Aceptación (CA)

- [ ] **CA1**: Los dos flags en `true` en el compose de la mesh y de la demo.
- [ ] **CA2**: `POST /api/roadmap/courses/{courseId}/sections/sync` responde 200 en el entorno integrado.
- [ ] **CA3**: El roadmap de un alumno con comisión se filtra por su comisión.
- [ ] **CA4**: Las fallas encontradas quedan registradas como bugs.

* * *

## BDD (mínimo 3 escenarios)

**Característica:** Flags encendidos en los entornos

**Escenario 1**

- **Dado**: el entorno de la demo con `SECTIONS_SYNC_ENABLED=true`
- **Cuando**: un profesor dueño ejecuta el sync de secciones
- **Entonces**: las secciones de Courses aparecen en el roadmap

**Escenario 2**

- **Dado**: el entorno con `ROADMAP_BY_GROUP_ENABLED=true` y un alumno en la comisión 2w1
- **Cuando**: el alumno abre el roadmap
- **Entonces**: ve solo las secciones habilitadas para 2w1

**Escenario 3**

- **Dado**: un flag encendido que provoca un error
- **Cuando**: se prueba el flujo
- **Entonces**: el error queda registrado como bug en su HU

* * *

## Prototipo

- **Capturas**: No aplica (sin pantalla).
- **URL Figma**: No aplica.
- **Storybook**: No aplica.
- **Mock API / Swagger**: No aplica.

* * *

## Estimación / Prioridad

- **Puntos (Fibonacci)**: 2
- **Prioridad (MoSCoW / Numérica)**: Must

* * *

## Dependencias / Impactos

- Servicios involucrados: Courses (secciones y comisiones), plataforma (compose).
- Módulos afectados: `application.properties` por entorno, `tpi-system-compose`.
- Otros equipos / aprobaciones: Quien mantiene `tpi-system-compose` y la mesh.
- Impacto en datos / migraciones: Sin migración.
- Riesgos y mitigación (opcional): Que Courses no tenga listos los scopes en ese entorno; mitigación: verificar G12 antes de encender.

## Tareas

- [ ] T-B02.1 Encender los flags en el compose de la mesh y de la demo
- [ ] T-B02.2 Probar sync de secciones y roadmap por comisión en el entorno integrado
- [ ] T-B02.3 Registrar los bugs encontrados

---

## Contexto en el cerebro (no va a Taiga)

### Qué hay hoy

Los dos flags están en `false` por defecto (DEC-004). Con eso apagado no andan HU-17, 18, 36, 44 y 45.

### Depende de

Nada: se puede empezar ya.

### Dudas que la frenan

- [[sprints/sprint-3/08-dudas|E6]]

### Deuda técnica que cierra

- [[deuda-tecnica|DT-20]]
