"""
==================================================
SCOOBA

Audio Player

Purpose:
Plays WAV recordings.

Author: Sachin
==================================================
"""

import sounddevice as sd
import soundfile as sf


class AudioPlayer:

    def play(self, filename):

        data, samplerate = sf.read(filename)

        print("\n▶ Playing recording...\n")

        sd.play(data, samplerate)

        sd.wait()