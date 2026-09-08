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
            args = Namespace(source=source, output=output, mode="standard", doi=None, pmid=None, arxiv=None, figure_extractor_version="1", template_version="1")
            paper_evidence.init_manifest(args)
            data = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(data["mode"], {"requested": "standard", "completed": "none"})
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
            plan = paper_evidence.invalidation_plan(data, source, "standard", "2", "1")
            self.assertEqual(plan["invalidate"], ["figures", "figure_qa", "interpretation", "deliverables"])
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
            plan = paper_evidence.invalidation_plan(data, source, "deep", "1", "1")
            self.assertEqual(plan["invalidate"], ["interpretation", "deliverables"])


if __name__ == "__main__":
    unittest.main()
