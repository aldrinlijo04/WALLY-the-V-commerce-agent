from llm_utils import preprocess_transcription, generate_command
from actions import search_product, add_to_cart, place_order, voice_authentication, deduct_money

def execute_command(command):
    """Parse and execute the command."""
    if "search_product" in command:
        product_name = command.split(":")[1].strip()
        search_product(product_name)
    elif "add_to_cart" in command:
        product_name = command.split(":")[1].strip()
        add_to_cart(product_name)
    elif "place_order" in command:
        place_order()
    elif "voice_authentication" in command:
        voice_authentication()
    elif "deduct_money" in command:
        amount = command.split(":")[1].strip()
        deduct_money(amount)
    else:
        print("Unknown command")

def main(transcription):
    """Main function to handle the workflow."""
    preprocessed_text = preprocess_transcription(transcription)
    command = generate_command(preprocessed_text)
    execute_command(command)

if __name__ == "__main__":
    # Example transcription (replace with actual input)
    transcription = "I would like to place an order for a vacuum cleaner"
    main(transcription)
