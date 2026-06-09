"""Deterministic matplotlib figures for the article (B5: the Python-generated graph).

Two data-driven charts saved as vector PDFs into ``tex/figures/``: the enterprise
agent-adoption curve (2023->2026 projection) and a framework production-fit
comparison. Data is fixed (no randomness) so the figures are byte-reproducible.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
from matplotlib import pyplot as plt  # noqa: E402

#: Enterprise AI-agent adoption (% of enterprises with agents in production).
_ADOPTION_YEARS = ["2023", "2024", "2025", "2026 (proj.)"]
_ADOPTION_PCT = [1, 5, 11, 40]

#: Illustrative production-fit score (0-10) per framework, 2026.
_FRAMEWORKS = ["LangGraph", "CrewAI", "AutoGen", "LlamaIndex", "PydanticAI", "DSPy"]
_FIT_SCORES = [9, 8, 7, 7, 8, 6]


def adoption_curve(out_path: Path | str) -> Path:
    """Save the 2023->2026 enterprise agent-adoption curve as a PDF (B5)."""
    fig, ax = plt.subplots(figsize=(6.0, 3.5))
    ax.plot(_ADOPTION_YEARS, _ADOPTION_PCT, marker="o", linewidth=2.0, color="#1f77b4")
    for x, y in zip(_ADOPTION_YEARS, _ADOPTION_PCT, strict=True):
        ax.annotate(f"{y}%", (x, y), textcoords="offset points", xytext=(0, 8), ha="center")
    ax.set_title("Enterprise AI-agent adoption, 2023–2026 (projected)")
    ax.set_ylabel("% of enterprises in production")
    ax.set_ylim(0, 50)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out = Path(out_path)
    fig.savefig(out, format="pdf")
    plt.close(fig)
    return out


def framework_fit(out_path: Path | str) -> Path:
    """Save the 2026 framework production-fit comparison as a PDF."""
    fig, ax = plt.subplots(figsize=(6.0, 3.5))
    bars = ax.barh(_FRAMEWORKS, _FIT_SCORES, color="#2ca02c")
    ax.set_xlim(0, 10)
    ax.set_xlabel("Production-fit score (0–10)")
    ax.set_title("Agent framework production-fit, 2026")
    ax.invert_yaxis()
    ax.bar_label(bars, padding=3)
    fig.tight_layout()
    out = Path(out_path)
    fig.savefig(out, format="pdf")
    plt.close(fig)
    return out


def generate_all(figures_dir: Path | str) -> list[str]:
    """Generate both figures into ``figures_dir``; return the written paths."""
    base = Path(figures_dir)
    base.mkdir(parents=True, exist_ok=True)
    return [
        str(adoption_curve(base / "adoption.pdf")),
        str(framework_fit(base / "frameworks.pdf")),
    ]
