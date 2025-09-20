# app/services.py
import asyncio
import json
from .api.schemas import ChatRequest
from .llm_utils import analyze_query_intent, get_english_from_data
from .db import execute_query
from .logger import get_logger

logger = get_logger(__name__)

class ChatService:
    """
    Orchestrates the chatbot's response generation by analyzing user intent
    and dispatching to the appropriate handler.
    """

    def __init__(self):
        # This handler map is the key to making the system extensible.
        # To add new functionality (e.g., visualization), just add a new
        # intent and its corresponding handler method here.
        self.intent_handlers = {
            "data_query": self._handle_data_query,
            "conversation": self._handle_conversation,
            # --- Future handlers can be added here ---
            # "bhashini_translate": self._handle_bhashini_translation,
            # "generate_visualization": self._handle_visualization,
            # "export_data": self._handle_data_export,
        }

    async def generate_streaming_response(self, request: ChatRequest):
        """
        Main entry point for generating responses.
        1. Analyzes intent.
        2. Dispatches to the correct handler.
        3. Streams the response.
        """
        logger.info(f"Processing query: {request.query}")
        
        try:
            yield "data: {\"type\": \"status\", \"message\": \"Analyzing your query...\"}\n\n"
            
            # 1. Analyze Intent
            intent_details = analyze_query_intent(request.query)
            intent = intent_details.get("intent", "unknown")

            # 2. Dispatch to the appropriate handler
            handler = self.intent_handlers.get(intent, self._handle_unknown_intent)
            
            async for chunk in handler(request, intent_details):
                yield chunk

        except Exception as e:
            logger.error(f"Error in streaming response pipeline: {str(e)}")
            error_payload = {
                "type": "error",
                "text": "I'm sorry, a critical error occurred.",
                "errorDetails": str(e)
            }
            yield f"data: {json.dumps(error_payload)}\n\n"

    # --- HANDLER METHODS ---
    # Each handler is a self-contained unit of logic for a specific intent.

    async def _handle_conversation(self, request: ChatRequest, intent_details: dict):
        """Handles simple conversational replies."""
        logger.info("Handling intent: conversation")
        response = intent_details.get("response", "I'm not sure how to respond to that. Please ask me about groundwater data.")
        yield response

    async def _handle_data_query(self, request: ChatRequest, intent_details: dict):
        """Handles the full pipeline for a database query."""
        logger.info("Handling intent: data_query")
        
        query_json = intent_details.get('query')
        if not query_json:
            yield "I understood that you're asking for data, but I couldn't figure out the specifics. Could you please rephrase?"
            return

        # Step 2.1: Fetch data from the database
        yield "data: {\"type\": \"status\", \"message\": \"Fetching groundwater data...\"}\n\n"
        filters = query_json.get('filters', {})
        fields = query_json.get('fields', [])
        db_results = execute_query(fields, filters)
        logger.info(f"Database returned {len(db_results)} results")

        # Step 2.2: Generate natural language response from the data
        yield "data: {\"type\": \"status\", \"message\": \"Preparing your summary...\"}\n\n"
        response_text = get_english_from_data(request.query, db_results, fields)
        
        yield response_text

    async def _handle_unknown_intent(self, request: ChatRequest, intent_details: dict):
        """Handles cases where the intent is not recognized."""
        logger.warning(f"Unhandled intent: {intent_details.get('intent')}")
        yield "I'm sorry, I'm not sure how to handle that request. Please try asking in a different way."

    def _prepare_visualization(self, data, query):
        """Create chart data based on real database results."""
        if not data or len(data) == 0:
            return None
        
        # Get the first few records for visualization
        sample_data = data[:10]  # Limit to first 10 records for chart clarity
        
        # Extract location names (district/state)
        labels = []
        for item in sample_data:
            if 'DISTRICT' in item and 'STATES' in item:
                labels.append(f"{item['DISTRICT']}, {item['STATES']}")
            elif 'DISTRICT' in item:
                labels.append(item['DISTRICT'])
            elif 'STATES' in item:
                labels.append(item['STATES'])
            else:
                labels.append("Unknown Location")
        
        # Determine what type of data to visualize based on available columns
        chart_data = None
        chart_title = "Groundwater Data"
        
        # Check for different types of groundwater data
        if 'AnnualGroundwaterRechargeTotal' in sample_data[0]:
            values = [float(item.get('AnnualGroundwaterRechargeTotal', 0)) for item in sample_data]
            chart_title = "Annual Groundwater Recharge (HAM)"
            chart_data = {
                "labels": labels,
                "datasets": [{
                    "label": 'Annual Groundwater Recharge (HAM)',
                    "data": values,
                    "backgroundColor": 'rgba(54, 162, 235, 0.6)',
                    "borderColor": 'rgba(54, 162, 235, 1)',
                    "borderWidth": 1
                }]
            }
        elif 'RainfallTotal' in sample_data[0]:
            values = [float(item.get('RainfallTotal', 0)) for item in sample_data]
            chart_title = "Total Rainfall (mm)"
            chart_data = {
                "labels": labels,
                "datasets": [{
                    "label": 'Total Rainfall (mm)',
                    "data": values,
                    "backgroundColor": 'rgba(75, 192, 192, 0.6)',
                    "borderColor": 'rgba(75, 192, 192, 1)',
                    "borderWidth": 1
                }]
            }
        elif 'GroundWaterExtractionforAllUsesTotal' in sample_data[0]:
            values = [float(item.get('GroundWaterExtractionforAllUsesTotal', 0)) for item in sample_data]
            chart_title = "Total Groundwater Extraction (HAM)"
            chart_data = {
                "labels": labels,
                "datasets": [{
                    "label": 'Total Groundwater Extraction (HAM)',
                    "data": values,
                    "backgroundColor": 'rgba(255, 99, 132, 0.6)',
                    "borderColor": 'rgba(255, 99, 132, 1)',
                    "borderWidth": 1
                }]
            }
        
        if chart_data:
            return {
                "type": "graph",
                "text": f"{chart_title} for your query",
                "data": {
                    "visualType": "bar",
                    "title": chart_title,
                    "chartData": chart_data
                }
            }
        
        return None