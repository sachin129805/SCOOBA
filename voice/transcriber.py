"""
==================================================
SCOOBA

Faster-Whisper Transcriber

Author: Sachin
==================================================
"""

from pathlib import Path
from faster_whisper import WhisperModel


class SpeechTranscriber:

    def __init__(
        self,
        model_size="small",
        device="cpu",
        compute_type="int8"
    ):
        print(f"\n🧠 Loading Faster-Whisper ({model_size})...")

        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type
        )

        print("✅ Faster-Whisper Ready.")

    def transcribe(self, audio_path: str) -> str:
        """
        Transcribe an audio file into text.

        Args:
            audio_path (str): Path to the recorded WAV file.

        Returns:
            str: Recognized speech.
        """

        audio_path = Path(audio_path)

        if not audio_path.exists():
            raise FileNotFoundError(
                f"Audio file not found: {audio_path}"
            )

        segments, info = self.model.transcribe(
            str(audio_path),
            beam_size=5,
            language="en",
            vad_filter=True
        )

        text = " ".join(
            segment.text.strip()
            for segment in segments
        ).strip()

        print(f"\n🧠 Recognized: {text}")

        return text