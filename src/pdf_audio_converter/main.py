#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: PDF Audio Converter 
File: main.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-20 
Updated: 2025-10-20 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
CLI entry point for PDF→Audio (TTS) and Audio→PDF (STT) workflows.

Usage: 
pdf-audio tts --pdf input.pdf --rate 180 --volume 0.9
pdf-audio stt --audio sample.wav --out out.pdf --txt out.txt

Notes: 
- See README for details. This file registers the console_script 'pdf-audio'.

===================================================================
"""
from __future__ import annotations

import argparse
from pathlib import Path

from .config import Defaults
from .logger import get_logger
from .pdf_utils import extract_text_from_pdf, write_text_to_pdf
from .tts import text_to_speech
from .stt import transcribe_audio_file, speech_to_text

logger = get_logger()


def _cmd_tts(args: argparse.Namespace) -> int:
    txt = extract_text_from_pdf(args.pdf, page_range=(args.start, args.end))
    if not txt:
        logger.warning("No text extracted. Are you using a scanned PDF?")
    text_to_speech(
        txt,
        rate=args.rate or Defaults.tts_rate,
        volume=args.volume or Defaults.tts_volume,
        voice=args.voice,
        async_play=False,
    )
    return 0


def _cmd_stt(args: argparse.Namespace) -> int:
    if args.mic:
        text = speech_to_text(language=args.lang or Defaults.language, 
                              phrase_time_limit=args.limit or Defaults.phrase_time_limit)
    else:
        text = transcribe_audio_file(args.audio, language=args.lang or Defaults.language)

    if not text:
        logger.warning("Nothing transcribed.")

    if args.out:
        write_text_to_pdf(text, args.out, title="Transcription")
        logger.info("Saved PDF → %s", Path(args.out).resolve())
    if args.txt:
        Path(args.txt).write_text(text, encoding="utf-8")
        logger.info("Saved TXT → %s", Path(args.txt).resolve())

    # Optionally speak back the transcription
    if args.speak_back:
        text_to_speech(text, rate=args.rate or Defaults.tts_rate, volume=args.volume or Defaults.tts_volume)

    return 0


def app(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="pdf-audio", description="PDF ↔ Audio Converter")

    sub = p.add_subparsers(dest="cmd", required=True)

    tts = sub.add_parser("tts", help="Read a PDF aloud (TTS)")
    tts.add_argument("--pdf", required=True, help="Input PDF path")
    tts.add_argument("--start", type=int, default=None, help="Start page (1-based)")
    tts.add_argument("--end", type=int, default=None, help="End page (1-based, inclusive)")
    tts.add_argument("--rate", type=int, default=Defaults.tts_rate)
    tts.add_argument("--volume", type=float, default=Defaults.tts_volume)
    tts.add_argument("--voice", default=None, help="Voice name contains (e.g., 'Zira')")
    tts.set_defaults(func=_cmd_tts)

    stt = sub.add_parser("stt", help="Transcribe audio and export to PDF/TXT")
    gsrc = stt.add_mutually_exclusive_group(required=True)
    gsrc.add_argument("--audio", help="Audio file path (wav/aiff/flac)")
    gsrc.add_argument("--mic", action="store_true", help="Record from default microphone")
    stt.add_argument("--lang", default=Defaults.language, help="Language code (e.g., en-US, fa-IR)")
    stt.add_argument("--limit", type=int, default=None, help="Max seconds to listen (mic mode)")
    stt.add_argument("--out", help="Output PDF path")
    stt.add_argument("--txt", help="Optional TXT save path")
    stt.add_argument("--speak-back", action="store_true", help="Speak back the transcription")
    stt.add_argument("--rate", type=int, default=Defaults.tts_rate)
    stt.add_argument("--volume", type=float, default=Defaults.tts_volume)
    stt.set_defaults(func=_cmd_stt)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(app())
