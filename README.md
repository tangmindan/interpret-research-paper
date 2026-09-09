# interpret-research-paper

A Chinese-first Codex/Agent Skill for evidence-grounded interpretation of scientific papers. It extracts and visually verifies complete paper figures, explains result panels and methods, separates observation from interpretation and evidence boundaries, and produces reusable Obsidian notes, literature-sharing slides, or accessible articles.

## Why this skill

Most paper readers optimize for summaries. This project optimizes for traceability: claims stay close to figures, panels, methods, statistics, and limitations. A machine-readable `paper-evidence.json` supports caching and incremental updates without overwriting user annotations.

The entrypoint is intentionally thin. `SKILL.md` keeps cross-task evidence rules and routes to task-specific files under `references/`; a quick read does not load Obsidian, slide, article, or deep-statistics instructions unnecessarily.

Scientific reasoning is modeled separately from evidence storage. Stable result units connect prior finding → current question → experimental rationale → strategy → answer → evidence boundary → next question. The same units can be projected into source-Figure order, a scientific logic chain, or an audience-oriented presentation without changing the underlying evidence.

## Modes

- `quick`: first-pass triage.
- `standard`: complete reusable note; default.
- `deep`: panel-level, supplement-aware, review/presentation-grade analysis.

Depth is independent from narrative:

- `figure`: follow the paper's source order for audit and close reading.
- `logic-chain`: organize by scientific dependencies and inferential advances.
- `presentation`: construct an audience-oriented storyboard and record reorder rationale.

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
python scripts/paper_evidence.py init --source paper.pdf --doi 10.xxxx/example --mode standard --narrative logic-chain --output paper-evidence.json
```

Check what must be recomputed:

```bash
python scripts/paper_evidence.py plan paper-evidence.json --source paper.pdf --mode deep --narrative presentation
```

Enrich an older manifest while preserving annotations:

```bash
python scripts/paper_evidence.py migrate paper-evidence.json --narrative logic-chain
```

Validate it:

```bash
python scripts/validate_evidence.py paper-evidence.json
```

The canonical paper identity uses DOI, PMID, arXiv ID, or a source hash in that order. Exact file editions use a separate SHA-256 fingerprint. Changes invalidate only dependent stages.

`result_units` bridge evidence and writing. `presentation_plans` store audience, goal, source order, presentation order, reorder reasons, and one-or-more-slide modules. A result maps to a slide module, not rigidly to one slide.

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
