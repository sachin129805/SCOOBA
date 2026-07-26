"""
==================================================
SCOOBA

Vosk Speech Provider

Real Offline Speech Recognition

Author: Sachin
==================================================
"""

import json
from pathlib import Path

import sounddevice as sd
from vosk import Model, KaldiRecognizer

from voice.speech.providers.base import BaseSpeechProvider


class VoskSpeechProvider(BaseSpeechProvider):

    def __init__(self):

        model_path = Path(
            "models/speech/vosk-model-small-en-us-0.15"
        )

        if not model_path.exists():
            raise FileNotFoundError(
                f"Vosk model not found:\n{model_path}"
            )

        print("\n🧠 Loading Vosk Model...")

        self.model = Model(str(model_path))

        self.sample_rate = 16000

        print("✅ Vosk Model Loaded.")

    def listen(self) -> str:

        recognizer = KaldiRecognizer(
            self.model,
            self.sample_rate
        )

        print("\n🎤 Listening...")
        print("Speak now...\n")

        with sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=8000,
            dtype="int16",
            channels=1,
        ) as stream:

            while True:

                data, overflowed = stream.read(4000)

                if overflowed:
                    print("⚠ Audio Overflow")

                if recognizer.AcceptWaveform(bytes(data)):

                    result = json.loads(
                        recognizer.Result()
                    )

                    text = result.get("text", "").strip()

                    if text:
                        print(f"\n🧠 Recognized: {text}")
                        return text