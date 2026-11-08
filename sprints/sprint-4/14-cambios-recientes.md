---
tags: [tpi, g10, sprint-4, cambios]
fecha: 2026-10-26
estado: plantilla
---

# 14 — Cambios recientes · Sprint 4

> [!warning] Plantilla de planificación
> Documento creado para replicar la estructura del Sprint 3. **No contiene alcance, estimaciones, responsables ni estado aprobados para Sprint 4.**

## Antecedente

- [Nota homóloga de Sprint 3](../sprint-3/14-cambios-recientes.md) — referencia histórica; verificar vigencia antes de trasladar cualquier dato.

## Por completar

- [ ] Llevar bitácora de PRs y decisiones del Sprint 4 con fecha, repositorio, enlace e impacto.
- [ ] Registrar fuentes y fecha de verificación.
- [ ] Confirmar con el equipo antes de marcar como plan vigente.

## Bitácora

### Front · visor 3D, tarjetas de curso y estado del nodo (2026-10-27)

| PR | Autor | Qué hace |
|---|---|---|
| [FE#1666](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/1666) | Benja | **Visor 3D:** HTML, Markdown, PDF, txt y CSV del nodo se ven dentro del panel, sin descargar (antes bajaba un archivo con el nombre de la clave de Storage). Tipo desde Courses **por sección** (`include_sections=true` viene vacío) y, si falta, desde los primeros bytes de Storage. Sin sonda de `Content-Disposition` |
| [FE#1666](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/1666) | Benja | **Tarjetas de curso:** descripción en 2 renglones con "…" y popover con el texto completo al pasar el mouse; caja de stats y botón anclados abajo, simétricos en la fila |
| [FE#1666](https://github.com/2026-P4-FE/2026-PIV-TPI-FE/pull/1666) | Benja | **Estado del nodo unificado (web + 3D):** badge a la derecha. Desafíos: Visto, Rehacer (nota + reintentos), Aprobado (nota), Para corregir. Teoría: Pendiente de lectura / Leído. Regla única en `roadmap/domain/node-student-status.ts`. "Visto" vive en `localStorage` (falta campo en el back) |

- **Entorno local:** el edge local necesitaba un segundo `sub_filter` para las URLs de Garage que el edge de la plataforma ya reescribe a `/_s3`. Ver [[arquitectura/levantar-entorno|Levantar el entorno]] ("Garage y `/_s3`").
- **Tests:** `verify` OK. 22 tests de la suite completa también fallan en `develop` limpio (ajenos al PR).
- Detalle: [[sprints/sprint-4/Planes/Benja/Front+Back - previsualizar HTML y Markdown en el visor 3D|plan del visor 3D]] (secciones "Adicionales" y "PR").
