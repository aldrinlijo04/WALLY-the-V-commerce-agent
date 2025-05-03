import os
from faster_whisper import WhisperModel

# Load the model (you can choose "base", "small", "medium", "large-v2", etc.)
model_size = "small"
model = WhisperModel(model_size, compute_type="int8", device="cpu")  # use "int8" for best speed-memory tradeoff

# Transcribe an audio file (must be in .wav, .mp3, .m4a, etc.)
segments, info = model.transcribe("../../middle_ware/recordings/recording.wav")

# Print transcription info
print("Detected language:", info.language)
print("Transcription segments:")
# Print each segment
for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")

# Ensure the directory exists before writing
output_dir = "../../middle_ware/transcriptions/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)  # Create the directory if it doesn't exist

# Try writing the transcription to a text file
try:
    with open(os.path.join(output_dir, "transcription.txt"), "w") as f:
        for segment in segments:
            f.write(f"{segment.text}\n")  # Add a newline after each segment's text
    print("Transcription file has been updated successfully.")
except Exception as e:
    print(f"Error writing transcription to file: {e}")
