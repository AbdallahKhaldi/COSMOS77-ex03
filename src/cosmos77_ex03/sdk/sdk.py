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

    def run(self, topic: str | None = None) -> Any:
        """Run the full pipeline (research -> write -> figures -> assemble -> build -> qa)."""
        raise NotImplementedError("SDK.run lands in Phase 9 (full pipeline wiring)")

    def smoke(self) -> str:
        """Run the one-agent Gemini smoke crew, record usage, return the reply."""
        from cosmos77_ex03.crew.smoke import run_smoke

        text, usage = run_smoke(self.config)
        self.gatekeeper.record(usage)
        return text

    def research(self) -> Any:
        """Run the research + outline tasks (Phase 5)."""
        raise NotImplementedError("SDK.research lands in Phase 5")

    def write_chapters(self) -> Any:
        """Run the parallel chapter writers + editor (Phase 6)."""
        raise NotImplementedError("SDK.write_chapters lands in Phase 6")

    def make_figures(self) -> Any:
        """Generate the matplotlib figures + TikZ diagram (Phase 7)."""
        raise NotImplementedError("SDK.make_figures lands in Phase 7")

    def assemble_latex(self) -> Any:
        """Assemble the tex/ project from chapters + figures (Phase 8)."""
        raise NotImplementedError("SDK.assemble_latex lands in Phase 8")

    def build_pdf(self) -> Any:
        """Compile tex/main.pdf via build_pdf.sh (Phase 9)."""
        raise NotImplementedError("SDK.build_pdf lands in Phase 9")

    def qa_pdf(self) -> Any:
        """Validate the PDF against the §13.1 checklist (Phase 9)."""
        raise NotImplementedError("SDK.qa_pdf lands in Phase 9")

    def spec_sheet(self) -> dict[str, Any]:
        """Return the Spec Sheet from the gatekeeper (provider from config)."""
        return self.gatekeeper.spec_sheet(provider=self.config.active_provider())

    def build_agents(self) -> dict[str, Any]:
        """Build the crew's singleton agents from config (Phase 4)."""
        from cosmos77_ex03.crew.agents import build_agents

        return build_agents(self.config)
