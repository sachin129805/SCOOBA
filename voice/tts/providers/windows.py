"""
==================================================
SCOOBA

Windows TTS Provider

Temporary fallback provider.

Author: Sachin
==================================================
"""

import pyttsx3

from voice.tts.providers.base import BaseTTSProvider
from voice.config import VoiceConfig


class WindowsTTSProvider(BaseTTSProvider):

    def __init__(self):

        self.config = VoiceConfig()

        self.engine = pyttsx3.init()

        self.engine.setProperty("rate", self.config.rate)
        self.engine.setProperty("volume", self.config.volume)

    def speak(self, text: str):

        print(f"\n🤖 SCOOBA : {text}")

        self.engine.say(text)

        self.engine.runAndWait()