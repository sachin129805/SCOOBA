"""
==================================================
SCOOBA

Piper TTS Provider

Offline Text-to-Speech using Piper.

Author: Sachin
==================================================
"""

import subprocess
from pathlib import Path

from voice.audio.player import AudioPlayer
from voice.tts.providers.base import BaseTTSProvider


class PiperTTSProvider(BaseTTSProvider):

    def __init__(self):

        self.player = AudioPlayer()

        self.piper = Path("tools/piper/piper.exe")

        self.model = Path(
            "models/tts/piper/en_US-lessac-medium.onnx"
        )

        self.config = Path(
            "models/tts/piper/en_US-lessac-medium.onnx.json"
        )

        self.espeak = Path(
            "tools/piper/espeak-ng-data"
        )

        self.output = Path(
            "data/temp/speech.wav"
        )

    def speak(self, text: str):

        if not self.piper.exists():
            raise FileNotFoundError(
                "Piper executable not found."
            )

        if not self.model.exists():
            raise FileNotFoundError(
                "Piper model not found."
            )

        self.output.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        command = [
            str(self.piper),
            "--model", str(self.model),
            "--config", str(self.config),
            "--output_file", str(self.output),
            "--espeak_data", str(self.espeak)
        ]

        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        process.communicate(text)

        if process.returncode != 0:

            raise RuntimeError(
                "Piper failed to generate speech."
            )

        self.player.play(
            str(self.output)
        )