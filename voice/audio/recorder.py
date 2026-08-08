"""
==================================================
SCOOBA

Audio Recorder

Author: Sachin
==================================================
"""

import tempfile

import sounddevice as sd
import soundfile as sf


class AudioRecorder:

    def __init__(self):

        self.sample_rate = 16000
        self.channels = 1

    def record(self, duration=5):

        print("\n🎤 Listening...")

        audio = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="float32"
        )

        sd.wait()

        temp = tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        )

        sf.write(
            temp.name,
            audio,
            self.sample_rate
        )

        print("✅ Recording complete.")

        return temp.name