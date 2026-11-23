---
tags: [presentacion, roadmap]
---

# A1. Guion operativo de demo

## Preparación y cuentas
- Entorno integrado y Gateway funcionando; confirmar versiones, organización, `AUTHZ_MODE`, permisos, servicios y WebGL/escritorio.
- Cuatro cuentas: docente dueño, alumno inscripto, gestor y admin con packs y organización verificados; además un segundo alumno ficticio inscripto en organización y comisiones correctas; no proyectar identidades reales sin validar privacidad.
- Cohorte activa con al menos dos comisiones, varias unidades, mapa principal y alternativa habilitada, contenidos accesibles, desafíos publicados y resultados/insignias preparados. Si se quieren mostrar deciles, al menos diez inscriptos.
- Una dependencia AND/OR clara, nodo habilitado y bloqueado, zona/portal y datos de retorno preparados; probar conexión a Motor, Courses y Accounting.
- Para primer alta y archivo usar cohortes descartables distintas. Ensayar y disponer capturas de respaldo; no se ejecutó ensayo integrado en este trabajo.

## Cuentas y recorrido de permisos
- **DOCENTE:** entrar a su cohorte, lista, editor y seguimiento; probar solo lectura o cambios descartables previamente ensayados.
- **ALUMNO:** ingresar a la organización y comisión correctas, ver mapas habilitados, mundo, progreso y ranking; comprobar que no aparece el editor.
- **GESTOR:** ingresar y mostrar listado o dashboard institucional si su pack y datos lo habilitan; no suponer que dispone de progreso individual ajeno.
- **ADMIN:** mostrar acceso administrativo preparado; mantenimiento solo como vista y si está ensayado, sin ejecutar operaciones destructivas. No prometer que tiene la misma pantalla inicial del docente.
- Contrastar con una cuenta sin acceso o una cohorte ajena en ensayo previo; si falla, no convertir el resultado en una afirmación general. El cierre real queda fuera de demo.

## Secuencia
1. Como docente abrir Courses y cohorte; explicar frontera. Abrir Roadmap y lista de variantes.
2. Presentar brevemente [[10-Roles-y-permisos]] y las cuatro cuentas; volver al docente.
3. Mostrar asistente sin confirmar; opcional, en cohorte limpia, abrir edición y esperar la sincronización inicial con unidades activas.
4. En editor mostrar nodos y relaciones; abrir regla, reordenar en copia y recargar. Verificar movimiento de sección si está ensayado. No afirmar coordenadas libres guardadas.
5. Cambiar a alumno: mostrar unidad bloqueada y motivo, navegar en barco, seleccionar y entrar a isla.
6. Cambiar cámara, señalar torre y cofre; abrir material probado y cerrarlo.
7. Abrir intento preparado, completar solo si se ensayó, regresar y mostrar ubicación. Tener ruta alternativa si Motor no responde.
8. Mostrar XP, insignias, ranking y, si hay, empate y puestos que efectivamente se observen.
9. Volver a docente; abrir avance por comisión, comparación y opcional dashboard de Courses. No efectuar cierre real.
10. Cerrar con diagrama y alcance; reservar [[A4-Limites-conocidos]] y [[A6-Preguntas-dificiles]].

## Contingencias
Si no se carga mundo, usar capturas y aclarar que son respaldo. Si gate rechaza por origen indisponible, explicar falla cerrada sin inventar avance. Si no hay empate, usar el ejemplo conceptual 1,1,3 del servidor frente a 1,2,3 de la función auxiliar, aclarando que el mapper HTTP conserva el resultado del servidor; no presentarlo como resultado real.
