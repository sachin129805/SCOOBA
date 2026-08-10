"""
==================================================
SCOOBA

Audio Recorder

Continuous / Adaptive Speech Detection

Author: Sachin
==================================================
"""

import tempfile
import queue
import time

import numpy as np
import sounddevice as sd
import soundfile as sf


class AudioRecorder:

    def __init__(self):

        # ==================================================
        # AUDIO
        # ==================================================

        self.sample_rate = 16000
        self.channels = 1

        # 30 ms audio frames
        self.block_duration = 0.03

        # ==================================================
        # LISTENING
        # ==================================================

        # Maximum time to wait for speech to begin
        self.start_timeout = 10.0

        # Absolute safety limit for one command
        self.max_duration = 30.0

        # Silence required before ending command
        self.silence_duration = 1.7

        # ==================================================
        # NOISE CALIBRATION
        # ==================================================

        self.calibration_duration = 0.5

        # ==================================================
        # VOLUME THRESHOLDS
        # ==================================================

        self.start_threshold_multiplier = 3.0

        self.silence_threshold_multiplier = 1.8

        self.minimum_speech_threshold = 0.008

        self.minimum_silence_threshold = 0.005

    # ==================================================
    # RMS
    # ==================================================

    def _rms(self, audio):

        if audio is None:
            return 0.0

        if len(audio) == 0:
            return 0.0

        audio = np.asarray(
            audio,
            dtype=np.float32
        )

        return float(
            np.sqrt(
                np.mean(
                    np.square(audio)
                )
            )
        )

    # ==================================================
    # RECORD
    # ==================================================

    def record(self, duration=None):

        print(
            "\n🎤 Listening..."
        )

        print(
            "   Waiting for speech..."
        )

        # ==================================================
        # CONFIGURATION
        # ==================================================

        block_size = int(
            self.sample_rate
            * self.block_duration
        )

        maximum_duration = (
            duration
            if duration is not None
            else self.max_duration
        )

        max_blocks = int(
            maximum_duration
            / self.block_duration
        )

        start_timeout_blocks = int(
            self.start_timeout
            / self.block_duration
        )

        silence_blocks_required = int(
            self.silence_duration
            / self.block_duration
        )

        calibration_blocks = int(
            self.calibration_duration
            / self.block_duration
        )

        # ==================================================
        # QUEUE
        # ==================================================

        audio_queue = queue.Queue()

        # ==================================================
        # CALLBACK
        # ==================================================

        def callback(
            indata,
            frames,
            callback_time,
            status
        ):

            if status:

                print(
                    f"⚠ Audio status: {status}"
                )

            audio_queue.put(
                indata.copy()
            )

        # ==================================================
        # STATE
        # ==================================================

        speech_started = False

        silence_counter = 0

        total_blocks = 0

        recorded_blocks = []

        # ==================================================
        # MICROPHONE
        # ==================================================

        try:

            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype="float32",
                blocksize=block_size,
                callback=callback
            ):

                # ==================================================
                # CALIBRATION
                # ==================================================

                print(
                    "   Calibrating microphone..."
                )

                calibration_samples = []

                for _ in range(
                    calibration_blocks
                ):

                    try:

                        data = (
                            audio_queue.get(
                                timeout=1.0
                            )
                        )

                        calibration_samples.append(
                            data
                        )

                    except queue.Empty:

                        continue

                # ==================================================
                # CALCULATE NOISE
                # ==================================================

                if calibration_samples:

                    calibration_audio = (
                        np.concatenate(
                            calibration_samples,
                            axis=0
                        )
                    )

                    noise_level = self._rms(
                        calibration_audio
                    )

                else:

                    noise_level = 0.0

                # ==================================================
                # ADAPTIVE THRESHOLDS
                # ==================================================

                speech_threshold = max(
                    self.minimum_speech_threshold,
                    noise_level
                    * self.start_threshold_multiplier
                )

                silence_threshold = max(
                    self.minimum_silence_threshold,
                    noise_level
                    * self.silence_threshold_multiplier
                )

                print(
                    f"   Ambient level: "
                    f"{noise_level:.5f}"
                )

                print(
                    f"   Speech threshold: "
                    f"{speech_threshold:.5f}"
                )

                print(
                    f"   Silence threshold: "
                    f"{silence_threshold:.5f}"
                )

                # ==================================================
                # MAIN LISTENING LOOP
                # ==================================================

                while True:

                    # ------------------------------------------
                    # Get next audio frame
                    # ------------------------------------------

                    try:

                        data = (
                            audio_queue.get(
                                timeout=1.0
                            )
                        )

                    except queue.Empty:

                        continue

                    total_blocks += 1

                    level = self._rms(
                        data
                    )

                    # ==================================================
                    # WAIT FOR SPEECH
                    # ==================================================

                    if not speech_started:

                        if level >= speech_threshold:

                            speech_started = True

                            print(
                                "🗣️ Speech detected."
                            )

                            recorded_blocks.append(
                                data
                            )

                            silence_counter = 0

                        elif (
                            total_blocks
                            >= start_timeout_blocks
                        ):

                            print(
                                "⌛ No speech detected."
                            )

                            return self._save_audio(
                                []
                            )

                        continue

                    # ==================================================
                    # SPEECH ACTIVE
                    # ==================================================

                    recorded_blocks.append(
                        data
                    )

                    # ==================================================
                    # SILENCE DETECTION
                    # ==================================================

                    if level < silence_threshold:

                        silence_counter += 1

                    else:

                        silence_counter = 0

                    # ==================================================
                    # COMMAND END
                    # ==================================================

                    if (
                        silence_counter
                        >= silence_blocks_required
                    ):

                        print(
                            "🤫 Natural pause detected."
                        )

                        break

                    # ==================================================
                    # SAFETY LIMIT
                    # ==================================================

                    if (
                        total_blocks
                        >= max_blocks
                    ):

                        print(
                            "⏱ Maximum command "
                            "duration reached."
                        )

                        break

        except Exception as e:

            print(
                f"❌ Recording failed: {e}"
            )

            raise

        # ==================================================
        # SAVE
        # ==================================================

        return self._save_audio(
            recorded_blocks
        )

    # ==================================================
    # SAVE AUDIO
    # ==================================================

    def _save_audio(
        self,
        blocks
    ):

        temp = tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        )

        # --------------------------------------------------
        # No speech
        # --------------------------------------------------

        if not blocks:

            audio = np.zeros(
                int(
                    self.sample_rate
                    * 0.1
                ),
                dtype=np.float32
            )

        # --------------------------------------------------
        # Speech
        # --------------------------------------------------

        else:

            audio = np.concatenate(
                blocks,
                axis=0
            )

        # ==================================================
        # WRITE WAV
        # ==================================================

        sf.write(
            temp.name,
            audio,
            self.sample_rate
        )

        print(
            "✅ Recording complete."
        )

        return temp.name