"""
==================================================
SCOOBA

TTS Manager

Author: Sachin
==================================================
"""

from voice.tts.providers.piper import PiperTTSProvider


class TTSManager:

    def __init__(self):

        self.provider = PiperTTSProvider()

    def speak(self, text: str):

        self.provider.speak(text)