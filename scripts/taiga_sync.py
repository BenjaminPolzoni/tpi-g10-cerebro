#!/usr/bin/env python3
"""Baja las épicas, historias y tareas de G10 desde Taiga a notas de Obsidian en taiga/.

Jerarquía: taiga/epicas/ (una nota por épica, con sus HU) → taiga/historias/ (una nota por HU, con sus tareas).

Uso:  python3 scripts/taiga_sync.py
Credenciales: variables de entorno o un .env en la raíz del repo (ver .env.example).
Todo lo que hay en taiga/ se regenera: no editar a mano.
"""
import json
import os
import re
import shutil
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "taiga"
G10 = re.compile(r"\[?G10\]?")


def load_env():
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"'))
    missing = [k for k in ("TAIGA_USERNAME", "TAIGA_PASSWORD") if not os.environ.get(k)]
    if missing:
        sys.exit(f"Faltan variables: {', '.join(missing)} (ver .env.example)")


def api(path, token=None, body=None, page=None):
    base = os.environ.get("TAIGA_BASE_URL", "https://api.taiga.io").rstrip("/")
    if page:
        path += f"{'&' if '?' in path else '?'}page={page}&page_size=100"
    req = urllib.request.Request(f"{base}/api/v1{path}", method="POST" if body else "GET")
    req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    data = json.dumps(body).encode() if body else None
    with urllib.request.urlopen(req, data, timeout=120) as r:
        return json.load(r), r.headers.get("x-pagination-next")


def api_all(path, token):
    # el proyecto es compartido por ~13 grupos: listas grandes, se paginan
    items, page = [], 1
    while True:
        chunk, more = api(path, token, page=page)
        items += chunk
        if not more:
            return items
        page += 1


def is_g10(item):
    tags = [t[0] if isinstance(t, list) else t for t in item.get("tags") or []]
    return bool(G10.search(item.get("subject", ""))) or any("g10" in t.lower() for t in tags)


def code_of(subject, ref):
    m = re.search(r"\b(H[UT])-?(\d+)", subject)
    return f"{m.group(1)}-{int(m.group(2)):02d}" if m else f"US-{ref}"


def clean_subject(subject):
    return re.sub(r"^\s*(\[DEPRECADA\]\s*)?(\[?G10\]?\s*[—-]?\s*)?(H[UT]-?\d+\s*[—-]\s*)?", r"\1", subject).strip()


def who(item):
    info = item.get("assigned_to_extra_info") or {}
    return info.get("full_name_display") or info.get("username") or "Sin asignar"


def status(item):
    return (item.get("status_extra_info") or {}).get("name", "?")


def closed(item):
    return bool((item.get("status_extra_info") or {}).get("is_closed"))


def note_name(code, subject):
    return f"{code} {clean_subject(subject)}"[:90].replace("/", "-").replace(":", " -")


def yaml_str(s):
    return json.dumps(s, ensure_ascii=False)


def main():
    load_env()
    project_id = int(os.environ.get("TAIGA_PROJECT_ID", "1804026"))
    token = api("/auth", body={"type": "normal", "username": os.environ["TAIGA_USERNAME"],
                               "password": os.environ["TAIGA_PASSWORD"]})[0]["auth_token"]
    project = api(f"/projects/{project_id}", token)[0]
    us_url = f"https://tree.taiga.io/project/{project['slug']}/us/"
    milestones = {m["id"]: m["name"] for m in api_all(f"/milestones?project={project_id}", token)}
    epics = [e for e in api_all(f"/epics?project={project_id}", token) if is_g10(e)]
    # historias de las épicas de G10 + las sueltas con tag g10
    found = {}
    for path in [f"/userstories?project={project_id}&epic={e['id']}" for e in epics] + \
                [f"/userstories?project={project_id}&tags={t}" for t in ("g10", "[g10]")]:
        found.update({s["id"]: s for s in api_all(path, token) if is_g10(s)})
    stories = list(found.values())

    shutil.rmtree(OUT, ignore_errors=True)
    (OUT / "historias").mkdir(parents=True)
    (OUT / "epicas").mkdir(parents=True)
    epic_note = {e["id"]: note_name(f"EP-{e['ref']}", e["subject"]) for e in epics}

    rows = []
    for s in sorted(stories, key=lambda s: s["ref"]):
        d = api(f"/userstories/{s['id']}", token)[0]
        tasks = api_all(f"/tasks?user_story={s['id']}", token)
        code = code_of(s["subject"], s["ref"])
        name = note_name(code, s["subject"])
        # una HU puede colgar de varias épicas: se enlaza a todas las de G10
        epic_ids = [e["id"] for e in s.get("epics") or [] if e["id"] in epic_note]
        epic_links = ", ".join(f"[[epicas/{epic_note[i]}|EP-{epic_note[i].split()[0][3:]}]]" for i in epic_ids) or "Sin épica"
        sprint = milestones.get(s.get("milestone"), "Backlog")
        done_tasks = sum(closed(t) for t in tasks)
        rows.append(dict(epics=epic_ids, code=code, name=name, status=status(s), closed=closed(s), who=who(s),
                         sprint=sprint, tasks=f"{done_tasks}/{len(tasks)}"))
        lines = [
            "---",
            f"tags: [tpi, g10, taiga, {code.split('-')[0].lower()}]",
            f"codigo: {code}",
            f"ref: {s['ref']}",
            f"estado: {yaml_str(status(s))}",
            f"responsable: {yaml_str(who(s))}",
            f"epicas: {yaml_str(epic_links)}",
            f"sprint: {yaml_str(sprint)}",
            f"url: {us_url}{s['ref']}",
            "---",
            "",
            f"# {code}: {clean_subject(s['subject'])}",
            "",
            f"> [!info] Generado desde Taiga ({datetime.now():%Y-%m-%d %H:%M}). No editar a mano: correr `scripts/taiga_sync.py`.",
            f"> [Abrir en Taiga]({us_url}{s['ref']}) · Estado: **{status(s)}** · Responsable: **{who(s)}** · Sprint: **{sprint}**",
            f"> Épica: {epic_links} · Tareas cerradas: **{done_tasks}/{len(tasks)}**",
            "",
            d.get("description") or "_Sin descripción en Taiga._",
            "",
            "## Tareas",
            "",
        ]
        lines += [f"- [{'x' if (t.get('status_extra_info') or {}).get('is_closed') else ' '}] "
                  f"#{t['ref']} {t['subject']} · {status(t)} · {who(t)}"
                  for t in sorted(tasks, key=lambda t: t["ref"])] or ["_Sin tareas._"]
        (OUT / "historias" / f"{name}.md").write_text("\n".join(lines) + "\n")

    def hu_table(rs):
        return ["| HU | Estado | Responsable | Sprint | Tareas |", "|---|---|---|---|---|"] + \
               [f"| [[historias/{r['name']}\\|{r['code']}]] {r['name'][len(r['code']) + 1:]} | {r['status']} | "
                f"{r['who']} | {r['sprint']} | {r['tasks']} |" for r in rs]

    def progress(rs):
        return f"{sum(r['closed'] for r in rs)}/{len(rs)}"

    epic_index = []
    for e in sorted(epics, key=lambda e: e["ref"]):
        d = api(f"/epics/{e['id']}", token)[0]
        rs = [r for r in rows if e["id"] in r["epics"]]
        url = us_url.replace("/us/", "/epic/") + str(e["ref"])
        epic_index.append(f"| [[epicas/{epic_note[e['id']]}\\|EP-{e['ref']}]] {clean_subject(e['subject'])} | "
                          f"{status(e)} | {progress(rs)} |")
        lines = [
            "---",
            "tags: [tpi, g10, taiga, epica]",
            f"ref: {e['ref']}",
            f"estado: {yaml_str(status(e))}",
            f"responsable: {yaml_str(who(e))}",
            f"avance: {yaml_str(progress(rs))}",
            f"url: {url}",
            "---",
            "",
            f"# EP-{e['ref']}: {clean_subject(e['subject'])}",
            "",
            f"> [!info] Generado desde Taiga ({datetime.now():%Y-%m-%d %H:%M}). No editar a mano: correr `scripts/taiga_sync.py`.",
            f"> [Abrir en Taiga]({url}) · Estado: **{status(e)}** · Responsable: **{who(e)}** · HU cerradas: **{progress(rs)}**",
            "",
            d.get("description") or "_Sin descripción en Taiga._",
            "",
            "## Historias",
            "",
        ]
        lines += hu_table(rs) if rs else ["_Sin historias de G10._"]
        (OUT / "epicas" / f"{epic_note[e['id']]}.md").write_text("\n".join(lines) + "\n")

    by_status = {}
    for r in rows:
        by_status[r["status"]] = by_status.get(r["status"], 0) + 1
    out = [
        "---", "tags: [tpi, g10, taiga]", f"actualizado: {datetime.now():%Y-%m-%d %H:%M}", "---", "",
        "# Taiga G10", "",
        f"> [!info] Generado el {datetime.now():%Y-%m-%d %H:%M} con `scripts/taiga_sync.py`. No editar a mano.", "",
        "Jerarquía: **épica** (`epicas/`) → **historias** (`historias/`) → **tareas** (dentro de cada historia).", "",
        "**Historias por estado:** " + " · ".join(f"{k}: {v}" for k, v in sorted(by_status.items())), "",
        "## Épicas", "",
        "| Épica | Estado | HU cerradas |", "|---|---|---|",
    ] + epic_index
    orphans = [r for r in rows if not r["epics"]]
    if orphans:
        out += ["", "## Historias sin épica", "", "> [!warning] Entran por el tag `g10`. Conviene asignarles una épica en Taiga.", ""]
        out += hu_table(orphans)
    out += ["", "## Por responsable", ""]
    for person in sorted({r["who"] for r in rows}):
        out.append(f"- **{person}**: " + ", ".join(f"[[historias/{r['name']}|{r['code']}]] ({r['status']})"
                                                   for r in rows if r["who"] == person))
    (OUT / "README.md").write_text("\n".join(out) + "\n")
    print(f"OK: {len(epics)} épicas, {len(rows)} historias, {len(orphans)} sin épica → {OUT}")


if __name__ == "__main__":
    main()
