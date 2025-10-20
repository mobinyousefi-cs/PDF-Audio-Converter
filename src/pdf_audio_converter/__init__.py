#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: PDF Audio Converter 
File: __init__.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-20 
Updated: 2025-10-20 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Package initializer exposing top-level functions and metadata.

Usage: 
from pdf_audio_converter import text_to_speech, speech_to_text

Notes: 
- Keep imports lightweight to avoid GUI/CLI startup latency.

===================================================================
"""

from .tts import text_to_speech
from .stt import speech_to_text, transcribe_audio_file
from .pdf_utils import extract_text_from_pdf, write_text_to_pdf

__all__ = [
    "text_to_speech",
    "speech_to_text",
    "transcribe_audio_file",
    "extract_text_from_pdf",
    "write_text_to_pdf",
]

__version__ = "0.1.0"
