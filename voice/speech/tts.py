"""
==================================================
SCOOBA

Text To Speech

Author: Sachin
==================================================
"""

import pyttsx3

from voice.config import VoiceConfig


class TextToSpeech:

    def __init__(self):

        self.config = VoiceConfig()

        self.engine = pyttsx3.init()

        self.engine.setProperty(
            "rate",
            self.config.rate
        )

        self.engine.setProperty(
            "volume",
            self.config.volume
        )

        voices = self.engine.getProperty("voices")

        # Try to select a female voice
        selected_voice = None

        for voice in voices:

            voice_name = voice.name.lower()

            if (
                "zira" in voice_name
                or "female" in voice_name
            ):
                selected_voice = voice.id
                break

        if selected_voice is None and len(voices) > 0:
            selected_voice = voices[0].id

        self.engine.setProperty(
            "voice",
            selected_voice
        )

    def speak(self, text: str):

        print(f"\n🤖 SCOOBA : {text}")

        self.engine.say(text)

        self.engine.runAndWait()