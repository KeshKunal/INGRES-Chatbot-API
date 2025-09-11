import os
import requests
import json
from dotenv import load_dotenv

# --- PART 1: SETUP ---

# Load variables from your .env file
load_dotenv()

# Get the API Key from the environment by its NAME
SARVAM_API_KEY = os.environ.get("SARVAM_API_KEY")

# Check if the key was loaded successfully
if not SARVAM_API_KEY:
    raise ValueError("API key not found. Please set the SARVAM_API_KEY in your .env file.")

# Define the API details from the documentation
API_URL = "https://api.sarvam.ai/v1/chat/completions"
MODEL_IDENTIFIER = "sarvam-m"

# Prepare the headers for all API requests
headers = {
    "Authorization": f"Bearer {SARVAM_API_KEY}",
    "Content-Type": "application/json"
}


# --- PART 2: CORE LLM FUNCTIONS ---

def get_json_from_query(user_query):
    """
    NLU: Takes a user's question and uses the Sarvam AI API to convert it
    into a structured JSON object.
    """
    messages = [
        {
            "role": "system",
            "content": "You are a highly intelligent assistant for the INGRES system. Your task is to convert a user's query into a structured JSON format. You must only return a valid JSON object and nothing else."
        },
        {
            "role": "user",
            "content": f"""Here are some examples:
            Query: "What was the groundwater extraction in Anantapur block in 2023?"
            JSON: {{"intent": "get_groundwater_data", "filters": {{"assessment_unit": "Anantapur block", "year": 2023, "metric": "extraction"}}}}

            Query: "List all over-exploited units in Karnataka"
            JSON: {{"intent": "get_units_by_category", "filters": {{"state": "Karnataka", "category": "Over-Exploited"}}}}
            ---
            Now, convert this query: "{user_query}" """
        }
    ]
    payload = { "model": MODEL_IDENTIFIER, "messages": messages, "temperature": 0.1, "max_tokens": 300 }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        api_output = response.json()
        generated_content = api_output['choices'][0]['message']['content'].strip()
        cleaned_json = generated_content.replace('```json', '').replace('```', '').strip()
        return json.loads(cleaned_json)
    except Exception as e:
        print(f"An error occurred in get_json_from_query: {e}")
        return None

def get_english_from_data(user_query, db_data):
    """
    NLG: Takes a user's question and raw database data, and uses the
    Sarvam AI API to generate a friendly, human-readable response.
    """
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant for the INGRES groundwater system. Your task is to answer the user's question based on the data provided. Respond in a clear and concise manner."
        },
        {
            "role": "user",
            "content": f"""The user's original question was: "{user_query}"
            Here is the data retrieved from the database:
            {str(db_data)}
            Please provide a natural language response to the user based on this data."""
        }
    ]
    payload = { "model": MODEL_IDENTIFIER, "messages": messages, "temperature": 0.7, "max_tokens": 400 }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        api_output = response.json()
        return api_output['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"An error occurred in get_english_from_data: {e}")
        return "Sorry, I encountered an error while formulating the response."