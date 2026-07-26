"""
==================================================
SCOOBA

Voice Manager

==================================================
"""

from voice.audio.stream import AudioStream
from voice.audio.devices import AudioDeviceManager
from voice.audio.recorder import AudioRecorder
from voice.audio.player import AudioPlayer

from voice.pipeline import VoicePipeline

# 👇 CHANGE IS HERE
from voice.tts.manager import TTSManager

from voice.speech.providers.vosk_provider import (
    VoskSpeechProvider
)


class VoiceManager:

    def __init__(self):

        self.tts = TTSManager()

        self.devices = AudioDeviceManager()

        self.recorder = AudioRecorder()

        self.player = AudioPlayer()

        self.stream = AudioStream()

        self.speech = VoskSpeechProvider()

        self.pipeline = VoicePipeline(
            self.stream,
            self.speech
        )

    def greet(self):

        self.tts.speak(
            "Hello Sachin. SCOOBA is online."
        )

    def list_microphones(self):

        return self.devices.get_microphones()

    def test_audio_pipeline(self):

        input("\nPress ENTER to start recording...")

        self.recorder.record()

        self.player.play("recording.wav")

    def listen(self):

        return self.pipeline.listen()