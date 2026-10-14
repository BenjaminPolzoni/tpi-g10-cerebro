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
3. *Settings → Community plugins → Browse* → instalar **Obsidian Git** y activarlo.
   La configuración ya viene en el repo: trae cambios al abrir y cada 5 minutos, y guarda y sube los tuyos cada 5 minutos.

> [!tip] Sin Obsidian
> Son archivos Markdown: se pueden leer y editar desde GitHub o cualquier editor. Los diagramas Mermaid y las cajas de aviso se ven en GitHub también.

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

> [!danger] Credenciales
> El `.env` está en `.gitignore`. Nunca commitear usuarios, contraseñas ni tokens.
