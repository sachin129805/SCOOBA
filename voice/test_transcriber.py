from voice.recorder import AudioRecorder
from voice.transcriber import SpeechTranscriber

recorder = AudioRecorder()
transcriber = SpeechTranscriber()

audio = recorder.record(5)

print("\nTranscribing...\n")

text = transcriber.transcribe(audio)

print("Recognized:", text)