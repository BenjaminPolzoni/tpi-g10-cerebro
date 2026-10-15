---
tags: [tpi, g10, guia]
---

# Cómo usar el cerebro

## 1. Clonar y abrir en Obsidian (una sola vez)

```bash
git clone https://github.com/BenjaminPolzoni/tpi-g10-cerebro.git
```

1. Abrir Obsidian → *Open folder as vault* → elegir la carpeta `tpi-g10-cerebro`.
2. Cuando pregunte, **confiar en el vault** (habilita los plugins).
3. El plugin **Obsidian Git** ya viene instalado en el repo. Si Obsidian muestra "Restricted mode", ir a *Settings → Community plugins → Turn on community plugins* y verificar que **Git** esté activado.
   La configuración también viene en el repo: trae cambios al abrir y cada 5 minutos, y guarda y sube los tuyos cada 5 minutos.

> [!warning] Abrir el vault correcto
> Los comandos `Obsidian Git: ...` solo aparecen con **este** vault abierto. Si tenés otro vault, cambiá desde el ícono de vaults (abajo a la izquierda) → *Open folder as vault*.

> [!tip] Sin Obsidian
> Son archivos Markdown: se pueden leer y editar desde GitHub o cualquier editor. Los diagramas Mermaid y las cajas de aviso se ven en GitHub también.

### En una compu nueva

1. **Instalar Git y Obsidian.** En macOS, `xcode-select --install` trae Git. Verificar con `git --version`.
2. **Configurar tu identidad de Git** (sin esto, Obsidian Git no puede commitear):
   ```bash
   git config --global user.name "Tu nombre"
   git config --global user.email "tu-mail-de-github@ejemplo.com"
   ```
3. **Autenticarse con GitHub** para poder subir tus cambios. Lo más simple es instalar la CLI de GitHub y loguearse por navegador:
   ```bash
   brew install gh
   gh auth login        # elegir GitHub.com → HTTPS → Login with a web browser
   ```
   Si preferís SSH, cargá tu clave pública en GitHub y clonar con `git@github.com:BenjaminPolzoni/tpi-g10-cerebro.git`.
4. **Clonar** en la carpeta donde guardes los proyectos (por ejemplo `~/dev/TPI_2026/`):
   ```bash
   git clone https://github.com/BenjaminPolzoni/tpi-g10-cerebro.git
   cd tpi-g10-cerebro && git status    # debe decir "On branch main" y "up to date"
   ```
5. **Abrir en Obsidian:** *Open folder as vault* → elegir `tpi-g10-cerebro` → confiar en el vault. La configuración del plugin Git viene en el repo, así que no hace falta cargarla a mano.
6. **Verificar el enlace:** *Command palette* → **Obsidian Git: Pull**. Tiene que terminar sin errores.
   - Si dice que no encuentra `git`: *Settings → Obsidian Git → Custom Git binary path* con la salida de `which git`.
   - Si no pide ni trae nada, revisar que el plugin esté activo (ver el paso 3 de arriba).

> [!warning] No usar otro vault
> Este repo es el único que se sincroniza. Un vault personal (por ejemplo en `Documents/`) no tiene git: abrir siempre la carpeta clonada.

## 2. Editar

- Crear notas nuevas con las plantillas: *Command palette* (`Cmd/Ctrl + P`) → **Templates: Insert template** → `acuerdo`, `decision` o `minuta`.
- Para linkear otra nota: `[[` y elegir.
- Obsidian Git sube solo. Para forzarlo: *Command palette* → **Obsidian Git: Commit-and-sync**.

> [!warning] Conflictos
> Si dos editan **el mismo párrafo** a la vez, Obsidian Git avisa del conflicto. Se resuelve como en cualquier repo: quedarse con las dos versiones y unirlas a mano. Para evitarlo, en notas compartidas (acuerdos) agregar al final en vez de reescribir.

## 3. Actualizar Taiga

```bash
cp .env.example .env    # una vez: completar TAIGA_USERNAME y TAIGA_PASSWORD (tu cuenta de Taiga)
python3 scripts/taiga_sync.py
```

- Tarda unos 2 minutos: el proyecto de Taiga lo comparten unos 13 grupos.
- Reescribe todo `taiga/`. Después hay que commitear y subir los cambios (o dejar que Obsidian Git lo haga).
- Una HU entra si pertenece a una **épica de G10** o tiene el **tag `g10` / `[g10]`**. Si una HU nueva no aparece, agregarle el tag en Taiga.

### Qué trae y cómo se organiza

Respeta la jerarquía de Taiga: **épica → historias → tareas**.

| Nivel | Dónde queda | Qué trae |
|---|---|---|
| Épica | `taiga/epicas/EP-<ref> ….md` | Estado, responsable, descripción completa (objetivo, supuestos, criterios a nivel épico) y tabla de sus HU con avance |
| Historia (HU / HT) | `taiga/historias/<código> ….md` | Estado, responsable, sprint, link a su(s) épica(s), descripción con criterios de aceptación y avance de tareas |
| Tarea | Dentro de la nota de su historia | Checklist con número, estado y responsable. No tienen nota propia |
| Índice | `taiga/README.md` | Épicas con HU cerradas, historias sin épica y quién tiene qué |

- Una HU que cuelga de varias épicas aparece en todas.
- Las épicas que no tienen HU de G10 (las "FUERA DE ALCANCE", Avatares, Racha) igual tienen nota, con "Sin historias de G10".
- No trae: comentarios, adjuntos, historial de cambios ni issues de Taiga.

> [!danger] Credenciales
> El `.env` está en `.gitignore`. Nunca commitear usuarios, contraseñas ni tokens.
