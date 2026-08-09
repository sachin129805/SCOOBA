"""
==================================================
SCOOBA

Voice Pipeline

Author: Sachin
==================================================
"""

import os


class VoicePipeline:

    def __init__(
        self,
        recorder,
        transcriber
    ):

        self.recorder = recorder

        self.transcriber = transcriber

    # ==================================================
    # LISTEN
    # ==================================================

    def listen(self):

        audio = None

        try:

            # ------------------------------------------
            # Record until natural silence
            # ------------------------------------------

            audio = self.recorder.record()

            if not audio:

                return ""

            # ------------------------------------------
            # Transcribe
            # ------------------------------------------

            text = (
                self.transcriber.transcribe(
                    audio
                )
            )

            return (
                text.strip()
                if text
                else ""
            )

        except Exception as e:

            print(
                f"❌ Voice pipeline error: {e}"
            )

            return ""

        finally:

            # ------------------------------------------
            # Always remove temporary audio
            # ------------------------------------------

            if audio:

                try:

                    if os.path.exists(audio):

                        os.remove(audio)

                except Exception as e:

                    print(
                        f"⚠ Could not remove "
                        f"temporary audio: {e}"
                    )