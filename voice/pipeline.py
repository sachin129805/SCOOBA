"""
==================================================
SCOOBA

Voice Pipeline

Author: Sachin
==================================================
"""

import os


class VoicePipeline:

    def __init__(self, recorder, transcriber):

        self.recorder = recorder
        self.transcriber = transcriber

    def listen(self):

        audio = self.recorder.record(5)

        text = self.transcriber.transcribe(audio)

        try:
            os.remove(audio)
        except:
            pass

        return text