#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: PDF Audio Converter 
File: stt.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-20 
Updated: 2025-10-20 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Speech-to-text utilities using the SpeechRecognition package.

Usage: 
from .stt import speech_to_text, transcribe_audio_file

Notes: 
- Defaults to Google Web Speech API (requires internet). Swap recognizer as needed.
- Microphone capture requires PyAudio (or alternative backends).

===================================================================
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import speech_recognition as sr

from .logger import get_logger

logger = get_logger()


def _recognize(recognizer: sr.Recognizer, audio: sr.AudioData, language: str) -> str:
    try:
        return recognizer.recognize_google(audio, language=language)
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        logger.error("STT API error: %s", e)
        return ""


def transcribe_audio_file(path: str | Path, *, language: str = "en-US") -> str:
    """Transcribe an audio file to text using SpeechRecognition."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(str(path)) as source:
        audio = recognizer.record(source)
    return _recognize(recognizer, audio, language)


def speech_to_text(*, language: str = "en-US", phrase_time_limit: Optional[int] = None) -> str:
    """Record from default microphone and transcribe to text.

    Args:
        language: BCP-47 code (e.g., 'en-US', 'fa-IR').
        phrase_time_limit: Max seconds to listen; None = no limit.
    """
    recognizer = sr.Recognizer()
    try:
        mic = sr.Microphone()
    except Exception as e:
        logger.error("No microphone available: %s", e)
        return ""

    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, phrase_time_limit=phrase_time_limit)
    return _recognize(recognizer, audio, language)
