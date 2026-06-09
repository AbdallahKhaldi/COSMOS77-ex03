"""Tests for the cover-PDF field values (exercise number 3, ex03 repo URL)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

_PATH = Path(__file__).resolve().parents[3] / "scripts" / "generate_cover_pdf.py"
_spec = importlib.util.spec_from_file_location("gen_cover", _PATH)
gen = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gen)


def test_exercise_number_and_repo_url():
    fields = dict(gen.build_field_values(exercise_number=3, self_score=85))
    assert fields["Submitting an exercise number"] == "3"
    assert "COSMOS77-ex03" in fields["Link to GITHUB"]
    assert fields["Recommendation for self-scoring"] == "85"
    assert fields["Group ID code"] == "COSMOS77"
    assert fields["A late submission confirmation"] == "no"


def test_students_are_both_partners():
    students = {row[0]: row[1] for row in gen._STUDENTS}
    assert students["Student 1"][0] == "212389712"
    assert students["Student 2"][0] == "323118794"
