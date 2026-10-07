#!/usr/bin/env python3
"""
Academic Paper Batch Text and Equation Extractor
================================================
Batch-extracts full text and equations from academic PDF papers with robust
Unicode/encoding preservation, font-aware math glyph detection, optional ML-based
LaTeX conversion (Nougat / pix2tex), and multi-level OCR/pdfplumber fallbacks.

Author: Antigravity Agent
"""

import os
import sys
import re
import csv
import json
import logging
import argparse
import unicodedata
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any

# Core libraries
try:
    import pymupdf as fitz  # PyMuPDF
except ImportError:
    try:
        import fitz
    except ImportError:
        sys.exit("Error: PyMuPDF is not installed. Run `pip install pymupdf`.")

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import pytesseract
    HAS_PYTESSERACT = True
except ImportError:
    HAS_PYTESSERACT = False

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable, **kwargs):
        return iterable

# Optional ML Equation extraction libraries
HAS_NOUGAT = False
try:
    import torch
    from nougat import NougatModel
    from nougat.utils.checkpoint import get_checkpoint
    from nougat.dataset.rasterize import rasterize_paper
    HAS_NOUGAT = True
except (ImportError, Exception):
    HAS_NOUGAT = False

HAS_PIX2TEX = False
try:
    from pix2tex.cli import LatexOCR
    HAS_PIX2TEX = True
except (ImportError, Exception):
    HAS_PIX2TEX = False


# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("extract_papers")


# =====================================================================
# Font & Symbol Mapping Tables for TeX / Math Fonts
# =====================================================================

MATH_FONT_KEYWORDS = [
    "cmmi", "cmsy", "msam", "msbm", "mtex", "cmex", "symbol", "math",
    "euclid", "stix", "cambria-math", "cambriamath", "asana", "texgyre",
    "wasy", "line", "circle", "eufm", "eurm", "eubm", "bbm"
]

# Standard Adobe Symbol Font mapping (character code -> Unicode)
ADOBE_SYMBOL_MAP = {
    0x21: "!", 0x22: "∀", 0x23: "#", 0x24: "∃", 0x25: "%", 0x26: "&", 0x27: "∷", 0x28: "(",
    0x29: ")", 0x2A: "∗", 0x2B: "+", 0x2C: ",", 0x2D: "−", 0x2E: ".", 0x2F: "/",
    0x30: "0", 0x31: "1", 0x32: "2", 0x33: "3", 0x34: "4", 0x35: "5", 0x36: "6", 0x37: "7",
    0x38: "8", 0x39: "9", 0x3A: ":", 0x3B: ";", 0x3C: "<", 0x3D: "=", 0x3E: ">", 0x3F: "?",
    0x40: "≅", 0x41: "Α", 0x42: "Β", 0x43: "Χ", 0x44: "Δ", 0x45: "Ε", 0x46: "Φ", 0x47: "Γ",
    0x48: "Η", 0x49: "Ι", 0x4A: "ϑ", 0x4B: "Κ", 0x4C: "Λ", 0x4D: "Μ", 0x4E: "Ν", 0x4F: "Ο",
    0x50: "Π", 0x51: "Θ", 0x52: "Ρ", 0x53: "Σ", 0x54: "Τ", 0x55: "Υ", 0x56: "ς", 0x57: "Ω",
    0x58: "Ξ", 0x59: "Ψ", 0x5A: "Ζ", 0x5B: "[", 0x5C: "∴", 0x5D: "]", 0x5E: "⊥", 0x5F: "_",
    0x60: "‾", 0x61: "α", 0x62: "β", 0x63: "χ", 0x64: "δ", 0x65: "ε", 0x66: "ϕ", 0x67: "γ",
    0x68: "η", 0x69: "ι", 0x6A: "ϕ", 0x6B: "κ", 0x6C: "λ", 0x6D: "μ", 0x6E: "ν", 0x6F: "ο",
    0x70: "π", 0x71: "θ", 0x72: "ρ", 0x73: "σ", 0x74: "τ", 0x75: "υ", 0x76: "ϖ", 0x77: "ω",
    0x78: "ξ", 0x79: "ψ", 0x7A: "ζ", 0x7B: "{", 0x7C: "|", 0x7D: "}", 0x7E: "∼",
    0xA0: "€", 0xA1: "ϒ", 0xA2: "′", 0xA3: "≤", 0xA4: "⁄", 0xA5: "∞", 0xA6: "ƒ", 0xA7: "♣",
    0xA8: "♦", 0xA9: "♥", 0xAA: "♠", 0xAB: "↔", 0xAC: "←", 0xAD: "↑", 0xAE: "→", 0xAF: "↓",
    0xB0: "°", 0xB1: "±", 0xB2: "″", 0xB3: "≥", 0xB4: "×", 0xB5: "∝", 0xB6: "∂", 0xB7: "•",
    0xB8: "÷", 0xB9: "≠", 0xBA: "≡", 0xBB: "≈", 0xBC: "…", 0xBD: "│", 0xBE: "─", 0xBF: "↵",
    0xC0: "ℵ", 0xC1: "ℑ", 0xC2: "ℜ", 0xC3: "℘", 0xC4: "⊗", 0xC5: "⊕", 0xC6: "∅", 0xC7: "∩",
    0xC8: "∪", 0xC9: "⊃", 0xCA: "⊇", 0xCB: "⊄", 0xCC: "⊂", 0xCD: "⊆", 0xCE: "∈", 0xCF: "∉",
    0xD0: "∠", 0xD1: "∇", 0xD2: "®", 0xD3: "©", 0xD4: "™", 0xD5: "∏", 0xD6: "√", 0xD7: "⋅",
    0xD8: "¬", 0xD9: "∧", 0xDA: "∨", 0xDB: "⇔", 0xDC: "⇐", 0xDD: "⇑", 0xDE: "⇒", 0xDF: "⇓",
    0xE0: "◇", 0xE1: "⟨", 0xE2: "®", 0xE3: "©", 0xE4: "™", 0xE5: "∑", 0xE6: "⎛", 0xE7: "⎜",
    0xE8: "⎝", 0xE9: "⎡", 0xEA: "⎢", 0xEB: "⎣", 0xEC: "⎧", 0xED: "⎨", 0xEE: "⎩", 0xEF: "⎪",
    0xF1: "⟩", 0xF2: "∫", 0xF3: "⌠", 0xF4: "⎮", 0xF5: "⌡", 0xF6: "⎞", 0xF7: "⎟", 0xF8: "⎠",
    0xF9: "⎤", 0xFA: "⎥", 0xFB: "⎦", 0xFC: "⎫", 0xFD: "⎬", 0xFE: "⎭"
}

# TeX CMSY (Computer Modern Math Symbols) table
CMSY_MAP = {
    0x00: "−", 0x01: "⋅", 0x02: "×", 0x03: "∗", 0x04: "÷", 0x05: "⋄", 0x06: "±", 0x07: "∓",
    0x08: "⊕", 0x09: "⊖", 0x0A: "⊗", 0x0B: "⊘", 0x0C: "⊙", 0x0D: "◯", 0x0E: "∘", 0x0F: "∙",
    0x10: "≍", 0x11: "≡", 0x12: "⊆", 0x13: "⊇", 0x14: "≤", 0x15: "≥", 0x16: "≼", 0x17: "≽",
    0x18: "∼", 0x19: "≈", 0x1A: "⊂", 0x1B: "⊃", 0x1C: "≪", 0x1D: "≫", 0x1E: "≺", 0x1F: "≻",
    0x20: "←", 0x21: "→", 0x22: "↑", 0x23: "↓", 0x24: "↔", 0x25: "↗", 0x26: "↘", 0x27: "≃",
    0x28: "⇐", 0x29: "⇒", 0x2A: "⇑", 0x2B: "⇓", 0x2C: "⇔", 0x2D: "↖", 0x2E: "↙", 0x2F: "∝",
    0x30: "′", 0x31: "∞", 0x32: "∈", 0x33: "∋", 0x34: "△", 0x35: "▽", 0x38: "∀", 0x39: "∃",
    0x3A: "¬", 0x3B: "∅", 0x3C: "ℜ", 0x3D: "ℑ", 0x3E: "⊤", 0x3F: "⊥", 0x61: "∪", 0x62: "∩",
    0x63: "⊎", 0x64: "∧", 0x65: "∨", 0x66: "⊢", 0x67: "⊣", 0x68: "⌊", 0x69: "⌋", 0x6A: "⌈",
    0x6B: "⌉", 0x6C: "{", 0x6D: "}", 0x6E: "⟨", 0x6F: "⟩", 0x70: "|", 0x71: "∥", 0x72: "↕",
    0x73: "⇕", 0x74: "∖", 0x75: "≀", 0x76: "√", 0x77: "∐", 0x78: "∇", 0x79: "∫", 0x7A: "⊔",
    0x7B: "⊓", 0x7C: "⊑", 0x7D: "⊒", 0x7E: "§", 0x7F: "†"
}

# TeX CMMI (Computer Modern Math Italic / Greek) table
CMMI_MAP = {
    0x00: "Γ", 0x01: "Δ", 0x02: "Θ", 0x03: "Λ", 0x04: "Ξ", 0x05: "Π", 0x06: "Σ", 0x07: "Υ",
    0x08: "Φ", 0x09: "Ψ", 0x0A: "Ω", 0x0B: "α", 0x0C: "β", 0x0D: "γ", 0x0E: "δ", 0x0F: "ϵ",
    0x10: "ζ", 0x11: "η", 0x12: "θ", 0x13: "ι", 0x14: "κ", 0x15: "λ", 0x16: "μ", 0x17: "ν",
    0x18: "ξ", 0x19: "π", 0x1A: "ρ", 0x1B: "σ", 0x1C: "τ", 0x1D: "υ", 0x1E: "ϕ", 0x1F: "χ",
    0x20: "ψ", 0x21: "ω", 0x22: "ε", 0x23: "ϑ", 0x24: "ϖ", 0x25: "ϱ", 0x26: "ς", 0x27: "φ",
    0x28: "↼", 0x29: "↽", 0x2A: "⇀", 0x2B: "⇁", 0x3A: "♭", 0x3B: "♮", 0x3C: "♯", 0x3D: "⌣",
    0x3E: "⌢", 0x3F: "ℓ"
}

# TeX MSAM / MSBM (AMS Math Symbols / Blackboard) table
MSAM_MSBM_MAP = {
    0x41: "𝔸", 0x42: "𝔹", 0x43: "ℂ", 0x44: "𝔻", 0x45: "𝔼", 0x46: "𝔽", 0x47: "𝔾", 0x48: "ℍ",
    0x49: "𝕀", 0x4A: "𝔁", 0x4B: "𝕂", 0x4C: "𝕃", 0x4D: "𝕄", 0x4E: "ℕ", 0x4F: "𝕆", 0x50: "ℙ",
    0x51: "ℚ", 0x52: "ℝ", 0x53: "𝕊", 0x54: "𝕋", 0x55: "𝕌", 0x56: "𝕍", 0x57: "𝕎", 0x58: "𝕏",
    0x59: "𝕐", 0x5A: "ℤ", 0x02: "⩽", 0x03: "⩾", 0x49: "✓"
}


def is_math_font(font_name: str) -> bool:
    """Check if font name belongs to known math/symbol families."""
    if not font_name:
        return False
    font_lower = font_name.lower()
    return any(k in font_lower for k in MATH_FONT_KEYWORDS)


def is_pua_or_unmapped(char: str) -> bool:
    """Check if a character is within Unicode Private Use Area or replacement char."""
    cp = ord(char)
    return (0xE000 <= cp <= 0xF8FF) or (0xF0000 <= cp <= 0xFFFFD) or (0x100000 <= cp <= 0x10FFFD) or (cp == 0xFFFD)


def remap_glyph(char: str, font_name: str) -> str:
    """Remap a character from known TeX/Symbol fonts to proper Unicode."""
    cp = ord(char)
    font_upper = font_name.upper() if font_name else ""

    if "CMSY" in font_upper and cp in CMSY_MAP:
        return CMSY_MAP[cp]
    if "CMMI" in font_upper and cp in CMMI_MAP:
        return CMMI_MAP[cp]
    if ("MSAM" in font_upper or "MSBM" in font_upper) and cp in MSAM_MSBM_MAP:
        return MSAM_MSBM_MAP[cp]
    if "SYMBOL" in font_upper and cp in ADOBE_SYMBOL_MAP:
        return ADOBE_SYMBOL_MAP[cp]

    # If it's a PUA character encoded in the 0xF000-0xF0FF range (common PDF embedding offset)
    if 0xF000 <= cp <= 0xF0FF:
        base_code = cp - 0xF000
        if "SYMBOL" in font_upper and base_code in ADOBE_SYMBOL_MAP:
            return ADOBE_SYMBOL_MAP[base_code]
        if "CMSY" in font_upper and base_code in CMSY_MAP:
            return CMSY_MAP[base_code]
        if "CMMI" in font_upper and base_code in CMMI_MAP:
            return CMMI_MAP[base_code]
        if ("MSAM" in font_upper or "MSBM" in font_upper) and base_code in MSAM_MSBM_MAP:
            return MSAM_MSBM_MAP[base_code]

    return char


def normalize_unicode(text: str) -> str:
    """Normalize text using NFKC to resolve ligatures, compatibility glyphs, etc."""
    if not text:
        return ""
    return unicodedata.normalize("NFKC", text)


# =====================================================================
# PDF Text & Equation Extraction Engine
# =====================================================================

class PaperExtractor:
    """
    Main extractor class that processes academic PDFs with encoding safety,
    font-aware math handling, equation extraction, and fallbacks.
    """

    def __init__(self,
                 model_choice: str = "auto",
                 dpi: int = 300,
                 min_text_length: int = 50):
        self.model_choice = model_choice
        self.dpi = dpi
        self.min_text_length = min_text_length

        self.nougat_model = None
        self.pix2tex_model = None

        self._init_models()

    def _init_models(self):
        """Initialize Nougat or Pix2Tex ML models if requested and available."""
        if self.model_choice in ("auto", "nougat") and HAS_NOUGAT:
            try:
                logger.info("Initializing Nougat OCR model...")
                checkpoint = get_checkpoint()
                self.nougat_model = NougatModel.from_pretrained(checkpoint)
                device = "cuda" if torch.cuda.is_available() else "cpu"
                self.nougat_model.to(device)
                self.nougat_model.eval()
                logger.info(f"Nougat OCR initialized successfully on {device}.")
            except Exception as e:
                logger.warning(f"Could not initialize Nougat model: {e}. Falling back.")
                self.nougat_model = None

        if self.model_choice in ("auto", "pix2tex") and HAS_PIX2TEX and not self.nougat_model:
            try:
                logger.info("Initializing pix2tex (LaTeX-OCR)...")
                self.pix2tex_model = LatexOCR()
                logger.info("pix2tex initialized successfully.")
            except Exception as e:
                logger.warning(f"Could not initialize pix2tex: {e}. Falling back.")
                self.pix2tex_model = None

    def extract_paper(self, pdf_path: Path) -> Dict[str, Any]:
        """
        Process a single academic PDF paper and return structured output.
        """
        source_name = pdf_path.name
        warnings = []
        had_encoding_issue = False

        result = {
            "source_file": source_name,
            "num_pages": 0,
            "full_text": "",
            "equations": [],
            "warnings": warnings,
            "_had_encoding_issue": False
        }

        # Step 1: Open PDF with PyMuPDF
        try:
            doc = fitz.open(str(pdf_path))
        except Exception as e:
            msg = f"Failed to open PDF '{source_name}': {e}"
            logger.error(msg)
            warnings.append(msg)
            return result

        num_pages = len(doc)
        result["num_pages"] = num_pages

        pages_full_text = []
        extracted_equations = []

        # Step 2: Iterate over pages
        for page_idx in range(num_pages):
            page_num = page_idx + 1
            page = doc[page_idx]

            # Primary text extraction: PyMuPDF get_text('text')
            raw_page_text = page.get_text("text")

            # Font-aware detailed dictionary scan
            page_dict = page.get_text("dict")
            remapped_spans_text, page_equations, pua_found = self._process_page_dict(
                page, page_dict, page_num
            )

            if pua_found:
                had_encoding_issue = True

            # Check if page is anomalously short (possible scanned or image page)
            final_page_text = raw_page_text.strip()
            if len(final_page_text) < self.min_text_length:
                # Try fallback 1: pdfplumber
                plumber_text = self._try_pdfplumber_fallback(pdf_path, page_idx)
                if plumber_text and len(plumber_text.strip()) >= self.min_text_length:
                    final_page_text = plumber_text.strip()
                    warnings.append(f"Page {page_num}: PyMuPDF had short text; used pdfplumber fallback.")
                else:
                    # Try fallback 2: pytesseract OCR on rendered page image
                    ocr_text = self._try_ocr_fallback(page, page_num)
                    if ocr_text and len(ocr_text.strip()) > 0:
                        final_page_text = ocr_text.strip()
                        warnings.append(f"Page {page_num}: Scanned/empty page detected; used pytesseract OCR fallback.")
                    else:
                        warnings.append(f"Page {page_num}: Anomalously short or empty text ({len(final_page_text)} chars).")

            # Incorporate remapped math characters and normalize NFKC
            if remapped_spans_text and len(remapped_spans_text) > len(final_page_text) * 0.5:
                # Use remapped text if it provides richer font-mapped glyphs
                combined_text = remapped_spans_text
            else:
                combined_text = final_page_text

            norm_text = normalize_unicode(combined_text)
            pages_full_text.append(norm_text)
            extracted_equations.extend(page_equations)

        doc.close()

        # Step 3: Run ML equation extraction if enabled (Nougat or pix2tex)
        if self.nougat_model:
            extracted_equations = self._run_nougat_extraction(pdf_path, extracted_equations, warnings)
        elif self.pix2tex_model:
            extracted_equations = self._run_pix2tex_extraction(pdf_path, extracted_equations, warnings)

        # Assemble full document text
        full_text = "\n\n--- Page Break ---\n\n".join(pages_full_text)
        result["full_text"] = full_text
        result["equations"] = extracted_equations
        result["_had_encoding_issue"] = had_encoding_issue

        return result

    def _process_page_dict(self, page: fitz.Page, page_dict: dict, page_num: int) -> Tuple[str, List[Dict[str, Any]], bool]:
        """
        Scan page dictionary blocks, detect math font families and PUA glyphs,
        remap characters, and extract potential equation blocks/spans.
        """
        page_lines_text = []
        page_equations = []
        pua_found = False

        blocks = page_dict.get("blocks", [])
        for block in blocks:
            if "lines" not in block:
                continue

            block_text_parts = []
            block_has_math = False
            math_spans_in_block = []

            for line in block.get("lines", []):
                line_text_parts = []
                for span in line.get("spans", []):
                    span_font = span.get("font", "")
                    raw_span_text = span.get("text", "")
                    bbox = span.get("bbox", [0, 0, 0, 0])

                    is_math = is_math_font(span_font)
                    remapped_chars = []

                    for ch in raw_span_text:
                        if is_pua_or_unmapped(ch):
                            pua_found = True
                        mapped_ch = remap_glyph(ch, span_font)
                        remapped_chars.append(mapped_ch)

                    remapped_span_text = "".join(remapped_chars)

                    # Check for math symbols in text or font
                    if is_math or any(ord(c) in range(0x2200, 0x22FF) or 0x0370 <= ord(c) <= 0x03FF for c in remapped_span_text):
                        block_has_math = True
                        math_spans_in_block.append({
                            "text": remapped_span_text,
                            "bbox": bbox,
                            "font": span_font
                        })

                    line_text_parts.append(remapped_span_text)

                line_full = "".join(line_text_parts)
                block_text_parts.append(line_full)

            block_full_text = " ".join(block_text_parts).strip()
            block_full_norm = normalize_unicode(block_full_text)
            page_lines_text.append(block_full_norm)

            # Detect if this block looks like a standalone equation or contains notable math
            if block_has_math and block_full_text:
                # Flag equation
                flagged_str = f"[POSSIBLE_EQUATION: {block_full_norm}]"
                page_equations.append({
                    "page": page_num,
                    "raw_extracted": block_full_norm,
                    "latex": None,
                    "extraction_method": "raw_unicode_flagged",
                    "bbox": block.get("bbox", None)
                })

        full_page_text = "\n".join(page_lines_text)
        return full_page_text, page_equations, pua_found

    def _try_pdfplumber_fallback(self, pdf_path: Path, page_idx: int) -> Optional[str]:
        """Attempt text extraction with pdfplumber for a specific page."""
        if not HAS_PDFPLUMBER:
            return None
        try:
            with pdfplumber.open(str(pdf_path)) as pdf:
                if page_idx < len(pdf.pages):
                    return pdf.pages[page_idx].extract_text()
        except Exception as e:
            logger.debug(f"pdfplumber fallback failed on page {page_idx+1}: {e}")
        return None

    def _try_ocr_fallback(self, page: fitz.Page, page_num: int) -> Optional[str]:
        """Render page image and perform pytesseract OCR fallback."""
        if not HAS_PYTESSERACT or not HAS_PIL:
            return None
        try:
            # Render page at 300 DPI (zoom 300/72 ≈ 4.166)
            zoom = self.dpi / 72.0
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            ocr_text = pytesseract.image_to_string(img)
            return ocr_text
        except Exception as e:
            logger.debug(f"pytesseract OCR fallback failed on page {page_num}: {e}")
            return None

    def _run_nougat_extraction(self, pdf_path: Path, existing_equations: List[Dict[str, Any]], warnings: List[str]) -> List[Dict[str, Any]]:
        """Run Nougat OCR to extract LaTeX equations from the document."""
        if not self.nougat_model:
            return existing_equations

        logger.info(f"Running Nougat model on {pdf_path.name}...")
        nougat_equations = []
        try:
            # Rasterize PDF pages
            images = rasterize_paper(str(pdf_path))
            for pno, img in enumerate(images):
                page_num = pno + 1
                # Run inference
                prediction = self.nougat_model.inference(img)
                # Find LaTeX equations $...$ and $$...$$
                inline_eqs = re.findall(r'\$(.*?)\$', prediction)
                block_eqs = re.findall(r'\$\$(.*?)\$\$', prediction, re.DOTALL)

                for eq in block_eqs:
                    eq_str = eq.strip()
                    if eq_str:
                        nougat_equations.append({
                            "page": page_num,
                            "raw_extracted": eq_str,
                            "latex": f"$${eq_str}$$",
                            "extraction_method": "nougat"
                        })
                for eq in inline_eqs:
                    eq_str = eq.strip()
                    if eq_str and eq_str not in [b.strip() for b in block_eqs]:
                        nougat_equations.append({
                            "page": page_num,
                            "raw_extracted": eq_str,
                            "latex": f"${eq_str}$",
                            "extraction_method": "nougat"
                        })
            if nougat_equations:
                return nougat_equations
        except Exception as e:
            msg = f"Nougat inference failed: {e}. Kept raw extracted equations."
            logger.warning(msg)
            warnings.append(msg)

        return existing_equations

    def _run_pix2tex_extraction(self, pdf_path: Path, existing_equations: List[Dict[str, Any]], warnings: List[str]) -> List[Dict[str, Any]]:
        """Run pix2tex (LaTeX-OCR) on cropped bounding boxes of equations."""
        if not self.pix2tex_model:
            return existing_equations

        doc = fitz.open(str(pdf_path))
        for eq in existing_equations:
            page_num = eq.get("page", 1)
            bbox = eq.get("bbox")
            if not bbox or page_num > len(doc):
                continue
            try:
                page = doc[page_num - 1]
                rect = fitz.Rect(bbox)
                zoom = self.dpi / 72.0
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat, clip=rect)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                # Predict LaTeX string
                latex_pred = self.pix2tex_model(img)
                if latex_pred:
                    eq["latex"] = latex_pred
                    eq["extraction_method"] = "pix2tex"
            except Exception as e:
                logger.debug(f"pix2tex error on page {page_num}: {e}")

        doc.close()
        return existing_equations


# =====================================================================
# Safe File IO & Batch Processing
# =====================================================================

def safe_write_json(filepath: Path, data: dict):
    """Write data as UTF-8 JSON safely with Unicode fallback."""
    # Remove internal temporary fields
    data_to_write = {k: v for k, v in data.items() if not k.startswith("_")}

    # Strip bboxes from equations if they exist
    if "equations" in data_to_write:
        clean_eqs = []
        for eq in data_to_write["equations"]:
            clean_eq = {
                "page": eq.get("page", 1),
                "raw_extracted": eq.get("raw_extracted", ""),
                "latex": eq.get("latex", None),
                "extraction_method": eq.get("extraction_method", "raw_unicode_flagged")
            }
            clean_eqs.append(clean_eq)
        data_to_write["equations"] = clean_eqs

    json_str = json.dumps(data_to_write, ensure_ascii=False, indent=2)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(json_str)
    except UnicodeEncodeError:
        with open(filepath, "w", encoding="utf-8", errors="backslashreplace") as f:
            f.write(json_str)


def write_summary_csv(csv_path: Path, rows: List[Dict[str, Any]]):
    """Write summary CSV file with UTF-8 encoding."""
    fieldnames = ["filename", "num_pages", "num_equations_found", "had_encoding_issues"]
    try:
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in rows:
                writer.writerow({
                    "filename": r["filename"],
                    "num_pages": r["num_pages"],
                    "num_equations_found": r["num_equations_found"],
                    "had_encoding_issues": r["had_encoding_issues"]
                })
    except UnicodeEncodeError:
        with open(csv_path, "w", encoding="utf-8", errors="backslashreplace", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in rows:
                writer.writerow({
                    "filename": r["filename"],
                    "num_pages": r["num_pages"],
                    "num_equations_found": r["num_equations_found"],
                    "had_encoding_issues": r["had_encoding_issues"]
                })


def batch_extract(input_dir: Path,
                  output_dir: Path,
                  model_choice: str = "auto",
                  dpi: int = 300,
                  force: bool = False,
                  limit: Optional[int] = None):
    """
    Main batch extraction workflow.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_csv_path = output_dir / "_all_papers_summary.csv"

    # Find all PDFs
    pdf_files = sorted(list(input_dir.glob("*.pdf")))
    if not pdf_files:
        # Check subdirectories as well if none found in root
        pdf_files = sorted(list(input_dir.glob("**/*.pdf")))

    if not pdf_files:
        logger.error(f"No PDF files found in '{input_dir}'.")
        return

    if limit and limit > 0:
        pdf_files = pdf_files[:limit]

    logger.info(f"Found {len(pdf_files)} PDF papers to process.")
    logger.info(f"Input directory:  {input_dir.resolve()}")
    logger.info(f"Output directory: {output_dir.resolve()}")

    extractor = PaperExtractor(model_choice=model_choice, dpi=dpi)
    summary_rows = []

    # Read existing summary rows if resuming
    existing_summaries = {}
    if summary_csv_path.exists() and not force:
        try:
            with open(summary_csv_path, "r", encoding="utf-8", errors="replace") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    existing_summaries[r["filename"]] = r
        except Exception:
            pass

    for pdf_path in tqdm(pdf_files, desc="Extracting papers", unit="paper"):
        pdf_stem = pdf_path.stem
        out_json_path = output_dir / f"{pdf_stem}.json"

        # Resumable check
        if out_json_path.exists() and not force:
            logger.info(f"Skipping already extracted file: {pdf_path.name}")
            if pdf_path.name in existing_summaries:
                summary_rows.append(existing_summaries[pdf_path.name])
            else:
                # Read from existing JSON
                try:
                    with open(out_json_path, "r", encoding="utf-8", errors="replace") as f:
                        data = json.load(f)
                        summary_rows.append({
                            "filename": pdf_path.name,
                            "num_pages": data.get("num_pages", 0),
                            "num_equations_found": len(data.get("equations", [])),
                            "had_encoding_issues": False
                        })
                except Exception:
                    pass
            continue

        logger.info(f"Processing: {pdf_path.name}")
        try:
            result = extractor.extract_paper(pdf_path)
            safe_write_json(out_json_path, result)

            summary_rows.append({
                "filename": pdf_path.name,
                "num_pages": result["num_pages"],
                "num_equations_found": len(result["equations"]),
                "had_encoding_issues": result.get("_had_encoding_issue", False)
            })

            # Update summary CSV iteratively for safety
            write_summary_csv(summary_csv_path, summary_rows)

        except Exception as e:
            logger.error(f"Unexpected error processing '{pdf_path.name}': {e}", exc_info=True)
            summary_rows.append({
                "filename": pdf_path.name,
                "num_pages": 0,
                "num_equations_found": 0,
                "had_encoding_issues": True
            })
            write_summary_csv(summary_csv_path, summary_rows)

    logger.info(f"\nProcessing complete! Summary written to: {summary_csv_path.resolve()}")
    logger.info(f"Extracted JSON files saved in: {output_dir.resolve()}")


# =====================================================================
# CLI Entry Point
# =====================================================================

def parse_args():
    parser = argparse.ArgumentParser(
        description="Batch extract full text and equations from academic PDFs with Unicode/math preservation."
    )
    # Default input dir checks ./papers first, then current dir .
    default_input = "./papers" if Path("./papers").is_dir() else "."
    parser.add_argument(
        "-i", "--input-dir",
        type=Path,
        default=Path(default_input),
        help=f"Path to directory containing input PDF files (default: {default_input})"
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=Path,
        default=Path("./extracted"),
        help="Path to directory where extracted JSONs and summary CSV will be saved (default: ./extracted)"
    )
    parser.add_argument(
        "--model",
        choices=["auto", "nougat", "pix2tex", "raw"],
        default="auto",
        help="Equation extraction model choice: 'auto' (tries nougat/pix2tex then raw fallback), 'nougat', 'pix2tex', or 'raw' (default: auto)"
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="DPI for rendering page images during OCR/ML extraction (default: 300)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force reprocessing of PDFs that already have output JSON files (default: False)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of PDFs to process (useful for quick testing)"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    batch_extract(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        model_choice=args.model,
        dpi=args.dpi,
        force=args.force,
        limit=args.limit
    )


if __name__ == "__main__":
    main()
