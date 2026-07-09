#!/usr/bin/env python3
"""Gera categorias/<categoria>.qmd e index.qmd a partir de figuras/ + _build/.

Uso:
    python3 scripts/generate_gallery.py

Não edite os arquivos em categorias/ à mão — eles são sobrescritos toda
vez que este script roda. Rode scripts/build_figuras.py antes, para que
as figuras já tenham PNG/SVG/EPS gerados em _build/.
"""
from __future__ import annotations

import html
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
FIGURAS_DIR = ROOT / "figuras"
BUILD_DIR = ROOT / "_build"
CATEGORIAS_DIR = ROOT / "categorias"
BANCO_DIR = ROOT / "banco"

CATEGORY_LABELS = {
    "controle-classico": "Controle Clássico",
    "controle-estados": "Controle por Espaço de Estados",
    "controle-digital": "Controle Digital",
    "circuitos-ca": "Circuitos CA",
    "metodos-numericos": "Métodos Numéricos",
    "identificacao": "Identificação de Sistemas",
    "koopman": "Koopman",
    "mpc-dmc": "MPC / DMC",
}


def label_for(categoria: str) -> str:
    return CATEGORY_LABELS.get(categoria, categoria.replace("-", " ").title())


def load_meta(tikz_path: Path) -> dict:
    meta_path = tikz_path.with_suffix(".meta.yml")
    if meta_path.exists():
        with open(meta_path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


def card_html(tikz_path: Path, categoria: str) -> str:
    nome = tikz_path.stem
    meta = load_meta(tikz_path)
    title = meta.get("title", nome)
    description = meta.get("description", "")
    tags = meta.get("tags", [categoria])

    build_dir = BUILD_DIR / categoria / nome
    prefix = f"../_build/{categoria}/{nome}"
    has_build = (build_dir / f"{nome}.png").exists()

    tags_html = "".join(f'<span class="figura-tag">{html.escape(t)}</span>' for t in tags)

    if has_build:
        preview = f'<img src="{prefix}/{nome}.png" alt="{html.escape(title)}" loading="lazy">'
        downloads = "".join(
            f'<a class="figura-download" href="{prefix}/{nome}.{ext}" download>{label}</a>'
            for ext, label in [
                ("png", "PNG"),
                ("svg", "SVG"),
                ("eps", "EPS"),
                ("tikz", ".tikz"),
                ("tex", ".tex"),
            ]
        )
    else:
        preview = '<div class="figura-pendente">ainda não compilada — rode scripts/rebuild.sh</div>'
        downloads = ""

    codigo = html.escape(tikz_path.read_text(encoding="utf-8"))

    return f"""<div class="figura-card">
  <div class="figura-preview">{preview}</div>
  <div class="figura-body">
    <h3>{html.escape(title)}</h3>
    <p>{html.escape(description)}</p>
    <div class="figura-tags">{tags_html}</div>
    <div class="figura-downloads">{downloads}</div>
    <details>
      <summary>Ver código TikZ</summary>
      <pre><code>{codigo}</code></pre>
    </details>
  </div>
</div>"""


def write_categoria_page(categoria_dir: Path) -> int:
    categoria = categoria_dir.name
    tikz_files = sorted(categoria_dir.glob("*.tikz"))
    cards = "\n".join(card_html(p, categoria) for p in tikz_files)

    content = f"""---
title: "{label_for(categoria)}"
---

{len(tikz_files)} figura(s) nesta categoria. Fonte em `figuras/{categoria}/`.

````{{=html}}
<div class="figura-grid">
{cards}
</div>
````
"""
    CATEGORIAS_DIR.mkdir(exist_ok=True)
    (CATEGORIAS_DIR / f"{categoria}.qmd").write_text(content, encoding="utf-8")
    return len(tikz_files)


def write_index(counts: dict[str, int]) -> None:
    cards = []
    for categoria, count in sorted(counts.items()):
        cards.append(
            f"""<a class="categoria-card" href="categorias/{categoria}.qmd">
  <h3>{label_for(categoria)}</h3>
  <p>{count} figura(s)</p>
</a>"""
        )

    banco_files = sorted(BANCO_DIR.glob("*.tikz"))
    banco_note = (
        f"\n> **Banco de entrada:** {len(banco_files)} figura(s) aguardando "
        "categorização em `banco/`."
        if banco_files
        else ""
    )

    content = f"""---
title: "Coleção TikZ"
---

Coleção organizada de figuras TikZ reutilizáveis nas disciplinas e
projetos de pesquisa. Cada figura pode ser baixada em PNG, SVG, EPS ou
como fonte `.tikz` / `.tex` standalone. Veja `SCOPE.md` para o desenho
completo e `README.md` para o fluxo de contribuição.
{banco_note}

````{{=html}}
<div class="categoria-grid">
{chr(10).join(cards)}
</div>
````
"""
    (ROOT / "index.qmd").write_text(content, encoding="utf-8")


def main() -> None:
    counts = {}
    for categoria_dir in sorted(FIGURAS_DIR.iterdir()):
        if not categoria_dir.is_dir():
            continue
        counts[categoria_dir.name] = write_categoria_page(categoria_dir)
        print(f"  categorias/{categoria_dir.name}.qmd ({counts[categoria_dir.name]} figuras)")
    write_index(counts)
    print("  index.qmd")


if __name__ == "__main__":
    main()
