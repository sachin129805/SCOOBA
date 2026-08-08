"""
==================================================
SCOOBA

Whisper Engine

Author: Sachin
==================================================
"""

from pathlib import Path
from faster_whisper import WhisperModel


class WhisperEngine:
    def __init__(
        self,
        model_size="base",
        device="cpu",
        compute_type="int8"
    ):
        print("🧠 Loading Faster-Whisper...")

        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type,
        )

        print("✅ Whisper Ready")

    def transcribe(self, audio_path: str) -> str:
        """
        Transcribes an audio file.

        Args:
            audio_path (str): Path to WAV file.

        Returns:
            str: Recognized speech.
        """

        audio_path = Path(audio_path)

        if not audio_path.exists():
            raise FileNotFoundError(audio_path)

        segments, info = self.model.transcribe(
            str(audio_path),
            beam_size=5
        )

        text = " ".join(
            segment.text.strip()
            for segment in segments
        )

        return text.strip()