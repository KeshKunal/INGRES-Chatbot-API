import os
import requests
import json
from dotenv import load_dotenv

# --- PART 1: SETUP ---

import os
import requests
import json
from dotenv import load_dotenv
from .logger import get_logger

# Initialize logger
logger = get_logger(__name__)

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
    into a structured JSON object, including which fields to select.
    """
    logger.info(f"Attempting to convert query to JSON: {user_query}")
    column_list = [
        "STATES", "DISTRICT", "RainfallTotal", "AnnualGroundwaterRechargeTotal",
        "AnnualExtractableGroundwaterResourceTotal", "GroundWaterExtractionforAllUsesTotal",
        "StageofGroundWaterExtractionTotal", "NetAnnualGroundWaterAvailabilityforFutureUseTotal"
    ]

    messages = [
        {
            "role": "system",
            "content": f"""You are a highly precise assistant for the INGRES system. Your only task is to convert a user's query into a structured JSON.
            - The JSON must have 'fields' (a list of columns) and 'filters' (a dictionary for 'state' and 'district').
            - Extract the state and district names accurately, even if they have multiple words.
            - If the user asks for general 'data', include all relevant numeric columns in the 'fields' list.
            - Relevant columns are: {', '.join(column_list)}.
            - Only return a valid JSON object.
            """
        },
        {
            "role": "user",
            "content": f"""Here are examples of how to convert queries. Follow them exactly.
            ---
            Query: "Show me the rainfall and groundwater recharge for Bengaluru district"
            JSON: {{"fields": ["RainfallTotal", "AnnualGroundwaterRechargeTotal"], "filters": {{"district": "Bengaluru"}}}}

            Query: "What was the total groundwater extraction in Karnataka?"
            JSON: {{"fields": ["GroundWaterExtractionforAllUsesTotal"], "filters": {{"state": "Karnataka"}}}}

            Query: "groundwater data for Bengaluru South, Karnataka"
            JSON: {{"fields": ["RainfallTotal", "AnnualGroundwaterRechargeTotal", "AnnualExtractableGroundwaterResourceTotal", "GroundWaterExtractionforAllUsesTotal", "StageofGroundWaterExtractionTotal", "NetAnnualGroundWaterAvailabilityforFutureUseTotal"], "filters": {{"state": "Karnataka", "district": "Bengaluru South"}}}}
            ---
            Now, convert this query: "{user_query}" """
        }
    ]

    payload = { "model": MODEL_IDENTIFIER, "messages": messages, "temperature": 0.1, "max_tokens": 3000 }

    try:
        logger.info(f"Sending request to Sarvam AI API with payload: {payload}")
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        api_output = response.json()
        logger.debug(f"API Response: {api_output}")
        generated_content = api_output['choices'][0]['message']['content'].strip()
        cleaned_json = generated_content.replace('```json', '').replace('```', '').strip()
        parsed_json = json.loads(cleaned_json)
        logger.info(f"Successfully parsed query into JSON: {parsed_json}")
        return parsed_json
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"API error response: {e.response.text}")
        return None
    except (KeyError, json.JSONDecodeError) as e:
        logger.error(f"Failed to parse API response: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in get_json_from_query: {str(e)}")
        return None

def get_english_from_data(user_query, db_data):
    """
    NLG: Takes a user's question and structured database data, and uses the
    Sarvam AI API to generate a direct, data-driven summary.
    """
    if not db_data:
        return "I couldn't find any data matching your query."

    # Convert the list of dictionaries to a more readable string format
    data_string = "\n".join([str(row) for row in db_data])

    messages = [
        {
            "role": "system",
            "content": """You are a straightforward data assistant for the INGRES system.
            Your ONLY job is to summarize the database results provided.
            - Summarize the key data points in a simple bulleted list.
            - DO NOT use any external knowledge.
            - If the data for a field is missing or null, state that directly.
            - Be concise and direct. Do not add conversational fluff or list your capabilities.
            """
        },
        {
            "role": "user",
            "content": f"""Here is an example of a good response.
            ---
            User Query: "Show me all groundwater data for Bengaluru"
            Database Data:
            {{'STATES': 'Karnataka', 'DISTRICT': 'Bengaluru', 'RainfallTotal': 1200.5, 'AnnualGroundwaterRechargeTotal': 450.2}}
            {{'STATES': 'Karnataka', 'DISTRICT': 'Bengaluru Rural', 'RainfallTotal': 950.8, 'AnnualGroundwaterRechargeTotal': 320.1}}

            Your Summary:
            "Here is the groundwater data I found:
            - For Bengaluru district in Karnataka:
              - Total Rainfall: 1200.5 mm
              - Annual Groundwater Recharge: 450.2 ham
            - For Bengaluru Rural district in Karnataka:
              - Total Rainfall: 950.8 mm
              - Annual Groundwater Recharge: 320.1 ham"
            ---
            Now, provide a similar summary for the following.

            User Query: "{user_query}"
            Database Data:
            {data_string}

            Your Summary:
            """
        }
    ]
    
    payload = {
        "model": MODEL_IDENTIFIER,
        "messages": messages,
        "temperature": 0.1,
        "max_tokens": 1000
    }

    try:
        # Log the request
        logger.info(f"Sending data-to-text request for query: {user_query}")
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        api_output = response.json()
        logger.debug(f"API Response: {api_output}")
        
        if 'choices' in api_output and len(api_output['choices']) > 0:
            return api_output['choices'][0]['message']['content'].strip()
        else:
            logger.error("API response missing 'choices' or empty choices array")
            return "I'm sorry, but I couldn't generate a proper summary from the data."
            
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed in get_english_from_data: {e}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"API error response: {e.response.text}")
        return "Sorry, I encountered an error while summarizing the data."
        
    except Exception as e:
        logger.error(f"Unexpected error in get_english_from_data: {str(e)}")
        return "Sorry, I encountered an error while formulating the response."