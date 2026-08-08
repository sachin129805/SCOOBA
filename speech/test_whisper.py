"""
==================================================
Test Faster-Whisper

Author: Sachin
==================================================
"""

from speech import AudioRecorder, WhisperEngine


def main():
    recorder = AudioRecorder()

    whisper = WhisperEngine()

    audio_file = recorder.record(duration=5)

    print("\n📝 Transcribing...")

    text = whisper.transcribe(audio_file)

    print("\n==============================")
    print("Recognized Text:")
    print(text)
    print("==============================")


if __name__ == "__main__":
    main()