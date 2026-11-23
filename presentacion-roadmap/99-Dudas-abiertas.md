---
tags: [presentacion, roadmap]
---

# 99. Dudas abiertas

1. ¿Qué ambiente, commits, organización y flags efectivos se usarán? (Confirmado por el equipo: lectura Neo4j activa.)
2. Cuentas confirmadas: docente, alumno, gestor y admin (ver [[10-Roles-y-permisos]]). Falta: ¿cohortes/comisiones con progreso, empates, insignias, zonas y portales reproducibles?
3. ¿Se ensayó la sincronización inicial y la selección/visibilidad de mapas con alumnos de varias comisiones?
4. ¿Están operativos Motor, Accounting, Courses y los contratos Kafka/HTTP entre las versiones desplegadas? ¿Quién consume cada endpoint técnico?
5. Código: Garage compatible S3, bucket configurable. **Lo revisa el usuario:** bucket/proveedor efectivo y URLs válidas en la demo.
6. ¿Se verificó el retorno desde intento, feedback, desbloqueo y examen con agenda real?
8. ¿Están desplegados y probados de punta a punta el cierre de Courses y el consumo del evento? ¿La exportación disponible sirve como acta y satisface el alcance requerido?
9. Anonimato del ranking: se presenta como garantía (confirmado por el equipo); verificar que la config del ambiente lo tenga activo.
10. ¿Qué rendimiento y compatibilidad de navegador/dispositivo se observaron en el equipo que presentará?
11. No se ejecutaron aplicaciones, pruebas ni verificación extremo a extremo; las fuentes son inspecciones estáticas de los commits indicados en [[00-Indice]].
