# Contributing

## Development setup

Use Python 3.10 or newer and install `requirements-dev.txt`. Run all checks before opening a pull request:

```bash
python -m unittest discover -s tests -v
python scripts/validate_skill.py
python scripts/validate_evidence.py examples/paper-evidence.example.json
```

Do not commit copyrighted PDFs, extracted paper figures, private vault paths, caches, generated notes, or API credentials.

## Compatibility

- Preserve existing `paper-evidence.json` fields within a major schema version.
- Add optional fields for backward-compatible changes.
- Provide a migration script before changing or removing required fields.
- Preserve `user_annotations` during every migration and automated update.
- Keep `SKILL.md` concise; put mode-specific mechanics in `references/`.

## Testing

Behavioral changes need tests for observable invariants. Parser and extractor fixes should include a minimal synthetic or redistributable fixture. Do not test generated prose wording.

## Release checklist

1. Update `CHANGELOG.md` and version constants.
2. Run tests on Python 3.10–3.12 through CI.
3. Run the Skill validator supplied by the target Agent runtime.
4. Validate the example and at least one real, private smoke-test manifest.
5. Verify a quick-to-deep incremental upgrade does not overwrite user annotations.
6. Tag `vMAJOR.MINOR.PATCH` and publish release notes describing schema compatibility.
