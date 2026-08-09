"""
==================================================
SCOOBA

Audio Recorder

Author: Sachin
==================================================
"""

import tempfile
import queue

import numpy as np
import sounddevice as sd
import soundfile as sf


class AudioRecorder:

    def __init__(self):

        self.sample_rate = 16000
        self.channels = 1

        # ------------------------------------------
        # Audio configuration
        # ------------------------------------------

        self.block_duration = 0.03

        # Time of silence required after speech
        # before recording stops.
        self.silence_duration = 1.0

        # Maximum command length.
        self.max_duration = 15.0

        # Maximum time to wait for the user
        # to begin speaking.
        self.start_timeout = 10.0

        # ------------------------------------------
        # Voice detection configuration
        # ------------------------------------------

        self.start_threshold_multiplier = 3.0

        self.min_start_threshold = 0.008

        self.silence_threshold_multiplier = 1.8

        self.min_silence_threshold = 0.005

        # ------------------------------------------
        # Noise calibration
        # ------------------------------------------

        self.calibration_duration = 0.4

    # ==================================================
    # RMS
    # ==================================================

    def _rms(self, audio):

        if audio is None or len(audio) == 0:

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

        print("\n🎤 Listening...")
        print(
            "   Waiting for speech..."
        )

        # ------------------------------------------
        # Configuration
        # ------------------------------------------

        block_size = int(
            self.sample_rate
            * self.block_duration
        )

        max_blocks = int(
            (
                duration
                if duration
                else self.max_duration
            )
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

        # ------------------------------------------
        # Audio queue
        # ------------------------------------------

        audio_queue = queue.Queue()

        # ------------------------------------------
        # Callback
        # ------------------------------------------

        def callback(
            indata,
            frames,
            time,
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
        # CALIBRATE AMBIENT NOISE
        # ==================================================

        print(
            "   Calibrating microphone..."
        )

        calibration_samples = []

        try:

            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype="float32",
                blocksize=block_size
            ) as stream:

                calibration_blocks = int(
                    self.calibration_duration
                    / self.block_duration
                )

                for _ in range(
                    calibration_blocks
                ):

                    data, overflowed = (
                        stream.read(
                            block_size
                        )
                    )

                    calibration_samples.append(
                        data.copy()
                    )

        except Exception as e:

            print(
                f"❌ Microphone calibration failed: {e}"
            )

            raise

        # ------------------------------------------
        # Calculate ambient noise
        # ------------------------------------------

        if calibration_samples:

            calibration_audio = np.concatenate(
                calibration_samples,
                axis=0
            )

            noise_level = self._rms(
                calibration_audio
            )

        else:

            noise_level = 0.0

        start_threshold = max(
            self.min_start_threshold,
            noise_level
            * self.start_threshold_multiplier
        )

        silence_threshold = max(
            self.min_silence_threshold,
            noise_level
            * self.silence_threshold_multiplier
        )

        print(
            f"   Ambient level: "
            f"{noise_level:.5f}"
        )

        print(
            f"   Speech threshold: "
            f"{start_threshold:.5f}"
        )

        # ==================================================
        # RECORDING
        # ==================================================

        recorded_blocks = []

        speech_started = False

        silence_counter = 0

        total_blocks = 0

        # ------------------------------------------
        # Start microphone stream
        # ------------------------------------------

        try:

            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype="float32",
                blocksize=block_size,
                callback=callback
            ):

                while True:

                    # ----------------------------------
                    # Read next audio block
                    # ----------------------------------

                    try:

                        data = audio_queue.get(
                            timeout=1.0
                        )

                    except queue.Empty:

                        continue

                    total_blocks += 1

                    level = self._rms(
                        data
                    )

                    # ==================================================
                    # WAITING FOR SPEECH
                    # ==================================================

                    if not speech_started:

                        if level >= start_threshold:

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

                    # ----------------------------------
                    # Detect silence
                    # ----------------------------------

                    if level < silence_threshold:

                        silence_counter += 1

                    else:

                        silence_counter = 0

                    # ----------------------------------
                    # User stopped speaking
                    # ----------------------------------

                    if (
                        silence_counter
                        >= silence_blocks_required
                    ):

                        print(
                            "🤫 Silence detected."
                        )

                        break

                    # ----------------------------------
                    # Maximum duration
                    # ----------------------------------

                    if (
                        total_blocks
                        >= max_blocks
                    ):

                        print(
                            "⏱ Maximum recording "
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

        if not blocks:

            # Create a valid empty/silent WAV.
            audio = np.zeros(
                int(
                    self.sample_rate
                    * 0.1
                ),
                dtype=np.float32
            )

        else:

            audio = np.concatenate(
                blocks,
                axis=0
            )

        sf.write(
            temp.name,
            audio,
            self.sample_rate
        )

        print(
            "✅ Recording complete."
        )

        return temp.name