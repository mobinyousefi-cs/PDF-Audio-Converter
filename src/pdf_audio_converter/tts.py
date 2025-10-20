#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: PDF Audio Converter 
File: tts.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-20 
Updated: 2025-10-20 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Text-to-speech utilities built on pyttsx3.

Usage: 
from .tts import text_to_speech

Notes: 
- Offline and cross-platform (SAPI5, NSSpeechSynthesizer, eSpeak).

===================================================================
"""
from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Optional, Iterable

import pyttsx3

from .logger import get_logger

logger = get_logger()


@dataclass
class TTSConfig:
    rate: int = 180
    volume: float = 0.9
    voice: Optional[str] = None  # voice id substring to match


class TTSEngine:
    def __init__(self, cfg: TTSConfig) -> None:
        self.cfg = cfg
        self.engine = pyttsx3.init()
        self._configure()
        self._thread: Optional[threading.Thread] = None

    def _configure(self) -> None:
        self.engine.setProperty("rate", self.cfg.rate)
        self.engine.setProperty("volume", self.cfg.volume)
        if self.cfg.voice:
            for v in self.engine.getProperty("voices"):
                if self.cfg.voice.lower() in (v.name or "").lower():
                    self.engine.setProperty("voice", v.id)
                    break

    def speak(self, chunks: Iterable[str]) -> None:
        """Speak an iterable of text chunks synchronously."""
        for chunk in chunks:
            if not chunk:
                continue
            self.engine.say(chunk)
        self.engine.runAndWait()

    def speak_async(self, chunks: Iterable[str]) -> None:
        self.stop()
        self._thread = threading.Thread(target=self.speak, args=(list(chunks),), daemon=True)
        self._thread.start()

    def stop(self) -> None:
        try:
            self.engine.stop()
        except Exception:
            pass


def text_to_speech(text: str, *, rate: int = 180, volume: float = 0.9, voice: Optional[str] = None,
                   chunk_size: int = 1800, async_play: bool = False) -> TTSEngine:
    """Speak the given text using pyttsx3.

    Args:
        text: Content to speak.
        rate: Words per minute (approx).
        volume: 0.0–1.0.
        voice: Optional voice name substring to select.
        chunk_size: Split text into manageable chunks.
        async_play: If True, returns immediately while playing.
    """
    cfg = TTSConfig(rate=rate, volume=volume, voice=voice)
    engine = TTSEngine(cfg)

    def chunks() -> Iterable[str]:
        s = text.strip()
        for i in range(0, len(s), chunk_size):
            yield s[i : i + chunk_size]

    if async_play:
        engine.speak_async(chunks())
    else:
        engine.speak(chunks())
    return engine
