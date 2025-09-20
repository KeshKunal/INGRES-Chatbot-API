# app/services.py
import asyncio
import json
from .api.schemas import ChatRequest
from .llm_utils import get_json_from_query, get_english_from_data
from .db import execute_query
from .logger import get_logger

logger = get_logger(__name__)

class ChatService:
    async def generate_streaming_response(self, request: ChatRequest):
        """
        Main entry point for generating responses as an asynchronous stream.
        """
        logger.info(f"Processing query: {request.query}")
        
        try:
            # Send status updates that won't be included in final response
            yield "data: {\"type\": \"status\", \"message\": \"Analyzing your query with AI intelligence...\"}\n\n"
            await asyncio.sleep(0.3)

            # --- Step 2: Convert natural language to structured query ---
            query_json = get_json_from_query(request.query)
            logger.info(f"Generated query JSON: {query_json}")
            
            yield "data: {\"type\": \"status\", \"message\": \"Fetching groundwater data from database...\"}\n\n"
            await asyncio.sleep(0.2)
            
            # Step 2: Execute database query with filters
            filters = query_json.get('filters', {}) if query_json else {}
            db_results = execute_query(filters)
            logger.info(f"Database returned {len(db_results)} results")
            
            yield "data: {\"type\": \"status\", \"message\": \"Preparing comprehensive response...\"}\n\n"
            await asyncio.sleep(0.2)
            
            # Step 3: Generate natural language response
            response_text = get_english_from_data(request.query, db_results)
            
            # Send the complete response at once (clean, without processing messages)
            yield response_text

        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            error_payload = {
                "type": "error",
                "text": "I'm sorry, an error occurred while processing your request.",
                "errorDetails": str(e)
            }
            yield f"data: {json.dumps(error_payload)}\n\n"

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