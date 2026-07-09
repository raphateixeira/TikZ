#!/usr/bin/env python3
"""Compila figuras/<categoria>/*.tikz para PDF/PNG/SVG/EPS em _build/.

Uso:
    python3 scripts/build_figuras.py [--force] [--only CATEGORIA[/NOME]]

Cada figura vira um documento standalone, compilado com pdflatex e
convertido para os formatos de saída. Build incremental: só recompila se
o .tikz ou o .meta.yml forem mais novos que o .pdf já existente (a menos
que --force seja passado).
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
FIGURAS_DIR = ROOT / "figuras"
BUILD_DIR = ROOT / "_build"

DEFAULT_LIBRARIES = [
    "arrows.meta",
    "positioning",
    "calc",
    "decorations.pathmorphing",
    "patterns",
    "fit",
    "shapes.geometric",
]
DEFAULT_DPI = 300

TEX_TEMPLATE = r"""\documentclass[border=2pt]{{standalone}}
\usepackage{{tikz}}
\usepackage{{amsmath}}
{extra_packages}
\usetikzlibrary{{{libraries}}}
{pgfplots_setup}
\begin{{document}}
\input{{{tikz_file}}}
\end{{document}}
"""


def pgfplots_setup(packages: list[str], meta: dict) -> str:
    if "pgfplots" not in packages:
        return ""
    lines = [r"\pgfplotsset{compat=1.18}"]
    pgf_libs = meta.get("pgfplots_libraries", [])
    if pgf_libs:
        lines.append(r"\usepgfplotslibrary{" + ", ".join(pgf_libs) + "}")
    return "\n".join(lines)


def load_meta(tikz_path: Path) -> dict:
    meta_path = tikz_path.with_suffix(".meta.yml")
    if meta_path.exists():
        with open(meta_path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


def needs_rebuild(tikz_path: Path, meta_path: Path, pdf_path: Path) -> bool:
    if not pdf_path.exists():
        return True
    pdf_mtime = pdf_path.stat().st_mtime
    if tikz_path.stat().st_mtime > pdf_mtime:
        return True
    if meta_path.exists() and meta_path.stat().st_mtime > pdf_mtime:
        return True
    return False


def run(cmd: list[str], cwd: Path) -> None:
    result = subprocess.run(
        cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    if result.returncode != 0:
        print(f"  [ERRO] {' '.join(cmd)}", file=sys.stderr)
        print(result.stdout, file=sys.stderr)
        raise SystemExit(1)


def build_one(tikz_path: Path, categoria: str, force: bool) -> None:
    nome = tikz_path.stem
    meta_path = tikz_path.with_suffix(".meta.yml")
    out_dir = BUILD_DIR / categoria / nome

    pdf_path = out_dir / f"{nome}.pdf"
    if not force and not needs_rebuild(tikz_path, meta_path, pdf_path):
        print(f"  = {categoria}/{nome} (atualizado, pulando)")
        return

    print(f"  > {categoria}/{nome}")
    out_dir.mkdir(parents=True, exist_ok=True)

    meta = load_meta(tikz_path)
    libraries = DEFAULT_LIBRARIES + list(meta.get("libraries", []))
    dpi = int(meta.get("dpi", DEFAULT_DPI))
    packages = list(meta.get("packages", []))

    tex_path = out_dir / f"{nome}.tex"
    tex_path.write_text(
        TEX_TEMPLATE.format(
            extra_packages="\n".join(f"\\usepackage{{{p}}}" for p in packages),
            libraries=", ".join(dict.fromkeys(libraries)),  # dedup mantendo ordem
            pgfplots_setup=pgfplots_setup(packages, meta),
            tikz_file=tikz_path.resolve(),
        ),
        encoding="utf-8",
    )

    run(
        [
            "pdflatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            f"-output-directory={out_dir}",
            str(tex_path),
        ],
        cwd=out_dir,
    )

    run(["pdftoppm", "-r", str(dpi), "-png", f"{nome}.pdf", nome], cwd=out_dir)
    # pdftoppm produz "<nome>-1.png" (ou "<nome>.png" se só houver 1 pagina
    # em versoes recentes); normaliza para "<nome>.png".
    png_candidates = sorted(out_dir.glob(f"{nome}-*.png")) or sorted(
        out_dir.glob(f"{nome}.png")
    )
    if png_candidates and png_candidates[0].name != f"{nome}.png":
        png_candidates[0].rename(out_dir / f"{nome}.png")

    run(["pdf2svg", f"{nome}.pdf", f"{nome}.svg"], cwd=out_dir)
    run(["pdftops", "-eps", f"{nome}.pdf", f"{nome}.eps"], cwd=out_dir)

    shutil.copy2(tikz_path, out_dir / tikz_path.name)

    # limpeza de auxiliares do pdflatex
    for aux_ext in (".aux", ".log"):
        aux_path = out_dir / f"{nome}{aux_ext}"
        aux_path.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="recompila tudo")
    parser.add_argument(
        "--only", help="restringe a uma categoria ou categoria/nome específicos"
    )
    args = parser.parse_args()

    if not FIGURAS_DIR.exists():
        print(f"Pasta não encontrada: {FIGURAS_DIR}", file=sys.stderr)
        raise SystemExit(1)

    only_categoria, only_nome = (args.only.split("/", 1) + [None])[:2] if args.only else (
        None,
        None,
    )

    for categoria_dir in sorted(FIGURAS_DIR.iterdir()):
        if not categoria_dir.is_dir():
            continue
        categoria = categoria_dir.name
        if only_categoria and categoria != only_categoria:
            continue
        print(f"Categoria: {categoria}")
        for tikz_path in sorted(categoria_dir.glob("*.tikz")):
            if only_nome and tikz_path.stem != only_nome:
                continue
            build_one(tikz_path, categoria, args.force)


if __name__ == "__main__":
    main()
