#!/usr/bin/env python3
"""Validate paper-evidence JSON against the bundled schema."""

import argparse
import json
from pathlib import Path


def semantic_errors(evidence: dict) -> list[str]:
    errors = []
    result_units = evidence.get("result_units", [])
    result_ids = [unit.get("result_id") for unit in result_units]
    if len(result_ids) != len(set(result_ids)):
        errors.append("result_units must have unique result_id values")
    known = set(result_ids)
    for unit in result_units:
        missing = set(unit.get("depends_on", [])) - known
        if missing:
            errors.append(f"{unit.get('result_id', '<unknown>')}.depends_on contains unknown result IDs: {sorted(missing)}")
    for plan in evidence.get("presentation_plans", []):
        for field in ("source_order", "presentation_order"):
            missing = set(plan.get(field, [])) - known
            if missing:
                errors.append(f"{plan.get('plan_id', '<unknown>')}.{field} contains unknown result IDs: {sorted(missing)}")
        for module in plan.get("modules", []):
            if module.get("result_id") not in known:
                errors.append(f"{plan.get('plan_id', '<unknown>')} module references unknown result_id: {module.get('result_id')}")
            if module.get("slide_count") != len(module.get("slides", [])):
                errors.append(f"{plan.get('plan_id', '<unknown>')} module slide_count does not match slides")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()
    root = Path(__file__).parents[1]
    schema = json.loads((root / "schemas" / "paper-evidence.schema.json").read_text(encoding="utf-8"))
    evidence = json.loads(args.evidence.read_text(encoding="utf-8"))
    semantic = semantic_errors(evidence)
    if semantic:
        for error in semantic:
            print(error)
        raise SystemExit(1)
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
        narrative = evidence.get("narrative")
        if narrative is not None and narrative.get("requested") not in {"figure", "logic-chain", "presentation"}:
            raise SystemExit("invalid narrative.requested")
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
