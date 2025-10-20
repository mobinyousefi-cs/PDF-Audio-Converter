#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: PDF Audio Converter 
File: pdf_utils.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-20 
Updated: 2025-10-20 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Utilities for extracting text from PDFs and writing text into a new PDF.

Usage: 
from .pdf_utils import extract_text_from_pdf, write_text_to_pdf

Notes: 
- Uses PyPDF2 for extraction and ReportLab for writing.

===================================================================
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def extract_text_from_pdf(path: str | Path, page_range: tuple[int | None, int | None] = (None, None)) -> str:
    """Extract text from a PDF.

    Args:
        path: Path to the PDF file.
        page_range: (start, end) 1-based inclusive range; None for full.

    Returns:
        Extracted text (may be empty when PDF is purely scanned images).
    """
    p = Path(path)
    reader = PdfReader(str(p))
    n = len(reader.pages)

    start, end = page_range
    if start is None:
        start = 1
    if end is None or end > n:
        end = n
    if start < 1 or start > end:
        raise ValueError("Invalid page range")

    texts: list[str] = []
    for i in range(start - 1, end):
        page = reader.pages[i]
        try:
            txt = page.extract_text() or ""
        except Exception:
            txt = ""
        texts.append(txt)
    return "\n".join(texts).strip()


def write_text_to_pdf(text: str, out_path: str | Path, *, title: str = "Transcription") -> Path:
    """Create a simple PDF with the given text content using ReportLab."""
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    c = canvas.Canvas(str(out), pagesize=A4)
    width, height = A4

    # Simple word-wrapping
    margin = 50
    y = height - margin
    line_height = 14
    c.setTitle(title)
    c.setFont("Times-Roman", 12)

    for line in _wrap_text(text.splitlines() or [""], max_width=width - 2 * margin):
        if y < margin:
            c.showPage()
            c.setFont("Times-Roman", 12)
            y = height - margin
        c.drawString(margin, y, line)
        y -= line_height

    c.save()
    return out


def _wrap_text(lines: Iterable[str], max_width: float, char_width: float = 6.0) -> Iterable[str]:
    """A very naive wrapper based on average char width."""
    max_chars = max(int(max_width // char_width), 1)
    for line in lines:
        while len(line) > max_chars:
            yield line[:max_chars]
            line = line[max_chars:]
        yield line
