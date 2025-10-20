#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: PDF Audio Converter 
File: config.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-20 
Updated: 2025-10-20 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Centralized configuration defaults for TTS/STT and PDF ops.

Usage: 
from .config import Defaults

Notes: 
- Modify defaults here to affect GUI and CLI.

===================================================================
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Defaults:
    tts_rate: int = 180
    tts_volume: float = 0.9
    tts_voice: str | None = None  # None = system default

    # STT
    language: str = "en-US"
    phrase_time_limit: int | None = None  # seconds

    # PDF
    pdf_page_range: tuple[int | None, int | None] = (None, None)  # start, end (1-based)

