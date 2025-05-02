from faster_whisper import WhisperModel

# Load the model (you can choose "base", "small", "medium", "large-v2", etc.)
model_size = "small"
model = WhisperModel(model_size, compute_type="int8")  # use "int8" for best speed-memory tradeoff

# Transcribe an audio file (must be in .wav, .mp3, .m4a, etc.)
segments, info = model.transcribe("models\\recordings\\testing.mp3.mp3")

# Print transcription info
print("Detected language:", info.language)
print("Transcription segments:")

# Print each segment
for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
