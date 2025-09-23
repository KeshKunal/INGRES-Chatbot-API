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

# Define units for columns
COLUMN_UNITS = {
    "SNo": "N/A", "STATES": "N/A", "DISTRICT": "N/A",
    "RainfallC": "mm", "RainfallNC": "mm", "RainfallPQ": "mm", "RainfallTotal": "mm",
    "RechargeAreaC": "Hectares", "RechargeAreaNC": "Hectares", "RechargeAreaPQ": "Hectares", "RechargeAreaTotal": "Hectares",
    "Hilly_Area": "Hectares", "TotalArea": "Hectares",
    "RainfallRechargeC": "ham", "RainfallRechargeNC": "ham", "RainfallRechargePQ": "ham", "RainfallRechargeTotal": "ham",
    "CanalsC": "ham", "CanalsNC": "ham", "CanalsPQ": "ham", "CanalsTotal": "ham",
    "SurfaceWaterIrrigationC": "ham", "SurfaceWaterIrrigationNC": "ham", "SurfaceWaterIrrigationPQ": "ham", "SurfaceWaterIrrigationTotal": "ham",
    "GroundWaterIrrigationC": "ham", "GroundWaterIrrigationNC": "ham", "GroundWaterIrrigationPQ": "ham", "GroundWaterIrrigationTotal": "ham",
    "TanksandPondsC": "ham", "TanksandPondsNC": "ham", "TanksandPondsPQ": "ham", "TanksandPondsTotal": "ham",
    "WaterConservationStructureC": "ham", "WaterConservationStructureNC": "ham", "WaterConservationStructurePQ": "ham", "WaterConservationStructureTotal": "ham",
    "PipelinesC": "ham", "PipelinesNC": "ham", "PipelinesPQ": "ham", "PipelinesTotal": "ham",
    "SewagesandFlashFloodChannelsC": "ham", "SewagesandFlashFloodChannelsNC": "ham", "SewagesandFlashFloodChannelsPQ": "ham", "SewagesandFlashFloodChannelsTotal": "ham",
    "GroundWaterRecharge_ham_C": "ham", "GroundWaterRechargeNC": "ham", "GroundWaterRechargePQ": "ham", "GroundWaterRechargeTotal": "ham",
    "BaseFlowC": "ham", "BaseFlowNC": "ham", "BaseFlowPQ": "ham", "BaseFlowTotal": "ham",
    "StreamRechargesC": "ham", "StreamRechargesNC": "ham", "StreamRechargesPQ": "ham", "StreamRechargesTotal": "ham",
    "LateralFlowsC": "ham", "LateralFlowsNC": "ham", "LateralFlowsPQ": "ham", "LateralFlowsTotal": "ham",
    "VerticalFlowsC": "ham", "VerticalFlowsNC": "ham", "VerticalFlowsPQ": "ham", "VerticalFlowsTotal": "ham",
    "EvaporationC": "ham", "EvaporationNC": "ham", "EvaporationPQ": "ham", "EvaporationTotal": "ham",
    "TranspirationC": "ham", "TranspirationNC": "ham", "TranspirationPQ": "ham", "TranspirationTotal": "ham",
    "EvapotranspirationC": "ham", "EvapotranspirationNC": "ham", "EvapotranspirationPQ": "ham", "EvapotranspirationTotal": "ham",
    "InFlowsAndOutFlowsC": "ham", "InFlowsAndOutFlowsNC": "ham", "InFlowsAndOutFlowsPQ": "ham", "InFlowsAndOutFlowsTotal": "ham",
    "AnnualGroundwaterRechargeC": "ham", "AnnualGroundwaterRechargeNC": "ham", "AnnualGroundwaterRechargePQ": "ham", "AnnualGroundwaterRechargeTotal": "ham",
    "EnvironmentalFlowsC": "ham", "EnvironmentalFlowsNC": "ham", "EnvironmentalFlowsPQ": "ham", "EnvironmentalFlowsTotal": "ham",
    "AnnualExtractableGroundwaterResourceC": "ham", "AnnualExtractableGroundwaterResourceNC": "ham", "AnnualExtractableGroundwaterResourcePQ": "ham", "AnnualExtractableGroundwaterResourceTotal": "ham",
    "GroundWaterExtractionforDomesticUsesC": "ham", "GroundWaterExtractionforDomesticUsesNC": "ham", "GroundWaterExtractionforDomesticUsesPQ": "ham", "GroundWaterExtractionforDomesticUsesTotal": "ham",
    "GroundWaterExtractionforIndustrialUsesC": "ham", "GroundWaterExtractionforIndustrialUsesNC": "ham", "GroundWaterExtractionforIndustrialUsesPQ": "ham", "GroundWaterExtractionforIndustrialUsesTotal": "ham",
    "GroundWaterExtractionforIrrigationUsesC": "ham", "GroundWaterExtractionforIrrigationUsesNC": "ham", "GroundWaterExtractionforIrrigationUsesPQ": "ham", "GroundWaterExtractionforIrrigationUsesTotal": "ham",
    "GroundWaterExtractionforAllUsesC": "ham", "GroundWaterExtractionforAllUsesNC": "ham", "GroundWaterExtractionforAllUsesPQ": "ham", "GroundWaterExtractionforAllUsesTotal": "ham",
    "StageofGroundWaterExtractionC": "%", "StageofGroundWaterExtractionNC": "%", "StageofGroundWaterExtractionPQ": "%", "StageofGroundWaterExtractionTotal": "%",
    "AllocationofGroundWaterResourceforDomesticUtilisationC": "ham", "AllocationofGroundWaterResourceforDomesticUtilisationNC": "ham", "AllocationofGroundWaterResourceforDomesticUtilisationPQ": "ham", "AllocationofGroundWaterResourceforDomesticUtilisationTotal": "ham",
    "NetAnnualGroundWaterAvailabilityforFutureUseC": "ham", "NetAnnualGroundWaterAvailabilityforFutureUseNC": "ham", "NetAnnualGroundWaterAvailabilityforFutureUsePQ": "ham", "NetAnnualGroundWaterAvailabilityforFutureUseTotal": "ham",
    "WaterloggedandshallowwaterTable": "ham", "FloodProne": "ham", "SpringDischarge": "ham",
    "FreshInStorageUnconfinedGroundWaterResources": "ham", "SalineInStorageUnconfinedGroundWaterResources": "ham", "FreshTotalGroundWaterAvailabilityinUnconfinedAquifier": "ham", "SalineTotalGroundWaterAvailabilityinUnconfinedAquifier": "ham",
    "FreshDynamicConfinedGroundWaterResources": "ham", "SalineDynamicConfinedGroundWaterResources": "ham", "FreshInStorageConfinedGroundWaterResources": "ham", "SalineInStorageConfinedGroundWaterResources": "ham", "FreshTotalConfinedGroundWaterResources": "ham", "SalineTotalConfinedGroundWaterResources": "ham",
    "FreshDynamicSemiConfinedGroundWaterResources": "ham", "SalineDynamicSemiConfinedGroundWaterResources": "ham", "FreshInStorageSemiConfinedGroundWaterResources": "ham", "SalineInStorageSemiConfinedGroundWaterResources": "ham", "FreshTotalSemiConfinedGroundWaterResources": "ham", "SalineTotalSemiConfinedGroundWaterResources": "ham",
    "FreshTotalGroundWaterAvailabilityinthearea": "ham", "SalineTotalGroundWaterAvailabilityinthearea": "ham"
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
    
    # Define a specific list of columns for generic "details" queries to prevent the LLM from inventing column names.
    default_detail_columns = [
        "RainfallTotal", "AnnualGroundwaterRechargeTotal", 
        "AnnualExtractableGroundwaterResourceTotal", "GroundWaterExtractionforAllUsesTotal",
        "StageofGroundWaterExtractionTotal", "NetAnnualGroundWaterAvailabilityforFutureUseTotal"
    ]

    # Explicit list of states to help the LLM distinguish between states and districts.
    # If a location is not in this list, it should be treated as a district by default.
    state_list = [
        "TAMILNADU", "KARNATAKA", "DAMAN AND DIU", "DELHI", "LADAKH", "RAJASTHAN", 
        "MANIPUR", "WEST BENGAL", "KERALA", "TELANGANA", "GUJARAT", "BIHAR", 
        "GOA", "CHANDIGARH", "LAKSHDWEEP", "TRIPURA", "DADRA AND NAGAR HAVELI", 
        "NAGALAND", "JHARKHAND", "ASSAM", "PUNJAB", "JAMMU AND KASHMIR", 
        "PUDUCHERRY", "ANDAMAN AND NICOBAR ISLANDS", "MEGHALAYA", "MIZORAM", 
        "MAHARASHTRA", "ARUNACHAL PRADESH", "CHHATTISGARH", "SIKKIM", "HARYANA", 
        "UTTARAKHAND", "HIMACHAL PRADESH"
    ]
    
    messages = [
        {
            "role": "system",
            "content": f"""You are a highly precise assistant for the INGRES system. Your task is to analyze a user's query and convert it into a structured JSON object that defines a list of tasks to be performed.

            The JSON output MUST have a key named "tasks", which is a list of objects. Each object in the list represents a single task.
            
            Possible tasks are:
            1. "data_query": If the user is asking for groundwater data. The task object should also include a "query" object with "fields" and "filters".
            2. "conversation": If the user is making a conversational remark. The task object should also include a "response" key with a helpful string.

            - If a user asks to compare or list data for multiple locations (e.g., 'in baksa and barpeta'), you MUST combine them into a single 'data_query' task by providing a list of names in the filter. For example: "filters": {{"district": ["baksa", "barpeta"]}}.
            - When extracting locations, use the following list of known states: {', '.join(state_list)}.
              - If a location name is in this list, it is a 'state'.
              - Otherwise, if it's a geographical location, it should be treated as a 'district'.
              - Major city names (e.g., Bengaluru, Chennai) should always be treated as districts.
            - IMPORTANT: If the user asks for general 'groundwater details' or 'data', you MUST use these exact fields in your query: {default_detail_columns}. Do NOT invent field names like 'GroundwaterDetails'.
            - If a query requires fetching data, the "data_query" task must always be the first task in the list.
            - Always return a valid JSON object.
            """
        },
        {
            "role": "user",
            "content": f"""Here are examples of how to process queries. Follow them exactly (though the names of the states/districts may vary). If you find multiple entries with the name present in them, list all of them.
            ---
            Query: "Provide the difference of the annual recharge rate in baksa and barpeta"
            {{"tasks": [{{"name": "data_query", "query": {{"fields": ["AnnualGroundwaterRechargeTotal"], "filters": {{"district": ["baksa", "barpeta"]}}}}}}]}}

            Query: "Show me the rainfall and groundwater recharge for Bengaluru district"
            {{"tasks": [{{"name": "data_query", "query": {{"fields": ["RainfallTotal", "AnnualGroundwaterRechargeTotal"], "filters": {{"district": "Bengaluru"}}}}}}]}}

            Query: "Give me all districts ground water details in delhi"
            {{"tasks": [{{"name": "data_query", "query": {{"fields": ["RainfallTotal", "AnnualGroundwaterRechargeTotal", "AnnualExtractableGroundwaterResourceTotal", "GroundWaterExtractionforAllUsesTotal", "StageofGroundWaterExtractionTotal", "NetAnnualGroundWaterAvailabilityforFutureUseTotal"], "filters": {{"state": "DELHI"}}}}}}]}}

            Query: "Compare the districts of goa and gujarat and find out which ones average annual recharge rate is more"
            {{"tasks": [{{"name": "data_query", "query": {{"fields": ["AnnualGroundwaterRechargeTotal"], "filters": {{"state": ["GOA", "GUJARAT"]}}}}}}]}}

            Query: "List all districts in goa"
            {{"tasks": [{{"name": "data_query", "query": {{"fields": ["STATES", "DISTRICT"], "filters": {{"state": "GOA"}}}}}}]}}

            Query: "hello there"
            {{"tasks": [{{"name": "conversation", "response": "Hello! How can I help you with groundwater data today?"}}]}}

            Query: "meh"
            {{"tasks": [{{"name": "conversation", "response": "I'm sorry, I didn't understand that. Could you please rephrase your question about groundwater data?"}}]}}
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

        # Attempt to clean and parse the content for logging, if it's a JSON string
        if 'choices' in log_output and len(log_output['choices']) > 0 and \
           'message' in log_output['choices'][0] and 'content' in log_output['choices'][0]['message']:
            
            raw_llm_content = log_output['choices'][0]['message']['content'].strip()
            cleaned_llm_content = raw_llm_content.replace('```json', '').replace('```', '').strip()
            
            try:
                # If the content is a JSON string, parse it and replace the string with the parsed object
                parsed_llm_content = json.loads(cleaned_llm_content)
                log_output['choices'][0]['message']['content'] = parsed_llm_content
            except json.JSONDecodeError:
                # If not valid JSON, keep the original string content
                pass

        logger.info("\n--- SARVAM API RESPONSE (NLU) ---\n" + json.dumps(log_output, indent=2))
        
        generated_content = api_output['choices'][0]['message']['content']

        # If the content is a string, clean and parse it as JSON
        if isinstance(generated_content, str):
            cleaned_json = generated_content.replace('```json', '').replace('```', '').strip()
            parsed_json = json.loads(cleaned_json)
        # If it's already a dict, use it directly
        elif isinstance(generated_content, dict):
            parsed_json = generated_content
        else:
            raise ValueError("Unexpected type for LLM content: {}".format(type(generated_content)))

        logger.info("\n--- SUCCESSFULLY PARSED INTENT JSON ---\n" + json.dumps(parsed_json, indent=2))
        logger.info("="*70)
        return parsed_json

    except (requests.exceptions.RequestException, KeyError, IndexError, json.JSONDecodeError) as e:
        logger.error(f"NLU analysis failed: {e}")
        return {"tasks": [{"name": "error", "details": str(e)}]}
    except Exception as e:
        logger.error(f"Unexpected error in analyze_query_intent: {str(e)}")
        return {"tasks": [{"name": "error", "details": "An unexpected error occurred during query analysis."}]}

def get_english_from_data(user_query, db_data, fields=None):
    """
    NLG: Takes a user's question, structured database data, and the requested fields,
    and uses the Sarvam AI API to generate a focused summary.
    Handles multi-part responses by requesting additional completions if needed.
    """
    if not db_data:
        return "I couldn't find any data matching your query."

    data_string = "\n".join([str(row) for row in db_data])

    field_instruction = (
        f"- Only summarize the following fields: {', '.join(fields)}.\nDo NOT include other groundwater details."
        if fields else "- Summarize all available groundwater data fields."
    )

    # Prepare unit information for the LLM
    unit_info_list = []
    if fields:
        for field in fields:
            unit = COLUMN_UNITS.get(field, "N/A")
            if unit != "N/A":
                unit_info_list.append(f"'{field}' is in {unit}")
        if unit_info_list:
            unit_info = "\n- Here are the units for the fields you are summarizing: " + ", ".join(unit_info_list) + "."
        else:
            unit_info = ""
    else:
        unit_info = "" # If no specific fields, LLM should infer or use N/A

    system_message = {
        "role": "system",
        "content": f"""You are a data analysis assistant for the INGRES groundwater system.
        Your primary task is to answer the user's query based *only* on the provided database data.
        - First, analyze the user's query to understand their goal (e.g., simple data retrieval, comparison, calculation).
        - If the user asks for a calculation (like 'difference', 'sum', 'total', 'average'), perform the calculation using the provided data and present the result clearly and concisely.
        - If the user asks for a simple data listing, present the data in a clear, structured, and human-readable format.
        {field_instruction}
        - If data for a requested entity is not present in the provided data, explicitly state that.
        - Round numerical values to 2 decimal places.
        - Be concise and directly answer the user's question.
        - Do not add extra notes or explanations about your formatting rules.
        - Use Markdown formatting (e.g., **, ####) for clarity.
        - DO NOT use ASCII art tables.
        - DO NOT use Markdown tables (i.e., do not use | or --- to make tables).
        - ONLY use bullet lists or plain text for presenting data.
        - IMPORTANT: When presenting numerical values, DO NOT use thousands separators (e.g., use 12345.67, not 12,345.67). The frontend will handle formatting.
        - ALWAYS include the appropriate unit after each numerical value. For example, "RainfallTotal: 661.15 mm" or "AnnualGroundwaterRechargeTotal: 68522.50 ham". For percentage values like 'StageofGroundWaterExtractionTotal', use '%' directly after the number.
        {unit_info}
        - Example of what NOT to do:
            | District | Value |
            |----------|-------|
            | X        | 123   |
        - Example of what you SHOULD do:
            - District X: Value 123 mm
            - District Y: Value 456 ham
        """
    }

    user_message = {
        "role": "user",
        "content": f"""User Query: "{user_query}"
        Database Data:
        {data_string}

        Your Summary:
        """
    }

    messages = [system_message, user_message]
    full_response_parts = [] # Use a list to collect parts
    continuation_count = 0
    max_continuations = 5  # Prevent infinite loops

    while continuation_count < max_continuations:
        payload = {
            "model": MODEL_IDENTIFIER,
            "messages": messages,
            "temperature": 0.1,
            "max_tokens": 7168
        }

        try:
            logger.info("="*25 + " NLG: GENERATING TEXT FROM DATA " + "="*25)
            logger.info(f"User Query: '{user_query}'")
            # Apply the same formatting as NLU for consistent, readable logs
            log_payload = json.dumps(payload, indent=2).replace('\\n', '\n').replace('\\"', '"')
            logger.info("\n--- SARVAM API REQUEST (NLG) ---\n" + log_payload)
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()
            api_output = response.json()
            log_output = api_output.copy()
            log_output.pop('usage', None)
            logger.info("\n--- SARVAM API RESPONSE (NLG) ---\n" + json.dumps(log_output, indent=2))

            if 'choices' in api_output and len(api_output['choices']) > 0:
                response_text = api_output['choices'][0]['message']['content'].strip()
                logger.info("\n--- SUCCESSFULLY GENERATED RESPONSE ---\n" + response_text)
                logger.info("="*70)
                full_response_parts.append(response_text) # Append to list

                # Check for continuation
                if "continued in next message" in response_text.lower() or api_output['choices'][0].get('finish_reason') == "length":
                    # Add the last assistant message to the conversation and continue
                    messages.append({"role": "assistant", "content": response_text})
                    continuation_count += 1
                    continue
                else:
                    return "\n".join(full_response_parts) # Join all parts at the end
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

    return "\n".join(full_response_parts) or "Sorry, the response was too long to complete."