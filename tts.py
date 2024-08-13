from gtts import gTTS
import sys

# Get the TTS response from command-line arguments
tts_response = sys.argv[1]

# Generate TTS audio
tts = gTTS(tts_response)
tts.save('tts_output.wav')
