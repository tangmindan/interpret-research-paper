#!/usr/bin/env python3
"""Check repository-specific skill invariants."""

import json
from pathlib import Path


def main() -> None:
    root = Path(__file__).parents[1]
    required = [
        "SKILL.md", "agents/openai.yaml", "schemas/paper-evidence.schema.json",
        "references/modes.md", "references/evidence-cache.md",
        "scripts/paper_evidence.py", "scripts/extract_pdf_figures.py", "LICENSE", "README.md",
    ]
    missing = [name for name in required if not (root / name).exists()]
    if missing:
        raise SystemExit("missing: " + ", ".join(missing))
    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    for marker in ("name: interpret-research-paper", "quick", "standard", "deep", "paper-evidence.json"):
        if marker not in skill:
            raise SystemExit(f"SKILL.md missing marker: {marker}")
    json.loads((root / "schemas" / "paper-evidence.schema.json").read_text(encoding="utf-8"))
    print("repository invariants: valid")


if __name__ == "__main__":
    main()
