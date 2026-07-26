"""
==================================================
SCOOBA

Voice Configuration

Author: Sachin
==================================================
"""


class VoiceConfig:

    def __init__(self):

        # Speech Engine
        self.provider = "windows"

        # Voice Profile
        self.gender = "female"

        # Speaking Speed
        self.rate = 175

        # Volume (0.0 - 1.0)
        self.volume = 1.0

        # Audio Settings
        self.sample_rate = 16000

        self.channels = 1

        # Future Features
        self.language = "en"

        self.voice_profile = "Aurora"

        self.enable_wake_word = False