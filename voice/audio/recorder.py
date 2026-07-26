"""
==================================================
SCOOBA

Audio Recorder

Purpose:
Records microphone input.

Author: Sachin
==================================================
"""

import sounddevice as sd
import soundfile as sf


class AudioRecorder:

    def record(
        self,
        filename="recording.wav",
        duration=5,
        sample_rate=44100
    ):

        print("\n🎙 Recording...")

        audio = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="float32"
        )

        sd.wait()

        sf.write(
            filename,
            audio,
            sample_rate
        )

        print("✅ Recording saved.")