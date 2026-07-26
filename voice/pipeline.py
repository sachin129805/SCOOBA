"""
==================================================
SCOOBA

Voice Pipeline

Purpose:
Coordinates the complete voice workflow.

Author: Sachin
==================================================
"""


class VoicePipeline:

    def __init__(self, stream, speech):

        self.stream = stream
        self.speech = speech

    def listen(self):

        self.stream.start()

        text = self.speech.listen()

        self.stream.stop()

        return text