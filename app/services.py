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
            # --- Stream Step 1: Acknowledge and think ---
            yield "Analyzing your query... "
            await asyncio.sleep(0.5)

            # --- Step 2: Convert natural language to structured query ---
            query_json = get_json_from_query(request.query)
            logger.info(f"DEBUG: The LLM produced this JSON -> {query_json}")
            
            if not query_json:
                raise ValueError("Could not understand the query.")
            
            yield "Accessing database... "
            await asyncio.sleep(0.5)

            # --- Step 3: Execute REAL database query ---
            try:
                # Use the actual execute_query function from your db.py
                db_results = execute_query(query_json)
                logger.info(f"Database returned {len(db_results) if db_results else 0} results")
                
                if not db_results:
                    yield "No data found for your query. Please try a different location or check the spelling."
                    return
                    
            except Exception as db_error:
                logger.error(f"Database query failed: {str(db_error)}")
                yield f"Sorry, I encountered an error while accessing the database: {str(db_error)}"
                return

            # --- Step 4: Send structured data first (if needed) ---
            if request.include_visualization and db_results:
                viz_data = self._prepare_visualization(db_results, request.query)
                yield f"data: {json.dumps(viz_data)}\n\n"
                await asyncio.sleep(0.5)

            # --- Step 5: Generate and stream the final natural language response ---
            yield "Generating response... "
            await asyncio.sleep(0.5)
            
            # Use the real data for response generation
            response_text = get_english_from_data(request.query, db_results)
            
            # Stream word by word for a real-time effect
            for word in response_text.split():
                yield f"{word} "
                await asyncio.sleep(0.05)

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