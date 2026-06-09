"""Assemble the complete ``tex/`` LaTeX project from crew artifacts (B11).

Deterministic builder: reads ``output/outline.json`` + ``output/chapters/*.md``,
converts each chapter to ``tex/sections/ch_NN.tex`` (Hebrew chapter wrapped for
BiDi), writes ``tex/refs.bib`` from ``output/citations.json`` (every cited key
resolved), and writes ``tex/main.tex``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

from cosmos77_ex03.crew.schemas import Outline
from cosmos77_ex03.latex.bib import build_refs_bib, cited_keys
from cosmos77_ex03.latex.convert import md_to_latex
from cosmos77_ex03.latex.document import build_main_tex

if TYPE_CHECKING:
    from cosmos77_ex03.shared.config import Config


def _load_citations(out_dir: str) -> list[dict]:
    path = Path(out_dir, "citations.json")
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


def assemble(cfg: Config) -> dict[str, Any]:
    """Convert chapters -> tex/sections, write refs.bib + main.tex; return a summary."""
    out_dir = cfg.paths().get("output_dir", "output")
    tex_dir = cfg.paths().get("tex_dir", "tex")
    outline = Outline.model_validate_json(Path(out_dir, "outline.json").read_text(encoding="utf-8"))
    sections_dir = Path(tex_dir, "sections")
    sections_dir.mkdir(parents=True, exist_ok=True)
    bodies: list[str] = []
    indices: list[int] = []
    for chapter in outline.chapters:
        md_path = Path(out_dir, "chapters", f"ch_{chapter.index:02d}.md")
        if not md_path.exists():
            continue
        body = md_to_latex(md_path.read_text(encoding="utf-8"), hebrew=chapter.is_bidi)
        (sections_dir / f"ch_{chapter.index:02d}.tex").write_text(body, encoding="utf-8")
        bodies.append(body)
        indices.append(chapter.index)
    citations = _load_citations(out_dir)
    Path(tex_dir, "refs.bib").write_text(
        build_refs_bib(citations, cited_keys(bodies)), encoding="utf-8"
    )
    Path(tex_dir, "main.tex").write_text(build_main_tex(cfg.article(), indices), encoding="utf-8")
    return {
        "sections": len(indices),
        "citations": len(citations),
        "bidi": [c.index for c in outline.chapters if c.is_bidi],
    }
