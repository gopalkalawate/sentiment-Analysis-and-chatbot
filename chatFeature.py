import requests
import os
import time

from sentimentUsingNLTK import Analyse

# Get the API token from environment variable
HUGGING_FACE_API_TOKEN = os.environ.get('HUGGING_FACE_API_KEY')
analyse = Analyse()

# Check if the API token is available
if not HUGGING_FACE_API_TOKEN:
    raise ValueError("HUGGING_FACE_API_KEY environment variable is not set")

# API endpoint for the BlenderBot model
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"

headers = {"Authorization": f"Bearer {HUGGING_FACE_API_TOKEN}"}

def query_model(input_text, max_retries=5, delay=5):
    for attempt in range(max_retries):
        response = requests.post(API_URL, headers=headers, json={"inputs": input_text})
        result = response.json()
        
        if isinstance(result, dict) and "error" in result and "currently loading" in result["error"].lower():
            if attempt < max_retries - 1:
                print(f"Model is loading. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                return {"error": "Max retries reached. Model is still loading."}
        else:
            return result
    
    return {"error": "Failed to get a valid response after multiple attempts."}
listt = []
def chat():
    print("Welcome to the BlenderBot conversation bot. Type 'exit' to end the conversation.")

    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'exit':
            # analyse.plot_bar_graph()
            print("Goodbye!")
            # return analyse.listt

            break
        
        # analyse.insert_sentiment(user_input)

        try:
            response = query_model(user_input)
            if isinstance(response, list) and len(response) > 0 and "generated_text" in response[0]:
                ai_response = response[0]['generated_text'].strip()
                print(f"AI: {ai_response}")
            elif isinstance(response, dict) and "error" in response:
                print(f"Error: {response['error']}")
            else:
                print("AI: I'm sorry, I couldn't generate a response. Please try again.")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while communicating with the API: {e}")
