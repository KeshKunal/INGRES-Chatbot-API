# app/services.py
import asyncio
import json
from .api.schemas import ChatRequest
from .llm_utils import analyze_query_intent, get_english_from_data
from .db import execute_query
from .logger import get_logger

logger = get_logger(__name__)

class ChatService:
    def __init__(self):
        self.task_handlers = {
            "data_query": self._handle_data_query,
            "generate_visualization": self._handle_visualization,
            "conversation": self._handle_conversation,
        }

    async def generate_streaming_response(self, request: ChatRequest):
        """
        Main entry point for generating responses.
        This function now uses a single, unified loop to process all tasks correctly.
        """
        logger.info(f"Processing query: {request.query}")
        
        try:
            yield 'data: {"type": "status", "message": "Analyzing your query..."}\n\n'
            
            nlu_result = analyze_query_intent(request.query)
            tasks = nlu_result.get("tasks", [])

            if not tasks:
                error_payload = {"type": "final_text", "content": "I couldn't understand that. Please rephrase."}
                yield f"data: {json.dumps(error_payload)}\n\n"
                return

            task_context = {'all_tasks': tasks}

            # --- SIMPLIFIED AND CORRECTED MAIN LOOP ---
            for task in tasks:
                task_name = task.get("name", "unknown")
                handler = self.task_handlers.get(task_name)
                
                if handler:
                    # The handler will yield dictionaries. This loop formats them.
                    async for chunk in handler(request, task, task_context):
                        yield f"data: {json.dumps(chunk)}\n\n"

        except Exception as e:
            logger.error(f"Error in streaming pipeline: {str(e)}", exc_info=True)
            error_payload = {"type": "error", "text": "A critical error occurred.", "errorDetails": str(e)}
            yield f"data: {json.dumps(error_payload)}\n\n"
        finally:
            # Always send an End-Of-Stream message so the frontend knows when to stop.
            yield 'data: {"type": "eos"}\n\n'

    async def _handle_conversation(self, request: ChatRequest, task: dict, task_context: dict):
        logger.info("Executing task: conversation")
        response = task.get("response", "Please ask me about groundwater data.")
        yield {"type": "final_text", "content": response}

    async def _handle_data_query(self, request: ChatRequest, task: dict, task_context: dict):
        """Handles text-only database queries."""
        logger.info("Executing task: data_query")
        
        # Check if a visualization is planned. If so, this task should be skipped.
        if any(t.get("name") == "generate_visualization" for t in task_context['all_tasks']):
            logger.info("Skipping redundant data_query task because a visualization is planned.")
            return

        query_json = task.get('query')
        if not query_json:
            yield {"type": "final_text", "content": "Query parameters were missing."}
            return

        yield {"type": "status", "message": "Fetching groundwater data..."}
        filters = query_json.get('filters', {})
        fields = query_json.get('fields', [])
        db_results = execute_query(fields, filters)
        
        yield {"type": "status", "message": "Preparing your summary..."}
        response_text = get_english_from_data(request.query, db_results, fields)
        yield {"type": "final_text", "content": response_text}

    async def _handle_visualization(self, request: ChatRequest, task: dict, task_context: dict):
        """Unified handler for visualizations. Fetches its own data."""
        logger.info("Executing task: generate_visualization")
        chart_type = task.get("chart_type")
        field = task.get("field")

        data_query_task = next((t for t in task_context['all_tasks'] if t.get('name') == 'data_query'), None)
        
        if not all([chart_type, field, data_query_task]):
            yield {"type": "final_text", "content": "I understood you want a chart, but some details are missing."}
            return

        yield {"type": "status", "message": f"Fetching data for your {chart_type} chart..."}
        
        query_json = data_query_task.get('query')
        filters = query_json.get('filters', {})
        fields = query_json.get('fields', [])
        
        # --- CRITICAL FIX ---
        # Ensure the field to be visualized is always added to the query fields.
        if field not in fields:
            fields.append(field)
        # --- END OF FIX ---
        
        db_results = execute_query(fields, filters)
        
        if not db_results:
            yield {"type": "final_text", "content": f"I couldn't find any data to create a {chart_type} chart."}
            return

        yield {"type": "status", "message": f"Generating your {chart_type} chart..."}
        
        if chart_type == 'bar':
            labels = [item.get('DISTRICT', 'Unknown') for item in db_results]
            values = [float(item.get(field, 0)) for item in db_results]
            chart_data = {"labels": labels, "values": values}
            title = f"{field} for districts matching '{filters.get('district', 'your query')}'"

            payload = {
                "type": "visualization",
                "data": { "visualType": "bar", "title": title, "chartData": chart_data }
            }
            yield payload