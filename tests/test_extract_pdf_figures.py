import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "extract_pdf_figures.py"
SPEC = importlib.util.spec_from_file_location("extract_pdf_figures", MODULE_PATH)
extractor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(extractor)


class CaptionTests(unittest.TestCase):
    def test_main_caption(self):
        self.assertEqual(extractor.caption_number("Fig. 3 | Result", False), ("Fig", 3))

    def test_extended_caption_requires_flag(self):
        text = "Extended Data Fig. 2 | Validation"
        self.assertIsNone(extractor.caption_number(text, False))
        self.assertEqual(extractor.caption_number(text, True), ("Extended_Data_Fig", 2))


if __name__ == "__main__":
    unittest.main()
