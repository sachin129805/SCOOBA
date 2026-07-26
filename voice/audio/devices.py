"""
==================================================
SCOOBA

Audio Device Manager

Purpose:
Discovers available audio input devices.

Author: Sachin
Version: 0.8.0
==================================================
"""

import sounddevice as sd


class AudioDeviceManager:
    """
    Handles microphone discovery.
    """

    def get_microphones(self):
        microphones = []

        devices = sd.query_devices()

        default_input = sd.default.device[0]

        for index, device in enumerate(devices):

            if device["max_input_channels"] > 0:

                microphones.append(
                    {
                        "id": index,
                        "name": device["name"],
                        "channels": device["max_input_channels"],
                        "default": index == default_input
                    }
                )

        return microphones