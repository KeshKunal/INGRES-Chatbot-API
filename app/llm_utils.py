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
    into a structured JSON object or provide a direct natural language response.
    Returns a dict if a query is understood, or a string for conversational replies.
    """
    logger.info("="*25 + " NLU: CONVERTING QUERY TO JSON " + "="*25)
    logger.info(f"User Query: '{user_query}'")
    column_list = [
        "STATES", "DISTRICT", "RainfallTotal", "AnnualGroundwaterRechargeTotal",
        "AnnualExtractableGroundwaterResourceTotal", "GroundWaterExtractionforAllUsesTotal",
        "StageofGroundWaterExtractionTotal", "NetAnnualGroundWaterAvailabilityforFutureUseTotal"
    ]

    messages = [
        {
            "role": "system",
            "content": f"""You are a highly precise assistant for the INGRES system. Your task is to analyze a user's query and respond in one of two ways:
            1. If the query is about groundwater data, convert it into a structured JSON.
               - The JSON must have 'fields' (a list of columns) and 'filters' (a dictionary for 'state' and 'district').
               - Extract state and district names accurately.
               - If the user asks for general 'data', include all relevant numeric columns: {', '.join(column_list)}.
            2. If the query is NOT about groundwater data (e.g., a greeting, nonsense), provide a brief, helpful, natural language response. DO NOT output JSON in this case.
            """
        },
        {
            "role": "user",
            "content": f"""Here are examples of how to process queries. Follow them exactly.
            ---
            Query: "Show me the rainfall and groundwater recharge for Bengaluru district"
            {{"fields": ["RainfallTotal", "AnnualGroundwaterRechargeTotal"], "filters": {{"district": "Bengaluru"}}}}

            Query: "What was the total groundwater extraction in Karnataka?"
            {{"fields": ["GroundWaterExtractionforAllUsesTotal"], "filters": {{"state": "Karnataka"}}}}

            Query: "groundwater data for Bengaluru South, Karnataka"
            {{"fields": ["RainfallTotal", "AnnualGroundwaterRechargeTotal", "AnnualExtractableGroundwaterResourceTotal", "GroundWaterExtractionforAllUsesTotal", "StageofGroundWaterExtractionTotal", "NetAnnualGroundWaterAvailabilityforFutureUseTotal"], "filters": {{"state": "Karnataka", "district": "Bengaluru South"}}}}

            Query: "hello there"
            Hello! How can I help you with groundwater data today?

            Query: "meh"
            I'm sorry, I didn't understand that. Could you please rephrase your question about groundwater data?
            ---
            Now, process this query: "{user_query}" """
        }
    ]

    payload = { "model": MODEL_IDENTIFIER, "messages": messages, "temperature": 0.1, "max_tokens": 3000 }

    try:
        log_payload = json.dumps(payload, indent=2).replace('\\n', '\n').replace('\\"', '"')
        logger.info("\n--- SARVAM API REQUEST (NLU) ---\n" + log_payload)
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        api_output = response.json()
        # Create a copy for logging and remove the verbose 'usage' block
        log_output = api_output.copy()
        log_output.pop('usage', None)
        logger.info("\n--- SARVAM API RESPONSE (NLU) ---\n" + json.dumps(log_output, indent=2))
        
        generated_content = api_output['choices'][0]['message']['content'].strip()

        # Try to parse as JSON first. If it fails, assume it's a natural language response.
        try:
            cleaned_json = generated_content.replace('```json', '').replace('```', '').strip()
            parsed_json = json.loads(cleaned_json)
            logger.info("\n--- SUCCESSFULLY PARSED JSON ---\n" + json.dumps(parsed_json, indent=2))
            logger.info("="*70)
            return parsed_json
        except json.JSONDecodeError:
            logger.info(f"Received natural language response (not JSON): '{generated_content}'")
            logger.info("="*70)
            return generated_content

    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"API error response: {e.response.text}")
        return None
    except (KeyError, IndexError) as e:
        logger.error(f"Failed to parse API response structure: {e}")
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
            "content": """You are a detailed data assistant for the INGRES groundwater system.
            Your task is to present ALL available data points in a structured format:
            - List EVERY field that has data, with appropriate units:
              * RainfallTotal (in mm)
              * AnnualGroundwaterRechargeTotal (in ham - hectare meters)
              * AnnualExtractableGroundwaterResourceTotal (in ham)
              * GroundWaterExtractionforAllUsesTotal (in ham)
              * StageofGroundWaterExtractionTotal (percentage)
              * NetAnnualGroundWaterAvailabilityforFutureUseTotal (in ham)
            - Use proper units for each measurement
            - If any field is null or missing, explicitly state that
            - Present data in a hierarchical format by State and District
            - Round numerical values to 2 decimal places for readability
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
            "Here is the complete groundwater data I found:
            - For Bengaluru district in Karnataka:
              - Total Rainfall: 1200.50 mm
              - Annual Groundwater Recharge: 450.20 ham
              - Annual Extractable Groundwater Resource: 405.18 ham
              - Total Groundwater Extraction: 380.45 ham
              - Stage of Groundwater Extraction: 93.85%
              - Net Annual Groundwater Available for Future Use: 24.73 ham
            - For Bengaluru Rural district in Karnataka:
              - Total Rainfall: 950.80 mm
              - Annual Groundwater Recharge: 320.10 ham
              - Annual Extractable Groundwater Resource: 288.09 ham
              - Total Groundwater Extraction: 245.67 ham
              - Stage of Groundwater Extraction: 85.27%
              - Net Annual Groundwater Available for Future Use: 42.42 ham"
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
        logger.info("="*25 + " NLG: GENERATING TEXT FROM DATA " + "="*25)
        logger.info(f"User Query: '{user_query}'")
        log_payload = json.dumps(payload, indent=2).replace('\\n', '\n').replace('\\"', '"')
        logger.info("\n--- SARVAM API REQUEST (NLG) ---\n" + log_payload)
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        api_output = response.json()
        # Create a copy for logging and remove the verbose 'usage' block
        log_output = api_output.copy()
        log_output.pop('usage', None)
        logger.info("\n--- SARVAM API RESPONSE (NLG) ---\n" + json.dumps(log_output, indent=2))
        
        if 'choices' in api_output and len(api_output['choices']) > 0:
            response_text = api_output['choices'][0]['message']['content'].strip()
            logger.info("\n--- SUCCESSFULLY GENERATED RESPONSE ---\n" + response_text)
            logger.info("="*70)
            return response_text
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