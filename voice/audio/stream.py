"""
==================================================
SCOOBA

Live Audio Stream

Author: Sachin
==================================================
"""

from voice.config import VoiceConfig


class AudioStream:

    def __init__(self):

        self.config = VoiceConfig()

        self.sample_rate = self.config.sample_rate

        self.channels = self.config.channels

        self.running = False

    def start(self):

        self.running = True

        print("\n🎤 Audio stream started...")

    def stop(self):

        self.running = False

        print("🛑 Audio stream stopped.")