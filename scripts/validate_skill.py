#!/usr/bin/env python3
"""Check repository-specific skill invariants."""

import json
import re
from pathlib import Path


def main() -> None:
    root = Path(__file__).parents[1]
    required = [
        "SKILL.md", "agents/openai.yaml", "schemas/paper-evidence.schema.json",
        "references/modes.md", "references/evidence-cache.md", "references/configuration.md",
        "references/interpretation-core.md", "references/figure-workflow.md",
        "references/obsidian-output.md", "references/presentation-guidance.md", "references/wechat-output.md",
        "scripts/paper_evidence.py", "scripts/extract_pdf_figures.py", "LICENSE", "README.md",
    ]
    missing = [name for name in required if not (root / name).exists()]
    if missing:
        raise SystemExit("missing: " + ", ".join(missing))
    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    for marker in ("name: interpret-research-paper", "quick", "standard", "deep", "paper-evidence.json"):
        if marker not in skill:
            raise SystemExit(f"SKILL.md missing marker: {marker}")
    skill_lines = skill.splitlines()
    if len(skill_lines) > 100 or len(skill) > 9000:
        raise SystemExit(f"SKILL.md entrypoint is too large: {len(skill_lines)} lines, {len(skill)} characters")
    for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", skill):
        if "://" not in target and not (root / target).exists():
            raise SystemExit(f"SKILL.md contains a broken local reference: {target}")
    json.loads((root / "schemas" / "paper-evidence.schema.json").read_text(encoding="utf-8"))
    public_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [root / "SKILL.md", root / "README.md", *sorted((root / "references").glob("*.md"))]
    )
    forbidden = ("D:\\Notes\\", "C:\\Users\\", "/Users/", "/home/")
    matches = [value for value in forbidden if value in public_text]
    if matches:
        raise SystemExit("public instructions contain personal absolute paths: " + ", ".join(matches))
    print("repository invariants: valid")


if __name__ == "__main__":
    main()
