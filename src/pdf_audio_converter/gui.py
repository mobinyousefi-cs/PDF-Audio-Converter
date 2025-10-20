#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: PDF Audio Converter 
File: gui.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-20 
Updated: 2025-10-20 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Tkinter GUI for PDF→Audio (TTS) and Audio/Speech→PDF (STT) conversions.

Usage: 
python -m pdf_audio_converter.gui

Notes: 
- Minimal dependencies; avoids blocking the UI by using threads for TTS/STT.

===================================================================
"""
from __future__ import annotations

import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from .config import Defaults
from .logger import get_logger
from .pdf_utils import extract_text_from_pdf, write_text_to_pdf
from .stt import speech_to_text, transcribe_audio_file
from .tts import text_to_speech, TTSEngine

logger = get_logger()


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("PDF ↔ Audio Converter")
        self.geometry("760x520")
        self.minsize(720, 480)
        self._tts_engine: TTSEngine | None = None

        self._build_ui()

    # -------------------- UI --------------------
    def _build_ui(self) -> None:
        nb = ttk.Notebook(self)
        nb.pack(fill=tk.BOTH, expand=True)

        self.tts_frame = ttk.Frame(nb)
        self.stt_frame = ttk.Frame(nb)
        nb.add(self.tts_frame, text="PDF → Audio")
        nb.add(self.stt_frame, text="Audio/Speech → PDF")

        self._build_tts_tab()
        self._build_stt_tab()

    def _build_tts_tab(self) -> None:
        frm = self.tts_frame

        # File selection
        path_var = tk.StringVar()
        self.tts_path_var = path_var

        row = ttk.Frame(frm)
        row.pack(fill=tk.X, padx=12, pady=8)
        ttk.Label(row, text="PDF File:").pack(side=tk.LEFT)
        ttk.Entry(row, textvariable=path_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)
        ttk.Button(row, text="Browse", command=self._choose_pdf).pack(side=tk.LEFT)

        # Page range
        r = ttk.Frame(frm)
        r.pack(fill=tk.X, padx=12)
        ttk.Label(r, text="Page Range (1-based):").pack(side=tk.LEFT)
        self.tts_start = tk.IntVar(value=0)
        self.tts_end = tk.IntVar(value=0)
        ttk.Entry(r, width=6, textvariable=self.tts_start).pack(side=tk.LEFT, padx=6)
        ttk.Label(r, text="to").pack(side=tk.LEFT)
        ttk.Entry(r, width=6, textvariable=self.tts_end).pack(side=tk.LEFT, padx=6)

        # Voice settings
        cfg = ttk.Frame(frm)
        cfg.pack(fill=tk.X, padx=12, pady=6)
        self.rate_var = tk.IntVar(value=Defaults.tts_rate)
        self.volume_var = tk.DoubleVar(value=Defaults.tts_volume)
        self.voice_var = tk.StringVar(value="")

        ttk.Label(cfg, text="Rate:").pack(side=tk.LEFT)
        ttk.Spinbox(cfg, from_=100, to=300, textvariable=self.rate_var, width=6).pack(side=tk.LEFT, padx=6)
        ttk.Label(cfg, text="Volume:").pack(side=tk.LEFT)
        ttk.Spinbox(cfg, from_=0.0, to=1.0, increment=0.1, textvariable=self.volume_var, width=6).pack(side=tk.LEFT, padx=6)
        ttk.Label(cfg, text="Voice contains:").pack(side=tk.LEFT)
        ttk.Entry(cfg, textvariable=self.voice_var, width=16).pack(side=tk.LEFT, padx=6)

        # Controls
        btns = ttk.Frame(frm)
        btns.pack(fill=tk.X, padx=12, pady=8)
        ttk.Button(btns, text="Read PDF", command=self._start_tts).pack(side=tk.LEFT)
        ttk.Button(btns, text="Stop", command=self._stop_tts).pack(side=tk.LEFT, padx=8)

        # Log box
        self.tts_log = tk.Text(frm, height=14)
        self.tts_log.pack(fill=tk.BOTH, expand=True, padx=12, pady=6)

    def _build_stt_tab(self) -> None:
        frm = self.stt_frame

        # Source selection
        src = ttk.Frame(frm)
        src.pack(fill=tk.X, padx=12, pady=8)
        self.audio_path_var = tk.StringVar()
        ttk.Label(src, text="Audio File (optional):").pack(side=tk.LEFT)
        ttk.Entry(src, textvariable=self.audio_path_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)
        ttk.Button(src, text="Browse", command=self._choose_audio).pack(side=tk.LEFT)

        # Language & limit
        cfg = ttk.Frame(frm)
        cfg.pack(fill=tk.X, padx=12)
        self.lang_var = tk.StringVar(value=Defaults.language)
        self.limit_var = tk.IntVar(value=0)
        ttk.Label(cfg, text="Language:").pack(side=tk.LEFT)
        ttk.Entry(cfg, textvariable=self.lang_var, width=10).pack(side=tk.LEFT, padx=6)
        ttk.Label(cfg, text="Time limit (s, mic):").pack(side=tk.LEFT)
        ttk.Entry(cfg, textvariable=self.limit_var, width=8).pack(side=tk.LEFT, padx=6)

        # Controls
        btns = ttk.Frame(frm)
        btns.pack(fill=tk.X, padx=12, pady=8)
        ttk.Button(btns, text="Transcribe File", command=self._transcribe_file).pack(side=tk.LEFT)
        ttk.Button(btns, text="Listen (Mic)", command=self._listen_mic).pack(side=tk.LEFT, padx=8)
        ttk.Button(btns, text="Export to PDF", command=self._export_pdf).pack(side=tk.LEFT)
        ttk.Button(btns, text="Save TXT", command=self._export_txt).pack(side=tk.LEFT, padx=8)

        # Text area
        self.stt_text = tk.Text(frm, height=16)
        self.stt_text.pack(fill=tk.BOTH, expand=True, padx=12, pady=6)

    # -------------------- actions --------------------
    def _choose_pdf(self) -> None:
        path = filedialog.askopenfilename(filetypes=[["PDF files", "*.pdf"]])
        if path:
            self.tts_path_var.set(path)

    def _choose_audio(self) -> None:
        path = filedialog.askopenfilename(filetypes=[["Audio", "*.wav *.aiff *.flac *.mp3"], ["All", "*.*"]])
        if path:
            self.audio_path_var.set(path)

    def _start_tts(self) -> None:
        path = self.tts_path_var.get().strip()
        if not path:
            messagebox.showwarning("Missing file", "Please choose a PDF file.")
            return
        try:
            start = self.tts_start.get() or None
            end = self.tts_end.get() or None
            text = extract_text_from_pdf(path, page_range=(start, end))
            if not text:
                self._log(self.tts_log, "No text found; PDF might be scanned.")
            self._tts_engine = text_to_speech(
                text,
                rate=self.rate_var.get(),
                volume=float(self.volume_var.get()),
                voice=self.voice_var.get().strip() or None,
                async_play=True,
            )
            self._log(self.tts_log, f"Reading: {Path(path).name}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _stop_tts(self) -> None:
        if self._tts_engine:
            self._tts_engine.stop()
            self._log(self.tts_log, "Stopped.")

    def _transcribe_file(self) -> None:
        path = self.audio_path_var.get().strip()
        if not path:
            messagebox.showwarning("Missing file", "Choose an audio file or use Listen (Mic).")
            return

        def run():
            try:
                text = transcribe_audio_file(path, language=self.lang_var.get().strip())
                self._set_text(self.stt_text, text)
            except Exception as e:
                messagebox.showerror("Transcription failed", str(e))

        threading.Thread(target=run, daemon=True).start()

    def _listen_mic(self) -> None:
        limit = self.limit_var.get() or None

        def run():
            try:
                text = speech_to_text(language=self.lang_var.get().strip(), phrase_time_limit=limit)
                self._set_text(self.stt_text, text)
            except Exception as e:
                messagebox.showerror("Microphone error", str(e))

        threading.Thread(target=run, daemon=True).start()

    def _export_pdf(self) -> None:
        text = self.stt_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("No text", "There is nothing to export.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[["PDF", "*.pdf"]])
        if path:
            write_text_to_pdf(text, path)
            self._log(self.tts_log, f"Saved PDF → {path}")

    def _export_txt(self) -> None:
        text = self.stt_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("No text", "There is nothing to save.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[["Text", "*.txt"]])
        if path:
            Path(path).write_text(text, encoding="utf-8")
            self._log(self.tts_log, f"Saved TXT → {path}")

    # -------------------- helpers --------------------
    @staticmethod
    def _log(widget: tk.Text, msg: str) -> None:
        widget.insert(tk.END, msg + "\n")
        widget.see(tk.END)

    @staticmethod
    def _set_text(widget: tk.Text, text: str) -> None:
        widget.delete("1.0", tk.END)
        widget.insert("1.0", text)


def main() -> None:  # pragma: no cover
    app = App()
    app.mainloop()


if __name__ == "__main__":  # pragma: no cover
    main()
