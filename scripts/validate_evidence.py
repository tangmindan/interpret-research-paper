#!/usr/bin/env python3
"""Validate paper-evidence JSON against the bundled schema."""

import argparse
import json
from pathlib import Path

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()
    root = Path(__file__).parents[1]
    schema = json.loads((root / "schemas" / "paper-evidence.schema.json").read_text(encoding="utf-8"))
    evidence = json.loads(args.evidence.read_text(encoding="utf-8"))
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        missing = [name for name in schema["required"] if name not in evidence]
        if missing:
            raise SystemExit("missing required fields: " + ", ".join(missing))
        canonical_id = evidence.get("paper_id", {}).get("canonical_id", "")
        source_hash = evidence.get("source", {}).get("source_sha256", "")
        if not any(canonical_id.startswith(prefix) for prefix in ("doi:", "pmid:", "arxiv:", "sha256:")):
            raise SystemExit("invalid paper_id.canonical_id")
        if len(source_hash) != 64 or any(character not in "0123456789abcdef" for character in source_hash):
            raise SystemExit("invalid source.source_sha256")
        print("warning: jsonschema is not installed; core invariants only")
    else:
        errors = sorted(Draft202012Validator(schema).iter_errors(evidence), key=lambda error: list(error.path))
        if errors:
            for error in errors:
                print(f"{'.'.join(map(str, error.path)) or '<root>'}: {error.message}")
            raise SystemExit(1)
    print(f"valid: {args.evidence}")


if __name__ == "__main__":
    main()
