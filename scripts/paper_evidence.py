#!/usr/bin/env python3
"""Create and maintain deterministic paper-evidence manifests."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = "1.0.0"
SKILL_VERSION = "1.0.1"
MODES = {"none": 0, "quick": 1, "standard": 2, "deep": 3}
STAGES = ("bibliography", "parse", "source_map", "figures", "figure_qa", "interpretation", "deliverables")
DESCENDANTS = {
    "parse": ("parse", "source_map", "figures", "figure_qa", "interpretation", "deliverables"),
    "figures": ("figures", "figure_qa", "interpretation", "deliverables"),
    "interpretation": ("interpretation", "deliverables"),
    "deliverables": ("deliverables",),
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_doi(value: str) -> str:
    value = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:\s*)", "", value.strip(), flags=re.I)
    return value.lower().rstrip(" .")


def normalize_arxiv(value: str) -> str:
    value = re.sub(r"^https?://arxiv\.org/(abs|pdf)/", "", value.strip(), flags=re.I)
    value = re.sub(r"\.pdf$", "", value, flags=re.I)
    return re.sub(r"v\d+$", "", value, flags=re.I)


def paper_id(source_hash: str, doi: str | None, pmid: str | None, arxiv: str | None) -> dict:
    if doi:
        kind, value = "doi", normalize_doi(doi)
    elif pmid:
        kind, value = "pmid", "".join(re.findall(r"\d", pmid))
        if not value:
            raise ValueError("PMID must contain digits")
    elif arxiv:
        kind, value = "arxiv", normalize_arxiv(arxiv)
    else:
        kind, value = "sha256", source_hash
    if not value:
        raise ValueError(f"Empty {kind} identifier")
    return {"canonical_id": f"{kind}:{value}", "kind": kind, "value": value}


def empty_stage() -> dict:
    return {"status": "pending", "input_hash": None, "completed_at": None, "outputs": []}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def init_manifest(args: argparse.Namespace) -> None:
    source = args.source.resolve()
    source_hash = sha256_file(source)
    data = {
        "schema_version": SCHEMA_VERSION,
        "skill_version": SKILL_VERSION,
        "paper_id": paper_id(source_hash, args.doi, args.pmid, args.arxiv),
        "bibliography": {},
        "source": {"path": str(source), "source_sha256": source_hash, "size_bytes": source.stat().st_size, "version": None},
        "mode": {"requested": args.mode, "completed": "none"},
        "fingerprints": {"source": source_hash, "figure_extractor": args.figure_extractor_version, "templates": args.template_version},
        "stages": {name: empty_stage() for name in STAGES},
        "study": {}, "methods": [], "claims": [], "figures": [], "limitations": [], "code_and_data": {},
        "unresolved": [], "user_annotations": [],
        "history": [{"at": now(), "event": "initialized", "mode": args.mode, "source_sha256": source_hash}],
    }
    save(args.output, data)
    print(json.dumps({"paper_id": data["paper_id"]["canonical_id"], "manifest": str(args.output)}, ensure_ascii=False))


def invalidation_plan(data: dict, source: Path, mode: str, figure_version: str, template_version: str) -> dict:
    changed = []
    invalidate = set()
    source_hash = sha256_file(source)
    if source_hash != data["source"]["source_sha256"]:
        changed.append("source")
        invalidate.update(DESCENDANTS["parse"])
    if figure_version != data.get("fingerprints", {}).get("figure_extractor"):
        changed.append("figure_extractor")
        invalidate.update(DESCENDANTS["figures"])
    if template_version != data.get("fingerprints", {}).get("templates"):
        changed.append("templates")
        invalidate.update(DESCENDANTS["deliverables"])
    completed = data.get("mode", {}).get("completed", "none")
    if MODES[mode] > MODES.get(completed, 0):
        changed.append(f"mode:{completed}->{mode}")
        invalidate.update(DESCENDANTS["interpretation"])
    pending = [name for name, stage in data.get("stages", {}).items() if stage.get("status") != "complete"]
    return {"changed": changed, "invalidate": [s for s in STAGES if s in invalidate], "pending": pending, "reuse": [s for s in STAGES if s not in invalidate and s not in pending], "source_sha256": source_hash}


def plan_manifest(args: argparse.Namespace) -> None:
    data = load(args.manifest)
    print(json.dumps(invalidation_plan(data, args.source.resolve(), args.mode, args.figure_extractor_version, args.template_version), ensure_ascii=False, indent=2))


def stamp_manifest(args: argparse.Namespace) -> None:
    data = load(args.manifest)
    stage = data["stages"][args.stage]
    stage.update({"status": args.status, "input_hash": args.input_hash, "completed_at": now() if args.status == "complete" else None, "outputs": args.output_file})
    if args.completed_mode:
        data["mode"]["completed"] = args.completed_mode
    data["history"].append({"at": now(), "event": "stage_stamped", "stage": args.stage, "status": args.status})
    save(args.manifest, data)


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser()
    commands = root.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init")
    init.add_argument("--source", type=Path, required=True)
    init.add_argument("--output", type=Path, required=True)
    init.add_argument("--mode", choices=("quick", "standard", "deep"), default="standard")
    init.add_argument("--doi"); init.add_argument("--pmid"); init.add_argument("--arxiv")
    init.add_argument("--figure-extractor-version", default="1")
    init.add_argument("--template-version", default="1")
    init.set_defaults(func=init_manifest)
    plan = commands.add_parser("plan")
    plan.add_argument("manifest", type=Path); plan.add_argument("--source", type=Path, required=True)
    plan.add_argument("--mode", choices=("quick", "standard", "deep"), default="standard")
    plan.add_argument("--figure-extractor-version", default="1"); plan.add_argument("--template-version", default="1")
    plan.set_defaults(func=plan_manifest)
    stamp = commands.add_parser("stamp")
    stamp.add_argument("manifest", type=Path); stamp.add_argument("--stage", choices=STAGES, required=True)
    stamp.add_argument("--status", choices=("pending", "complete", "invalid"), required=True)
    stamp.add_argument("--input-hash"); stamp.add_argument("--output-file", action="append", default=[])
    stamp.add_argument("--completed-mode", choices=("quick", "standard", "deep"))
    stamp.set_defaults(func=stamp_manifest)
    return root


if __name__ == "__main__":
    args = parser().parse_args()
    args.func(args)
