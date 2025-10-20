# PDF ↔ Audio Converter (Tkinter GUI + CLI)

Convert **PDF → Audiobook (TTS)** and **Audio/Speech → PDF (STT)** with a clean Python project structure. Includes a Tkinter GUI and a CLI, cross‑platform text‑to‑speech (pyttsx3), speech recognition (SpeechRecognition), PDF text extraction (PyPDF2), and PDF writing (ReportLab).

---

## ✨ Features
- **PDF → Audio (TTS):** Extracts text from PDFs and reads aloud with adjustable rate/voice/volume.
- **Audio → Text → PDF (STT):** Record from microphone *or* transcribe an audio file; export as PDF/TXT.
- **GUI (Tkinter):** Simple, responsive interface with progress, controls, and status logs.
- **CLI:** Scriptable workflows for batch conversion and automation.
- **Robustness:** Graceful fallbacks, error messages, and logging to console/file.

---

## 🗂 Project Structure
```
pdf-audio-converter/
├─ src/
│  └─ pdf_audio_converter/
│     ├─ __init__.py
│     ├─ main.py              # CLI entry points
│     ├─ gui.py               # Tkinter application
│     ├─ tts.py               # Text-to-speech services (pyttsx3)
│     ├─ stt.py               # Speech-to-text services (SpeechRecognition)
│     ├─ pdf_utils.py         # PDF read/write helpers
│     ├─ logger.py            # Logging configuration
│     └─ config.py            # Centralized defaults
├─ tests/
│  └─ test_smoke.py
├─ .github/
│  └─ workflows/
│     └─ ci.yml               # Ruff + Black + Pytest CI
├─ README.md
├─ pyproject.toml             # PEP 621 + Ruff/Black config
├─ .editorconfig
├─ .gitignore
└─ LICENSE (MIT)
```

---

## 🔧 Installation
> Python **3.10+** recommended.

```bash
# clone your repo, then:
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -U pip
pip install -e .
```

**System notes**
- **TTS (pyttsx3):** Works offline on Windows (SAPI5), macOS (NSSpeechSynthesizer), Linux (eSpeak).
- **STT (SpeechRecognition):** By default uses Google Web Speech API (internet). You can plug in other engines.
- **Recording:** `pyaudio` (or `sounddevice`) may need system dependencies.

---

## ▶️ Usage
### GUI
```bash
python -m pdf_audio_converter.gui
```

### CLI
```bash
# PDF → Audio (speaks immediately)
pdf-audio tts --pdf input.pdf --rate 180 --volume 0.9

# Audio file → Text → PDF
pdf-audio stt --audio sample.wav --out out.pdf

# Record from microphone, then export PDF/TXT
pdf-audio stt --mic --out notes.pdf --txt notes.txt
```

> The console/GUI will show errors if microphones, drivers, or engines are unavailable.

---

## 🛠 Dependencies
Managed in `pyproject.toml`:
- `pyttsx3` – offline TTS
- `SpeechRecognition` – STT wrapper
- `PyPDF2` – extract text
- `reportlab` – write PDF
- `pyaudio` – microphone input (optional, platform dependent)
- `tkinter` – standard GUI (bundled with most Python installs)

Dev:
- `pytest`, `ruff`, `black`

---

## 🧪 Testing
```bash
pytest -q
```

---

## 📄 License
MIT — see `LICENSE`.

---

## 🙌 Credits
Author: **Mobin Yousefi** (GitHub: `github.com/mobinyousefi`).

