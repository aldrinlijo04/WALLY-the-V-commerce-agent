import torch
from transformers import pipeline
#from datasets import load_dataset

device = "cuda:0" if torch.cuda.is_available() else "cpu"

pipe = pipeline(
  "automatic-speech-recognition",
  model="openai/whisper-small.en",
  chunk_length_s=30,
  device=device,
)

#ds = load_dataset("hf-internal-testing/librispeech_asr_dummy", "clean", split="validation")
#sample = ds[0]["audio"]

prediction = pipe("recorded_audio.wav", batch_size=8)
print(prediction["text"])

# we can also return timestamps for the predictions
#prediction = pipe(sample.copy(), batch_size=8, return_timestamps=True)["chunks"]
