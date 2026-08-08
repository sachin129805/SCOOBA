"""
==================================================
SCOOBA

Audio Recorder

Author: Sachin
==================================================
"""

import sounddevice as sd
import soundfile as sf
import tempfile


class AudioRecorder:
    def __init__(self, samplerate=16000, channels=1):
        self.samplerate = samplerate
        self.channels = channels

    def record(self, duration=5):
        """
        Records audio from the microphone and saves it
        to a temporary WAV file.

        Returns:
            str: Path to the recorded audio file.
        """

        print("\n🎤 Listening...")

        audio = sd.rec(
            int(duration * self.samplerate),
            samplerate=self.samplerate,
            channels=self.channels,
            dtype="float32",
        )

        sd.wait()

        temp = tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        )

        sf.write(
            temp.name,
            audio,
            self.samplerate
        )

        print("✅ Recording Complete")

        return temp.name