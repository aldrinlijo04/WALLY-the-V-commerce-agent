import torch
from transformers import pipeline
import os

device = "cuda:0" if torch.cuda.is_available() else "cpu"

pipe = pipeline(
  "automatic-speech-recognition",
  model="openai/whisper-small.en",
  chunk_length_s=30,
  device=device,
)

# Get the latest file in the recordings directory
recordings_dir = "recordings"
latest_file = max([os.path.join(recordings_dir, f) for f in os.listdir(recordings_dir)], key=os.path.getctime)

# Transcribe the latest audio file
prediction = pipe(latest_file, batch_size=32)
transcription_text = prediction["text"]

# to save the transciption text into a file:
try:
  with open("transcription.txt","w") as f:
      f.write(transcription_text)
      f.close()
  print(f"Transcription file {transcription_text} has been updated")
except:
  print("Error in writing the transcription text into a file")