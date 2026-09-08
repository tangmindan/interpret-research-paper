#!/usr/bin/env python3
"""Extract complete main-figure regions from scholarly PDFs for Obsidian."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

__version__ = "1.0.0"

MAIN_CAPTION = re.compile(r"^Fig\.\s*(\d+)\s*[|.:]", re.IGNORECASE)
EXT_CAPTION = re.compile(r"^Extended\s+Data\s+Fig\.\s*(\d+)\s*[|.:]", re.IGNORECASE)


def normalize(text: str) -> str:
    return " ".join(text.replace("\u00ad", "").split())


def caption_number(text: str, include_extended: bool):
    if include_extended:
        match = EXT_CAPTION.match(text)
        if match:
            return "Extended_Data_Fig", int(match.group(1))
    match = MAIN_CAPTION.match(text)
    return ("Fig", int(match.group(1))) if match else None


def is_body(block, page_width: float) -> bool:
    x0, y0, x1, y1, text = block[:5]
    clean = normalize(text)
    lines = [line for line in text.splitlines() if line.strip()]
    words = clean.split()
    return len(lines) >= 2 and len(words) >= 24 and len(clean) >= 140 and (x1 - x0) >= page_width * 0.22


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--dpi", type=int, default=220)
    parser.add_argument("--margin-pt", type=float, default=18.0)
    parser.add_argument("--include-extended", action="store_true")
    parser.add_argument("--keep-candidates", action="store_true", help="Preserve rendered page candidates for visual QA")
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--version", action="version", version=__version__)
    args = parser.parse_args()

    try:
        import fitz
        from PIL import Image
    except ImportError as exc:
        raise SystemExit("PyMuPDF and Pillow are required: python -m pip install pymupdf pillow") from exc

    pdf = args.pdf.resolve()
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    document = fitz.open(pdf)
    manifest = []

    for page_index, page in enumerate(document, start=1):
        blocks = [b for b in page.get_text("blocks", sort=True) if len(b) >= 7 and b[6] == 0]
        captions = []
        for block in blocks:
            text = normalize(block[4])
            number = caption_number(text, args.include_extended)
            if number:
                captions.append((block, text, number))
        if not captions:
            continue

        matrix = fitz.Matrix(args.dpi / 72, args.dpi / 72)
        pixmap = page.get_pixmap(matrix=matrix, alpha=False)
        page_image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
        sx = page_image.width / page.rect.width
        sy = page_image.height / page.rect.height

        for caption_order, (caption, caption_text, (kind, number)) in enumerate(captions):
            caption_top = float(caption[1])
            source_page = page
            source_blocks = blocks
            cross_page = caption_top < 70 and page_index > 1
            next_page = caption_order > 0 and page_index < len(document)
            if next_page:
                source_page = document[page_index]
                source_blocks = [b for b in source_page.get_text("blocks", sort=True) if len(b) >= 7 and b[6] == 0]
                matrix = fitz.Matrix(args.dpi / 72, args.dpi / 72)
                pixmap = source_page.get_pixmap(matrix=matrix, alpha=False)
                page_image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
                sx = page_image.width / source_page.rect.width
                sy = page_image.height / source_page.rect.height
                body = [b for b in source_blocks if is_body(b, source_page.rect.width)]
                first_body = min((float(b[1]) for b in body), default=source_page.rect.height - args.margin_pt)
                bottom_pt = source_page.rect.height - args.margin_pt if first_body < source_page.rect.height * 0.35 else first_body - 4
                top_pt = args.margin_pt
            elif cross_page:
                source_page = document[page_index - 2]
                source_blocks = [b for b in source_page.get_text("blocks", sort=True) if len(b) >= 7 and b[6] == 0]
                matrix = fitz.Matrix(args.dpi / 72, args.dpi / 72)
                pixmap = source_page.get_pixmap(matrix=matrix, alpha=False)
                page_image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
                sx = page_image.width / source_page.rect.width
                sy = page_image.height / source_page.rect.height
                preceding_body = [b for b in source_blocks if is_body(b, source_page.rect.width)]
                top_pt = max((float(b[3]) for b in preceding_body), default=args.margin_pt) + 5
                bottom_pt = source_page.rect.height - args.margin_pt
            else:
                preceding_body = [b for b in source_blocks if float(b[3]) < caption_top - 3 and is_body(b, source_page.rect.width)]
                top_pt = max((float(b[3]) for b in preceding_body), default=args.margin_pt) + 5
                bottom_pt = caption_top - 4
            if bottom_pt - top_pt < 70:
                top_pt = max(args.margin_pt, bottom_pt - source_page.rect.height * 0.48)
            crop_box = (
                round(args.margin_pt * sx),
                round(top_pt * sy),
                round((source_page.rect.width - args.margin_pt) * sx),
                round(bottom_pt * sy),
            )
            cropped = page_image.crop(crop_box)
            filename = f"{kind}_{number:02d}.png"
            cropped.save(out / filename, optimize=True)
            if args.keep_candidates:
                candidate_dir = out / "candidates"
                candidate_dir.mkdir(exist_ok=True)
                for candidate_page in range(max(1, page_index - 1), min(len(document), page_index + 1) + 1):
                    candidate_source = document[candidate_page - 1]
                    candidate_pixmap = candidate_source.get_pixmap(matrix=fitz.Matrix(min(args.dpi, 150) / 72, min(args.dpi, 150) / 72), alpha=False)
                    candidate_image = Image.frombytes("RGB", (candidate_pixmap.width, candidate_pixmap.height), candidate_pixmap.samples)
                    candidate_image.save(candidate_dir / f"{kind}_{number:02d}_page_{candidate_page}.png", optimize=True)
            image_objects = len(source_page.get_images(full=True))
            vector_objects = len(source_page.get_drawings())
            body_chars = sum(len(normalize(b[4])) for b in source_blocks if is_body(b, source_page.rect.width) and float(b[1]) < bottom_pt and float(b[3]) > top_pt)
            low_confidence = (image_objects == 0 and vector_objects < 3) or body_chars > 1200
            manifest.append({
                "figure": f"{kind} {number}",
                "page": page_index + 1 if next_page else (page_index - 1 if cross_page else page_index),
                "file": filename,
                "width": cropped.width,
                "height": cropped.height,
                "caption": caption_text,
                "obsidian_embed": f"![[{filename}]]",
                "crop_points": [args.margin_pt, top_pt, source_page.rect.width - args.margin_pt, bottom_pt],
                "caption_page": page_index,
                "selection": "next-page" if next_page else ("previous-page" if cross_page else "same-page"),
                "requires_visual_review": True,
                "low_confidence": low_confidence,
                "pdf_objects": {"images": image_objects, "vectors": vector_objects, "body_chars_in_crop": body_chars},
                "extractor_version": __version__,
            })

    document.close()
    manifest.sort(key=lambda item: (str(item["figure"]).startswith("Extended"), int(str(item["figure"]).split()[-1])))
    manifest_path = args.manifest.resolve() if args.manifest else out / "figure-manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"figures": len(manifest), "manifest": str(manifest_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()


