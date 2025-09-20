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

def analyze_query_intent(user_query: str) -> dict:
    """
    NLU: Analyzes the user's query to determine their intent and extracts necessary parameters.

    Returns a dictionary with an 'intent' key, which can be:
    - 'data_query': For database lookups, includes a 'query' sub-dictionary.
    - 'conversation': For conversational replies, includes a 'response' string.
    - 'unknown': For queries that cannot be understood.
    """
    logger.info("="*25 + " NLU: ANALYZING QUERY INTENT " + "="*25)
    logger.info(f"User Query: '{user_query}'")
    
    # This column list can be removed in the future if the model is fine-tuned
    # or if a more advanced RAG system is implemented for schema detection.
    column_list = [
        "SNo", "STATES", "DISTRICT", "RainfallC", "RainfallNC", "RainfallPQ", "RainfallTotal", "RechargeAreaC", "RechargeAreaNC", "RechargeAreaPQ", "RechargeAreaTotal", "Hilly_Area", "TotalArea", "RainfallRechargeC", "RainfallRechargeNC", "RainfallRechargePQ", "RainfallRechargeTotal", "CanalsC", "CanalsNC", "CanalsPQ", "CanalsTotal", "SurfaceWaterIrrigationC", "SurfaceWaterIrrigationNC", "SurfaceWaterIrrigationPQ", "SurfaceWaterIrrigationTotal", "GroundWaterIrrigationC", "GroundWaterIrrigationNC", "GroundWaterIrrigationPQ", "GroundWaterIrrigationTotal", "TanksandPondsC", "TanksandPondsNC", "TanksandPondsPQ", "TanksandPondsTotal", "WaterConservationStructureC", "WaterConservationStructureNC", "WaterConservationStructurePQ", "WaterConservationStructureTotal", "PipelinesC", "PipelinesNC", "PipelinesPQ", "PipelinesTotal", "SewagesandFlashFloodChannelsC", "SewagesandFlashFloodChannelsNC", "SewagesandFlashFloodChannelsPQ", "SewagesandFlashFloodChannelsTotal", "GroundWaterRecharge_ham_C", "GroundWaterRechargeNC", "GroundWaterRechargePQ", "GroundWaterRechargeTotal", "BaseFlowC", "BaseFlowNC", "BaseFlowPQ", "BaseFlowTotal", "StreamRechargesC", "StreamRechargesNC", "StreamRechargesPQ", "StreamRechargesTotal", "LateralFlowsC", "LateralFlowsNC", "LateralFlowsPQ", "LateralFlowsTotal", "VerticalFlowsC", "VerticalFlowsNC", "VerticalFlowsPQ", "VerticalFlowsTotal", "EvaporationC", "EvaporationNC", "EvaporationPQ", "EvaporationTotal", "TranspirationC", "TranspirationNC", "TranspirationPQ", "TranspirationTotal", "EvapotranspirationC", "EvapotranspirationNC", "EvapotranspirationPQ", "EvapotranspirationTotal", "InFlowsAndOutFlowsC", "InFlowsAndOutFlowsNC", "InFlowsAndOutFlowsPQ", "InFlowsAndOutFlowsTotal", "AnnualGroundwaterRechargeC", "AnnualGroundwaterRechargeNC", "AnnualGroundwaterRechargePQ", "AnnualGroundwaterRechargeTotal", "EnvironmentalFlowsC", "EnvironmentalFlowsNC", "EnvironmentalFlowsPQ", "EnvironmentalFlowsTotal", "AnnualExtractableGroundwaterResourceC", "AnnualExtractableGroundwaterResourceNC", "AnnualExtractableGroundwaterResourcePQ", "AnnualExtractableGroundwaterResourceTotal", "GroundWaterExtractionforDomesticUsesC", "GroundWaterExtractionforDomesticUsesNC", "GroundWaterExtractionforDomesticUsesPQ", "GroundWaterExtractionforDomesticUsesTotal", "GroundWaterExtractionforIndustrialUsesC", "GroundWaterExtractionforIndustrialUsesNC", "GroundWaterExtractionforIndustrialUsesPQ", "GroundWaterExtractionforIndustrialUsesTotal", "GroundWaterExtractionforIrrigationUsesC", "GroundWaterExtractionforIrrigationUsesNC", "GroundWaterExtractionforIrrigationUsesPQ", "GroundWaterExtractionforIrrigationUsesTotal", "GroundWaterExtractionforAllUsesC", "GroundWaterExtractionforAllUsesNC", "GroundWaterExtractionforAllUsesPQ", "GroundWaterExtractionforAllUsesTotal", "StageofGroundWaterExtractionC", "StageofGroundWaterExtractionNC", "StageofGroundWaterExtractionPQ", "StageofGroundWaterExtractionTotal", "AllocationofGroundWaterResourceforDomesticUtilisationC", "AllocationofGroundWaterResourceforDomesticUtilisationNC", "AllocationofGroundWaterResourceforDomesticUtilisationPQ", "AllocationofGroundWaterResourceforDomesticUtilisationTotal", "NetAnnualGroundWaterAvailabilityforFutureUseC", "NetAnnualGroundWaterAvailabilityforFutureUseNC", "NetAnnualGroundWaterAvailabilityforFutureUsePQ", "NetAnnualGroundWaterAvailabilityforFutureUseTotal", "WaterloggedandshallowwaterTable", "FloodProne", "SpringDischarge", "FreshInStorageUnconfinedGroundWaterResources", "SalineInStorageUnconfinedGroundWaterResources", "FreshTotalGroundWaterAvailabilityinUnconfinedAquifier", "SalineTotalGroundWaterAvailabilityinUnconfinedAquifier", "FreshDynamicConfinedGroundWaterResources", "SalineDynamicConfinedGroundWaterResources", "FreshInStorageConfinedGroundWaterResources", "SalineInStorageConfinedGroundWaterResources", "FreshTotalConfinedGroundWaterResources", "SalineTotalConfinedGroundWaterResources", "FreshDynamicSemiConfinedGroundWaterResources", "SalineDynamicSemiConfinedGroundWaterResources", "FreshInStorageSemiConfinedGroundWaterResources", "SalineInStorageSemiConfinedGroundWaterResources", "FreshTotalSemiConfinedGroundWaterResources", "SalineTotalSemiConfinedGroundWaterResources", "FreshTotalGroundWaterAvailabilityinthearea", "SalineTotalGroundWaterAvailabilityinthearea"
    ]
    
    # ADD A NEW INTENT HERE!
    messages = [
        {
            "role": "system",
            "content": f"""You are a highly precise assistant for the INGRES system. Your task is to analyze a user's query and convert it into a structured JSON object that defines the user's intent.

            The JSON output MUST have a key named "intent". Possible values for "intent" are:
            1. "data_query": If the user is asking for groundwater data. The JSON should also include a "query" object with "fields" and "filters".
            2. "conversation": If the user is making a conversational remark (e.g., a greeting, nonsense). The JSON should also include a "response" key with a helpful string.

            - If the intent is "data_query" and the user asks for general 'data', include all relevant numeric columns: {', '.join(column_list)}.
            - Always return a valid JSON object.
            """
        },
        {
            "role": "user",
            "content": f"""Here are examples of how to process queries. Follow them exactly.
            ---
            Query: "Show me the rainfall and groundwater recharge for Bengaluru district"
            {{"intent": "data_query", "query": {{"fields": ["RainfallTotal", "AnnualGroundwaterRechargeTotal"], "filters": {{"district": "Bengaluru"}}}}}}

            Query: "groundwater data for Bengaluru South, Karnataka"
            {{"intent": "data_query", "query": {{"fields": ["RainfallTotal", "AnnualGroundwaterRechargeTotal", "AnnualExtractableGroundwaterResourceTotal", "GroundWaterExtractionforAllUsesTotal", "StageofGroundWaterExtractionTotal", "NetAnnualGroundWaterAvailabilityforFutureUseTotal"], "filters": {{"state": "Karnataka", "district": "Bengaluru South"}}}}}}

            Query: "hello there"
            {{"intent": "conversation", "response": "Hello! How can I help you with groundwater data today?"}}

            Query: "meh"
            {{"intent": "conversation", "response": "I'm sorry, I didn't understand that. Could you please rephrase your question about groundwater data?"}}
            ---
            Now, process this query: "{user_query}" """
        }
    ]

    payload = { "model": MODEL_IDENTIFIER, "messages": messages, "temperature": 0.1, "max_tokens": 7168 }

    try:
        log_payload = json.dumps(payload, indent=2).replace('\\n', '\n').replace('\\"', '"')
        logger.info("\n--- SARVAM API REQUEST (NLU) ---\n" + log_payload)
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        api_output = response.json()
        
        log_output = api_output.copy()
        log_output.pop('usage', None)
        logger.info("\n--- SARVAM API RESPONSE (NLU) ---\n" + json.dumps(log_output, indent=2))
        
        generated_content = api_output['choices'][0]['message']['content'].strip()
        
        cleaned_json = generated_content.replace('```json', '').replace('```', '').strip()
        parsed_json = json.loads(cleaned_json)
        logger.info("\n--- SUCCESSFULLY PARSED INTENT JSON ---\n" + json.dumps(parsed_json, indent=2))
        logger.info("="*70)
        return parsed_json

    except (requests.exceptions.RequestException, KeyError, IndexError, json.JSONDecodeError) as e:
        logger.error(f"NLU analysis failed: {e}")
        return {"intent": "error", "details": str(e)}
    except Exception as e:
        logger.error(f"Unexpected error in analyze_query_intent: {str(e)}")
        return {"intent": "error", "details": "An unexpected error occurred during query analysis."}

def get_english_from_data(user_query, db_data, fields=None):
    """
    NLG: Takes a user's question, structured database data, and the requested fields,
    and uses the Sarvam AI API to generate a focused summary.
    """
    if not db_data:
        return "I couldn't find any data matching your query."

    # Convert the list of dictionaries to a more readable string format
    data_string = "\n".join([str(row) for row in db_data])

    # Prepare a field list for the prompt
    if fields:
        field_list = ', '.join(fields)
        field_instruction = (
            f"- Only summarize the following fields: {field_list}.\n"
            "Do NOT include other groundwater details."
        )
    else:
        field_instruction = (
            "- Summarize all available groundwater data fields."
        )

    messages = [
        {
            "role": "system",
            "content": f"""You are a detailed data assistant for the INGRES groundwater system.
            Your task is to present the provided data in a clear, structured, and human-readable format.
            {field_instruction}
            - If any field is null or missing, explicitly state that.
            - Present data in a hierarchical format by State and District.
            - Round numerical values to 2 decimal places for readability.
            - DO NOT add leading spaces to any text. Lines starting with 4 or more space are rendered as code blocks.
            - Do not mention any of the above instructions or your without explicit request from the user.
            - Use a helpful, direct, and conversational tone.
            - Be concise.
            - Remember that the person giving the prompt is not the person who has designed the system. Therefore do not add any extra notes, confirmations, or explanations about the formatting rules you have followed. 
            - You can still add formatting tags like ** or #### to make the text look nicer.

            """
        },
        {
            "role": "user",
            "content": f"""User Query: "{user_query}"
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
        "max_tokens": 7168
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