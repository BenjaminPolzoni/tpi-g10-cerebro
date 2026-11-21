---
tags: [presentacion, roadmap]
---

# A4. Límites conocidos y cómo responder

| Tema | Límite | Respuesta si preguntan |
|---|---|---|
| Demo integrada | Inspección estática; no se levantó stack ni probaron permisos, datos o servicios | «Esto está en código; estamos validando el comportamiento integrado del ambiente». |
| Arrastre | Orden y cambio de sección tienen persistencia implementada; layout de regiones usa ETag con respaldo local; `moveNode(x,y)` retorna 501 local | «No prometemos guardar coordenadas libres de nodos; distinguimos orden, sección y layout». |
| Neo4j | Proyección y selección existen; activación y convergencia no comprobadas | «Postgres manda; la lectura en Neo4j depende de configuración». |
| Primer sync | Sin secciones activas no crea principal desde sync; alternativas propias pueden no sincronizarse | «Hay que preparar unidades en Courses o crear el mapa explícitamente». |
| Publicación/versionado | No se verificó publicación global ni historial de versiones | «Clonar es crear otra variante, no versionar automáticamente». |
| Cierre HU-72 | Courses implementa escritura de estado final y archivo; front exporta CSV de calificaciones; circuito integrado y alcance del CSV no acreditados | «Courses es autoridad; falta validar cierre de punta a punta». |
| Examen | Tipo, tiempo y gate presentes; agenda y experiencia integrada no verificadas | «La regla existe, estamos verificando la integración con horarios y Motor». |
| Ranking | Back 1,1,3; front consecutivo; zonas pueden diferir. `reached_first` usa hora registrada | «La presentación no es idéntica al puesto de servidor y la fecha puede reflejar demoras». |
| Privacidad | Depende de configuración; no anonimato universal probado | «Antes de mostrar datos reales verificamos visibilidad y permisos». |
| Salud / Backoffice | Front de Courses consume resumen y timeline; Backoffice consume eventos bajo flag, sin cliente HTTP identificado | «Ofrecemos la información; falta verificar consumidor y despliegue». |
| Materiales | Código configura Garage compatible S3 y bucket `course-materials`; proveedor efectivo y URL del entorno no comprobados; formatos no siempre embebidos | «Courses administra el material y el visor elige cómo abrirlo». |
| Portales | Representación de zonas implementada; un dibujo no prueba acceso | «La elegibilidad la decide el servidor». |
| Progreso | Una rectificación puede reabrir nodos; no toda reversión de desbloqueos fue auditada | «Ajustamos movimientos y resultado; no aseguramos reversión total». |
| Flags/seguridad | `AUTHZ_MODE` por defecto off en fuente; configuración efectiva desconocida | «Confirmamos el modo y la matriz real en el ambiente antes de la demo». |
| Feedback y rendimiento | Motor, feedback por tipo, FPS y compatibilidad no verificados | «Mostramos solo lo ensayado; el detalle de corrección pertenece al Motor». |
| Eventos | Outbox/reintentos no prueban entrega exactamente una vez ni consumo | «Tenemos mecanismos de entrega e idempotencia específicos, no una garantía global». |

## Dificultad equivocada y recompensas históricas

Editar dificultad o dar de baja un nodo no recalcula ni revierte automáticamente recompensas ya otorgadas. La rectificación es una revisión de nota, no de dificultad histórica, y no revoca insignias. Existe reversión explícita por intento en el Motor, con autorización, liquidación previa y confirmación de Accounting: puede compensar XP, monedas, vida y cargas, pero no garantiza aceptación, no recalcula la diferencia por dificultad y conserva completados e insignias. No se verificó botón de reversión en el front de desafíos. Detalle y condiciones: [[10-revertir-recompensas]].
