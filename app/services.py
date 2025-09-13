# app/services.py
from .api.schemas import ChatRequest
from .config import settings
from .llm_utils import get_json_from_query, get_english_from_data
from .db import execute_query
from .logger import get_logger

# Setup basic logging
logger = get_logger(__name__)


class ChatService:
    def generate_response(self, request: ChatRequest) -> dict:
        """Main entry point for generating responses"""
        return self.process_request(request)

    def process_request(self, request):
        """Process a chat request through the full pipeline"""
        logger.info(f"Processing query: {request.query}")
        
        try:
            # Step 1: Convert natural language to structured query
            query_json = get_json_from_query(request.query)
            
            # Debug line to see the exact JSON produced by the LLM
            logger.info(f"DEBUG: The LLM produced this JSON -> {query_json}")
            
            if not query_json:
                raise ValueError("Could not understand the query.")
            
            logger.info(f"Generated query JSON: {query_json}")
            
            # Step 2: Execute database query with filters
            filters = query_json.get('filters', {}) if query_json is not None else {}
            db_results = execute_query(filters)
            logger.info(f"Database returned {len(db_results)} results")
            
            # Step 3: Generate natural language response
            response_text = get_english_from_data(request.query, db_results)
            
            # Step 4: Prepare visualization data if requested
            viz_data = {}
            if request.include_visualization:
                viz_data = self._prepare_visualization(db_results)
                
            return {
                "response_text": response_text,
                "visualization_data": viz_data,
                "map_data": self._prepare_map_data(db_results) if db_results else {},
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {
                "response_text": f"I'm sorry, I couldn't process that request. Error: {str(e)}",
                "visualization_data": {},
                "map_data": {},
            }

    def _prepare_visualization(self, data):
        """Convert DB results to visualization-ready format"""
        # Logic to transform data for charts
        return {}

    def _prepare_map_data(self, data):
        """Extract geospatial data for maps"""
        # Logic to extract coordinates and values for map
        return {}