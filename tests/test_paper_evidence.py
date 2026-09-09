import importlib.util
import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "paper_evidence.py"
SPEC = importlib.util.spec_from_file_location("paper_evidence", MODULE_PATH)
paper_evidence = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(paper_evidence)

VALIDATOR_PATH = Path(__file__).parents[1] / "scripts" / "validate_evidence.py"
VALIDATOR_SPEC = importlib.util.spec_from_file_location("validate_evidence", VALIDATOR_PATH)
validate_evidence = importlib.util.module_from_spec(VALIDATOR_SPEC)
VALIDATOR_SPEC.loader.exec_module(validate_evidence)


class PaperEvidenceTests(unittest.TestCase):
    def test_identifier_priority_and_normalization(self):
        result = paper_evidence.paper_id("a" * 64, "https://doi.org/10.1000/ABC.1", "123", "2401.001v2")
        self.assertEqual(result["canonical_id"], "doi:10.1000/abc.1")

    def test_arxiv_version_is_not_part_of_logical_identity(self):
        result = paper_evidence.paper_id("a" * 64, None, None, "https://arxiv.org/abs/2401.00001v3")
        self.assertEqual(result["canonical_id"], "arxiv:2401.00001")

    def test_source_hash_fallback(self):
        result = paper_evidence.paper_id("b" * 64, None, None, None)
        self.assertEqual(result["canonical_id"], "sha256:" + "b" * 64)

    def test_init_preserves_required_collections(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "paper.pdf"
            source.write_bytes(b"test source")
            output = root / "paper-evidence.json"
            args = Namespace(source=source, output=output, mode="standard", narrative="logic-chain", doi=None, pmid=None, arxiv=None, figure_extractor_version="1", template_version="1")
            paper_evidence.init_manifest(args)
            data = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(data["mode"], {"requested": "standard", "completed": "none"})
            self.assertEqual(data["narrative"], {"requested": "logic-chain", "completed": []})
            self.assertEqual(data["result_units"], [])
            self.assertEqual(data["presentation_plans"], [])
            self.assertEqual(data["user_annotations"], [])
            self.assertEqual(set(data["stages"]), set(paper_evidence.STAGES))

    def test_incremental_invalidation_is_scoped(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "paper.pdf"
            source.write_bytes(b"same")
            source_hash = paper_evidence.sha256_file(source)
            data = {
                "source": {"source_sha256": source_hash},
                "mode": {"completed": "standard"},
                "fingerprints": {"figure_extractor": "1", "templates": "1"},
                "stages": {name: {"status": "complete"} for name in paper_evidence.STAGES},
            }
            data["narrative"] = {"requested": "logic-chain", "completed": ["logic-chain"]}
            plan = paper_evidence.invalidation_plan(data, source, "standard", "logic-chain", "2", "1")
            self.assertEqual(plan["invalidate"], ["figures", "figure_qa", "interpretation", "reasoning", "deliverables"])
            self.assertIn("bibliography", plan["reuse"])

    def test_mode_upgrade_only_recomputes_interpretation_branch(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "paper.pdf"
            source.write_bytes(b"same")
            source_hash = paper_evidence.sha256_file(source)
            data = {
                "source": {"source_sha256": source_hash},
                "mode": {"completed": "quick"},
                "fingerprints": {"figure_extractor": "1", "templates": "1"},
                "stages": {name: {"status": "complete"} for name in paper_evidence.STAGES},
            }
            data["narrative"] = {"requested": "logic-chain", "completed": ["logic-chain"]}
            plan = paper_evidence.invalidation_plan(data, source, "deep", "logic-chain", "1", "1")
            self.assertEqual(plan["invalidate"], ["interpretation", "reasoning", "deliverables"])

    def test_new_narrative_only_invalidates_deliverables(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "paper.pdf"
            source.write_bytes(b"same")
            source_hash = paper_evidence.sha256_file(source)
            data = {
                "source": {"source_sha256": source_hash},
                "mode": {"completed": "deep"},
                "narrative": {"requested": "logic-chain", "completed": ["logic-chain"]},
                "fingerprints": {"figure_extractor": "1", "templates": "1"},
                "stages": {name: {"status": "complete"} for name in paper_evidence.STAGES},
            }
            plan = paper_evidence.invalidation_plan(data, source, "deep", "presentation", "1", "1")
            self.assertEqual(plan["invalidate"], ["deliverables"])
            self.assertIn("reasoning", plan["reuse"])

    def test_migration_preserves_annotations_and_adds_reasoning_fields(self):
        with tempfile.TemporaryDirectory() as folder:
            manifest = Path(folder) / "paper-evidence.json"
            annotation = {"text": "keep me"}
            manifest.write_text(json.dumps({
                "schema_version": "1.0.0", "skill_version": "1.0.2",
                "stages": {}, "user_annotations": [annotation], "history": []
            }), encoding="utf-8")
            paper_evidence.migrate_manifest(Namespace(manifest=manifest, output=None, narrative="logic-chain"))
            data = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(data["user_annotations"], [annotation])
            self.assertIn("reasoning", data["stages"])
            self.assertEqual(data["result_units"], [])
            self.assertEqual(data["presentation_plans"], [])

    def test_storyboard_rejects_unknown_result_reference(self):
        evidence = {
            "result_units": [{"result_id": "R1", "depends_on": []}],
            "presentation_plans": [{
                "plan_id": "talk", "source_order": ["R1"], "presentation_order": ["R2"], "modules": []
            }],
        }
        errors = validate_evidence.semantic_errors(evidence)
        self.assertTrue(any("unknown result IDs" in error for error in errors))

    def test_storyboard_slide_count_must_match_slides(self):
        evidence = {
            "result_units": [{"result_id": "R1", "depends_on": []}],
            "presentation_plans": [{
                "plan_id": "talk", "source_order": ["R1"], "presentation_order": ["R1"],
                "modules": [{"result_id": "R1", "slide_count": 2, "slides": [{}]}],
            }],
        }
        errors = validate_evidence.semantic_errors(evidence)
        self.assertTrue(any("slide_count" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
