"""Tests for the deterministic matplotlib figures (B5)."""

from __future__ import annotations

from pathlib import Path

from cosmos77_ex03.figures import charts


def test_generate_all_writes_two_pdfs(tmp_path):
    paths = charts.generate_all(tmp_path)
    assert len(paths) == 2
    for p in paths:
        data = Path(p).read_bytes()
        assert data.startswith(b"%PDF")
        assert len(data) > 1000
    assert (tmp_path / "adoption.pdf").exists()
    assert (tmp_path / "frameworks.pdf").exists()


def test_individual_figures_are_pdfs(tmp_path):
    assert charts.adoption_curve(tmp_path / "a.pdf").read_bytes().startswith(b"%PDF")
    assert charts.framework_fit(tmp_path / "f.pdf").read_bytes().startswith(b"%PDF")
