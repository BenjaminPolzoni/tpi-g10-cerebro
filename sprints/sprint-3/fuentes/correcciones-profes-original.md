# **Correcciones — lo que nos toca**

## **1\. Primera parte: lo que sí es nuestro**

### **Grafo y editor**

* ☐ **Mejorar el arrastre del grafo** y poder relacionar unidades entre sí desde el editor.  
* ☐ **Las unidades son el curso (ejemplo Google Maps).** El mapa *es* el curso, no un curso que contiene unidades. La pantalla course-editor-page es nuestra.  
* ☐ **Regla: siempre nodo inicio y nodo final**, con el grafo en el medio. No dejar guardar sin ellos.  
* ☐ **Relaciones con 4 niveles (Related to / Belongs to…)**: "una necesita de otra", etc.  
  * Tipos de relación definidos.  
  * Configurable qué relaciones se ven.  
  * Mostrar el nombre de la relación.  
* ☐ **Usar una BD de grafo** (ej. Neo4j) en vez de tablas relacionales.  
* ☐ **Lista de nodos que muestre la obligatoriedad** (qué nodo es prerrequisito de otro).

### **Nodos especiales**

* ☐ **Nodo inicio "Bienvenidos"**, con un visual de que empieza acá.  
* ☐ **Nodo final "Felicitaciones"**, con un visual de que termina ahí.  
* ☐ **Nodo examen habilitado por hora.** El nodo y su desbloqueo son nuestros (HU-01); el contenido del examen lo arman desafíos (G04/G09).

### **Ranking**

* ☐ **Ranking por grupo que hoy da error.** Ver por qué no se ve; explicar que todas las evaluaciones son del mismo curso y definir si el default es por curso.

### **Mundo y Archibaldo**

* ☐ **Archibaldo como Hernán** aspecto visual.  
* ☐ **Destello en el camino** que guíe por el mapa.  
* ☐ **Hablar con Archibaldo con Enter**, no solo con clic.

### **De todos los grupos (hacemos nuestra parte)**

* ☐ **Seed de la demo con un curso entero:** nuestra BD con un roadmap completo y curado.  
* ☐ **Permisos en los endpoints en vez de roles.** Hoy hay unos 16 hasRole/hasAnyRole en Roadmap para listar y migrar.  
* ☐ **Documentación global del micro Roadmap.**  
* ☐ **Dashboard, entre todos.** Lo arma G06; nosotros definimos qué datos aportamos (progreso, ranking, XP).

## **2\. No son nuestros**

No los hacemos nosotros; incluye los 5 de la primera parte que no son de Roadmap.

| Ítem | Dueño | Por qué / qué hacemos igual |
| :---- | :---- | :---- |
| Usuarios demo admin, profe y alumno (1ª parte) | G07 Users | Los usuarios son de Users. Nosotros solo los usamos en el seed |
| Quitar UUID del curso en buscadores y selects (1ª parte) | G06 y G12 | El UUID aparece en admin (alertas, reportes, panel docente) y en accounting; en nuestras pantallas no. La regla general aplica igual |
| Parámetros globales en el BackOffice (1ª parte) | G06 | Épica "G06 \- Parámetros Globales". Nosotros leemos los que nos tocan (curva de XP) |
| Auditoría por curso, profesores (1ª parte) | G06 | Pantalla admin/11-admin-audit. Les mandamos nuestros eventos |
| Drag and drop del orden del desafío (1ª parte) | Probablemente G04 | El reordenar ya existe en el armado de cuestionarios de desafíos teóricos |
| Vista cross-curso del dashboard del admin | G06 | Dashboard y KPIs en admin |
| Rango de fechas default en el reporte | G06 | admin/15-report-builder |
| Roles y permisos desde parámetros globales | G06 | Administración de la plataforma |
| Alertas | G06 | Schedule configurable; acción en cada alerta; cards de distinto tamaño |
| Permitir sumar parámetros globales | G06 | Igual que el de arriba |
| Chat y canales externos | G02 | Telegram/Discord \+ instructivo; navegación chat y chat del curso |
| Creación de desafíos | G04 / G09 | Puntaje de aprobación; cerrar/entregar; entrega tardía; lista sábana; aclarar inputs; "Admite variante LLM"; rúbrica vs. prompt; draft o publicar; título repetido |
| Resolución y corrección de desafíos | G04 / G09 | Nota visible al corregir; vista elegida por el alumno; teóricos vs. prácticos; tipo de desafío abierto |
| Git de desafíos | G04 / G09 | Slug del repo; mensaje de commit; git clone; link a vscode web |

