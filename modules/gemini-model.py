"""
Install the Google AI Python SDK

$ pip install google-generativeai
"""

import os
import google.generativeai as genai

genai.configure(api_key=os.environ["API_KEY"])

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  tools='code_execution',
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "Improved Prompt:\nPrompt:\n\nExtract the intended action, product, and wallet access requirement from the given e-commerce user input.\n\nExamples:\n\nInput: \"I want to order a vacuum cleaner\"\nOutput: \"action: want to order, product: vacuum cleaner, wallet_access: no\"\nInput: \"Please add this to my cart\"\nOutput: \"action: add to cart, product: not specified, wallet_access: no\"\nInput: \"I need to check out\"\nOutput: \"action: check out, product: not specified, wallet_access: yes\"\nInput: \"action: check out\"\nOutput: \"action: check out, product: not specified, wallet_access: yes\"\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "\n```python\n\nprint(\"action: \", \"product: \", \"wallet_access: \")\n```\n\n```Code execution output\naction:  product:  wallet_access: \n```\nI will need more information to extract the intended action, product, and wallet access requirement from the given e-commerce user input.  Please provide me with the actual user input you want me to analyze. \n",
      ],
    },
  ]
)
with open("transcription.txt") as f:
    transcript = f.read()

response = chat_session.send_message(transcript)

print(response.text)