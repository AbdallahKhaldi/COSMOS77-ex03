"""The SDK — the single entry point for all business logic (CLAUDE.md rule 2).

CLI, crew entry, and external callers use only this class. Phase 2 ships the
skeleton: Config + Gatekeeper wiring and ``NotImplementedError`` stubs that later
phases fill (research -> write -> figures -> assemble -> build -> qa).
"""

from __future__ import annotations

from typing import Any

from cosmos77_ex03.shared.config import Config
from cosmos77_ex03.shared.gatekeeper import Gatekeeper


class SDK:
    """Facade over the research -> write -> figures -> LaTeX -> PDF pipeline."""

    def __init__(self, config: Config | None = None, gatekeeper: Gatekeeper | None = None) -> None:
        self.config = config or Config()
        self.gatekeeper = gatekeeper or Gatekeeper()

    def run(self, topic: str | None = None) -> dict[str, Any]:
        """Full pipeline: research -> write -> figures -> assemble -> build -> qa."""
        self.research()
        self.write_chapters()
        self.make_figures()
        self.assemble_latex()
        self.build_pdf()
        return self.qa_pdf()

    def smoke(self) -> str:
        """Run the one-agent Gemini smoke crew, record usage, return the reply."""
        from cosmos77_ex03.crew.smoke import run_smoke

        text, usage = run_smoke(self.config)
        self.gatekeeper.record(usage)
        return text

    def research(self) -> Any:
        """Run the research + outline tasks; persist artifacts; record usage."""
        from cosmos77_ex03.crew.research_run import run_research

        outline, usage = run_research(self.config)
        self.gatekeeper.record(usage)
        return outline

    def write_chapters(self) -> Any:
        """Write all chapters in parallel + stitch the article; record usage."""
        from cosmos77_ex03.crew.write_run import run_write

        count, usage = run_write(self.config)
        self.gatekeeper.record(usage)
        return count

    def make_figures(self) -> list[str]:
        """Generate the matplotlib figures into the configured figures dir."""
        from cosmos77_ex03.figures.charts import generate_all

        return generate_all(self.config.paths().get("figures_dir", "tex/figures"))

    def assemble_latex(self) -> dict[str, Any]:
        """Assemble the tex/ project deterministically from chapters + citations."""
        from cosmos77_ex03.latex.assemble import assemble

        return assemble(self.config)

    def build_pdf(self) -> str:
        """Compile tex/main.pdf via the 4-pass LuaLaTeX pipeline; return its path."""
        import subprocess
        from pathlib import Path

        root = Path(__file__).resolve().parents[3]
        tex_dir = root / self.config.paths().get("tex_dir", "tex")
        subprocess.run(["bash", str(root / "scripts" / "build_pdf.sh"), str(tex_dir)], check=True)
        return str(tex_dir / "main.pdf")

    def qa_pdf(self) -> dict[str, Any]:
        """Run the §13.1 PDF QA checklist; return ``{ok, report}``."""
        from pathlib import Path

        from cosmos77_ex03.latex.qa import format_report, has_critical_failure, run_checks

        root = Path(__file__).resolve().parents[3]
        tex_dir = root / self.config.paths().get("tex_dir", "tex")
        checks = run_checks(tex_dir, target_pages=int(self.config.get("article.target_pages", 15)))
        return {"ok": not has_critical_failure(checks), "report": format_report(checks)}

    def spec_sheet(self) -> dict[str, Any]:
        """Return the Spec Sheet from the gatekeeper (provider from config)."""
        return self.gatekeeper.spec_sheet(provider=self.config.active_provider())

    def build_agents(self) -> dict[str, Any]:
        """Build the crew's singleton agents from config (Phase 4)."""
        from cosmos77_ex03.crew.agents import build_agents

        return build_agents(self.config)
