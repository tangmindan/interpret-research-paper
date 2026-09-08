# interpret-research-paper

A Chinese-first Codex/Agent Skill for evidence-grounded interpretation of scientific papers. It extracts and visually verifies complete paper figures, explains result panels and methods, separates observation from interpretation and evidence boundaries, and produces reusable Obsidian notes, literature-sharing slides, or accessible articles.

## Why this skill

Most paper readers optimize for summaries. This project optimizes for traceability: claims stay close to figures, panels, methods, statistics, and limitations. A machine-readable `paper-evidence.json` supports caching and incremental updates without overwriting user annotations.

The entrypoint is intentionally thin. `SKILL.md` keeps cross-task evidence rules and routes to task-specific files under `references/`; a quick read does not load Obsidian, slide, article, or deep-statistics instructions unnecessarily.

## Modes

- `quick`: first-pass triage.
- `standard`: complete reusable note; default.
- `deep`: panel-level, supplement-aware, review/presentation-grade analysis.

## Install

Copy or clone this directory into your Agent Skills directory. For Codex, a common location is:

```text
~/.codex/skills/interpret-research-paper
```

Install runtime dependencies:

```bash
python -m pip install -r requirements.txt
```

Invoke it with a local paper, for example:

```text
Use $interpret-research-paper in standard mode to interpret this PDF as a Chinese Obsidian note.
```

For persistent Obsidian or slide output, pass `vault_root`, `note_dir`, `figure_dir`, or `ppt_dir` explicitly, or copy `config.example.json` to the ignored local file `.interpret-research-paper.json`. No personal output path is built into the Skill.

## Evidence manifest

Initialize state:

```bash
python scripts/paper_evidence.py init --source paper.pdf --doi 10.xxxx/example --mode standard --output paper-evidence.json
```

Check what must be recomputed:

```bash
python scripts/paper_evidence.py plan paper-evidence.json --source paper.pdf --mode deep
```

Validate it:

```bash
python scripts/validate_evidence.py paper-evidence.json
```

The canonical paper identity uses DOI, PMID, arXiv ID, or a source hash in that order. Exact file editions use a separate SHA-256 fingerprint. Changes invalidate only dependent stages.

## Figure extraction

```bash
python scripts/extract_pdf_figures.py paper.pdf figures --keep-candidates
```

Automatic crops are always marked for visual review. The Skill forbids embedding a low-confidence or unchecked crop as verified evidence.

## Development

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python scripts/validate_skill.py
python scripts/validate_evidence.py examples/paper-evidence.example.json
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for release and compatibility rules.

## Privacy and copyright

The default cache is project-local. Do not commit paper PDFs, extracted copyrighted figures, private notes, caches, or generated deliverables without permission.

## License

MIT. The license covers this Skill and its code, not the papers or figures processed with it.
