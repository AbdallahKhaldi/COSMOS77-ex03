"""Tests for the tex/ project assembler (B11, B8 routing)."""

from __future__ import annotations

import json

from cosmos77_ex03.crew.schemas import Chapter, Citation, Outline
from cosmos77_ex03.latex import assemble as asm


def test_assemble_writes_full_project(tmp_path, mocker):
    out_dir = tmp_path / "output"
    (out_dir / "chapters").mkdir(parents=True)
    tex_dir = tmp_path / "tex"
    tex_dir.mkdir()
    (out_dir / "chapters" / "ch_01.md").write_text(
        "## Intro\n\nHi \\cite{segal2026}.", encoding="utf-8"
    )
    (out_dir / "chapters" / "ch_02.md").write_text(
        "## עברית\n\nשלום \\cite{segal2026}", encoding="utf-8"
    )
    outline = Outline(
        chapters=[Chapter(index=1, title="Intro"), Chapter(index=2, title="Heb", is_bidi=True)],
        citations=[Citation(key="segal2026", title="Arch")],
    )
    (out_dir / "outline.json").write_text(outline.model_dump_json(), encoding="utf-8")
    (out_dir / "citations.json").write_text(
        json.dumps([c.model_dump() for c in outline.citations]), encoding="utf-8"
    )
    cfg = mocker.Mock()
    cfg.paths.return_value = {"output_dir": str(out_dir), "tex_dir": str(tex_dir)}
    cfg.article.return_value = {"title": "T", "author": "A", "course": "C", "instructor": "I"}

    summary = asm.assemble(cfg)

    assert summary["sections"] == 2
    assert summary["bidi"] == [2]
    assert (tex_dir / "sections" / "ch_01.tex").exists()
    hebrew = (tex_dir / "sections" / "ch_02.tex").read_text(encoding="utf-8")
    assert "\\selectlanguage{hebrew}" in hebrew and "שלום" in hebrew
    assert "segal2026" in (tex_dir / "refs.bib").read_text(encoding="utf-8")
    assert "\\input{sections/ch_01.tex}" in (tex_dir / "main.tex").read_text(encoding="utf-8")
