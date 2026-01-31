from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass
from pathlib import Path

from .mdlite import parse_markdown, render_html


@dataclass(frozen=True)
class Note:
    slug: str
    title: str
    html: str


_STYLE = """
:root{ --bg:#070912; --fg:#e9eefb; --muted:rgba(233,238,251,.72); --card:rgba(255,255,255,.06); --border:rgba(255,255,255,.10); --accent:#9bd3ff; }
*{box-sizing:border-box}
body{ margin:0; font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial; background: radial-gradient(1200px 600px at 20% 10%, rgba(155,211,255,.18), transparent 60%), radial-gradient(900px 500px at 80% 0%, rgba(185,167,255,.16), transparent 55%), var(--bg); color:var(--fg); }
main{ max-width:980px; margin:0 auto; padding:44px 20px 60px; }
a{ color:var(--accent); text-decoration:none; } a:hover{ text-decoration:underline; }
.header{ margin-bottom:20px; }
.kicker{ margin:0 0 10px; letter-spacing:.12em; text-transform:uppercase; font-size:12px; color:var(--muted); }
.card{ border:1px solid var(--border); border-radius:16px; padding:16px; background:var(--card); }
.grid{ display:grid; grid-template-columns: 1fr; gap: 14px; }
pre{ overflow:auto; padding:12px; border-radius:12px; background: rgba(0,0,0,.28); border:1px solid var(--border); }
code{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 13px; }
.footer{ margin-top:18px; color:var(--muted); }
""".strip()


def _page(title: str, body: str, *, root: str = "./") -> str:
    stamp = _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <meta name=\"color-scheme\" content=\"dark\" />
  <title>{title}</title>
  <style>{_STYLE}</style>
</head>
<body>
  <main>
    <div class=\"header\">
      <p class=\"kicker\"><a href=\"{root}index.html\">starlibrary</a></p>
    </div>
    {body}
    <div class=\"footer\">
      <p>Built: {stamp}</p>
    </div>
  </main>
</body>
</html>
"""


def _slug_from_path(p: Path) -> str:
    return p.stem.lower().replace(" ", "-")


def build_site(*, notes_dir: Path, out_dir: Path, title: str = "Starlibrary") -> None:
    notes_dir = Path(notes_dir)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    notes: list[Note] = []
    for md in sorted(notes_dir.glob("*.md")):
        raw = md.read_text(encoding="utf-8")
        nodes = parse_markdown(raw.splitlines(True))
        html_body = render_html(nodes)
        note_title = nodes[0].text.strip() if nodes and nodes[0].kind.startswith("h") else md.stem
        slug = _slug_from_path(md)
        notes.append(Note(slug=slug, title=note_title, html=html_body))

        page = _page(f"{note_title} — {title}", f"<article class=\"card\">\n{html_body}\n</article>")
        (out_dir / f"{slug}.html").write_text(page, encoding="utf-8")

    items = "\n".join(
        f"<li><a href=\"./{n.slug}.html\">{n.title}</a></li>" for n in notes
    ) or "<li><span style=\"color:var(--muted)\">No notes yet.</span></li>"

    index_body = f"""
<section class=\"grid\">
  <div class=\"card\">
    <h1>{title}</h1>
    <p style=\"color:var(--muted)\">A small shelf of notes. Plain HTML. No build system.</p>
  </div>
  <div class=\"card\">
    <h2>Notes</h2>
    <ul>\n{items}\n</ul>
  </div>
</section>
""".strip()

    (out_dir / "index.html").write_text(_page(title, index_body), encoding="utf-8")
