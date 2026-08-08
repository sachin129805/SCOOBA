from speech.recorder import AudioRecorder

rec = AudioRecorder()

wav = rec.record(5)

print("\nSaved:", wav)