from transformers import pipeline

# Load the pre-trained LLM model (e.g., GPT-3)
llm = pipeline("text-generation", model="openai-community/gpt2")  # Replace with your chosen model

def preprocess_transcription(transcription):
    """Preprocess the transcription if necessary."""
    return transcription.lower().strip()

def generate_command(text):
    """Generate a command based on the preprocessed text."""
    response = llm(f"Extract the action and details from the following text: '{text}'",pad_token_id=50256)
    return response[0]['generated_text']
