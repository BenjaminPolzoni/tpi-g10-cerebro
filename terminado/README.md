# Terminado

Notas de tareas/planes implementados. Las cinco notas originales de esta carpeta registraban explícitamente **completada**, **hecho** o **mergeado**. Las dieciséis incorporadas el 2026-10-22 fueron verificadas contra el código de `origin/develop` a esa fecha; algunas conservan en su contenido un estado histórico anterior (por ejemplo, “borrador” o “en revisión”). La carpeta clasifica la implementación, no cambia retrospectivamente el texto de las notas.

## Estado explícito en la nota

| Documento | Estado registrado |
|---|---|
| [[13-plan-T-45-7]] | Completada; back y front mergeados |
| [[HT-14 Front - quitar IDs de mock]] | Hecho |
| [[T-45.7 Back - error del ranking]] | Completada |
| [[T-45.7 Front - estados de error del ranking]] | Completada |
| [[T-45.8 Back - ranking con filtro por comisión]] | Mergeado |

## Implementación verificada en `origin/develop` (2026-10-22)

### Frontend y ranking

| Documento | Funcionalidad |
|---|---|
| [[Fix Front - barco da vueltas al atracar]] | Atracado del barco |
| [[Fix Front - card del alumno entra al modo simple]] | Card del alumno en modo simple |
| [[Fix Front - cámara persistente y posición al volver de un desafío]] | Cámara y posición al regresar |
| [[Fix Front - orden de nodos y restricciones]] | Orden de nodos y restricciones |
| [[T-45.9 Front - filtro por comisión en el ranking]] | Filtro del ranking por comisión |
| [[T-45.10 Front - avance por comisión para el profesor]] | Avance por comisión del profesor |
| [[T-45.11 Back+Front - ranking por XP o por notas]] | Ranking por XP/notas |

### Roadmap, Accounting y Gate

| Documento | Funcionalidad |
|---|---|
| [[T-03-2-ACCOUNTING-CLIENT]] | Cliente HTTP de Accounting |
| [[T-03-3-LEDGER-Y-DESBLOQUEOS]] | Ledger de XP y desbloqueos |
| [[T-15-1-GATE-V3]] | Gate v3 |
| [[T-15-2-ACCOUNTING-GATE-LEDGER]] | Accounting, Gate y Ledger |
| [[T-15-4-MATRICULA-VIDAS-RECUPERACION]] | Matrícula, vidas y recuperación |
| [[T-15-6-GATE-BDD-LOAD]] | Pruebas BDD y de carga del Gate |
| [[T-35-1-ENDPOINT-INVENTARIO]] | Endpoint de inventario |
| [[T-44-4-ROADMAP-POR-GRUPO]] | Configuración del roadmap por grupo |
| [[T-59.5 — Qué le falta al alumno para desbloquear un nodo]] | Requisitos para desbloquear nodo |

Las notas con partes sustanciales pendientes o no verificadas siguen en sus carpetas de origen.
### Planes de Benja, verificados el 2026-10-25

| Documento | Funcionalidad | Evidencia |
|---|---|---|
| [[T-62.5 Front - alternar roadmaps y unidades en el mapa del profesor]] | Alternar roadmaps en General y en el mapa | FE #1462 mergeada; T-62.5 Closed |
| [[Back+Front - configurar roadmaps al crear un curso]] | Roadmaps por comisión, configuración y vista del alumno | FE #1462 y BE #341 mergeadas; T-57.5 a T-57.7 y T-61.5 a T-61.8 Closed; HU-57 y HU-61 Done |
| [[Issue 270 Back+Front - ver feedback desde el mapa sin abrir intento]] | Feedback del desafío desde el mapa | FE #1111 y #1152, BE #318 mergeadas; issue #270 cerrada |
| [[Issue 309 Back - resumen de progreso por cohorte y serie semanal de XP]] | Resumen por cohorte y serie semanal de XP | BE #325 y #326 mergeadas; issue #309 cerrada. El PR 2 (bloqueados y motivos) quedó atado a D1 |
| [[Front - niebla negra en las islas bloqueadas del archipiélago]] | Niebla sobre las islas bloqueadas | En `archipelago-3d.service.ts` de `develop`, con la niebla del mundo hex en vez del negro liso |
