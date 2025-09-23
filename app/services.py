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
        # It maps a task name to its corresponding handler method.
        self.task_handlers = {
            "data_query": self._handle_data_query,
            "conversation": self._handle_conversation,
            # --- Future handlers for multi-tasking can be added here ---
            # "generate_visualization": self._handle_visualization,
            # "export_data": self._handle_data_export,
        }

    async def generate_streaming_response(self, request: ChatRequest):
        """
        Main entry point for generating responses.
        1. Analyzes the query to get a list of tasks.
        2. Executes each task, collecting final outputs.
        3. Composes and streams a single, final response.
        """
        logger.info(f"Processing query: {request.query}")
        
        task_context = {}
        final_response_parts = []

        try:
            yield "data: {\"type\": \"status\", \"message\": \"Analyzing your query...\"}\n\n"
            
            nlu_result = analyze_query_intent(request.query)
            tasks = nlu_result.get("tasks", [])

            if not tasks:
                yield "I'm sorry, I could not determine what to do with your request."
                return

            # 2. Loop through tasks, stream status updates, and collect final text outputs.
            for task in tasks:
                task_name = task.get("name", "unknown")
                handler = self.task_handlers.get(task_name, self._handle_unknown_task)
                
                async for chunk in handler(request, task, task_context):
                    if isinstance(chunk, str) and chunk.startswith("data:"):
                        yield chunk  # Pass status updates directly to the client
                    elif isinstance(chunk, dict) and chunk.get("type") == "final_text":
                        final_response_parts.append(chunk.get("content")) # Collect final text

            # 3. After all tasks are complete, combine the collected parts into a single response.
            if final_response_parts:
                # Join the parts with a Markdown horizontal rule for clear separation.
                final_response = "\n\n---\n\n".join(filter(None, final_response_parts))
                yield final_response

        except Exception as e:
            logger.error(f"Error in streaming response pipeline: {str(e)}")
            error_payload = {
                "type": "error",
                "text": "I'm sorry, a critical error occurred.",
                "errorDetails": str(e)
            }
            yield f"data: {json.dumps(error_payload)}\n\n"

    # --- HANDLER METHODS ---
    # Handlers now yield status updates and a structured dict for their final text output.

    async def _handle_conversation(self, request: ChatRequest, task: dict, task_context: dict):
        """Handles simple conversational replies."""
        logger.info("Executing task: conversation")
        response = task.get("response", "I'm not sure how to respond to that. Please ask me about groundwater data.")
        yield {"type": "final_text", "content": response}

    async def _handle_data_query(self, request: ChatRequest, task: dict, task_context: dict):
        """Handles the full pipeline for a database query."""
        logger.info("Executing task: data_query")
        
        query_json = task.get('query')
        if not query_json:
            yield {"type": "final_text", "content": "I understood that you're asking for data, but I couldn't figure out the specifics. Could you please rephrase?"}
            return

        # Step 1: Yield status and fetch data
        yield "data: {\"type\": \"status\", \"message\": \"Fetching groundwater data...\"}\n\n"
        filters = query_json.get('filters', {})
        fields = query_json.get('fields', [])
        db_results = execute_query(fields, filters)
        logger.info(f"Database returned {len(db_results)} results")

        task_context['db_results'] = db_results

        # Step 2: Yield status and generate summary
        yield "data: {\"type\": \"status\", \"message\": \"Preparing your summary...\"}\n\n"
        response_text = get_english_from_data(request.query, db_results, fields)
        
        # Step 3: Yield the final text output in a structured way
        yield {"type": "final_text", "content": response_text}

    async def _handle_unknown_task(self, request: ChatRequest, task: dict, task_context: dict):
        """Handles cases where the task name is not recognized."""
        logger.warning(f"Unhandled task: {task.get('name')}")
        yield {"type": "final_text", "content": "I'm sorry, I'm not sure how to handle part of your request. Please try asking in a different way."}

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