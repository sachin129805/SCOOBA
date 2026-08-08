"""
==================================================
SCOOBA

Voice Manager

Author: Sachin
==================================================
"""

from voice.audio.devices import AudioDeviceManager
from voice.audio.recorder import AudioRecorder
from voice.audio.player import AudioPlayer

from voice.pipeline import VoicePipeline

from voice.tts.manager import TTSManager

from voice.transcriber import SpeechTranscriber


class VoiceManager:

    def __init__(self):

        self.tts = TTSManager()

        self.devices = AudioDeviceManager()

        self.recorder = AudioRecorder()

        self.player = AudioPlayer()

        self.transcriber = SpeechTranscriber()

        self.pipeline = VoicePipeline(
            self.recorder,
            self.transcriber
        )

    def greet(self):

        self.tts.speak(
            "Hello Sachin. SCOOBA is online."
        )

    def list_microphones(self):

        return self.devices.get_microphones()

    def test_audio_pipeline(self):

        input("\nPress ENTER to start recording...")

        audio = self.recorder.record(5)

        self.player.play(audio)

    def listen(self):

        return self.pipeline.listen()