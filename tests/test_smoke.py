#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: PDF Audio Converter 
File: test_smoke.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-20 
Updated: 2025-10-20 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Basic smoke tests for importability and simple pure-Python helpers.

Usage: 
pytest -q

Notes: 
- STT/TTS and GUI are not exercised in CI (require system deps).

===================================================================
"""
from pdf_audio_converter import __version__
from pdf_audio_converter.pdf_utils import _wrap_text


def test_version() -> None:
    assert isinstance(__version__, str)


def test_wrap_text() -> None:
    lines = list(_wrap_text(["abcdefghij"], max_width=30, char_width=6))
    assert lines  # not empty
