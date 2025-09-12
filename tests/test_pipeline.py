import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.api.schemas import ChatRequest
from app.services import ChatService

# Create a test request
test_request = ChatRequest(
    session_id="test-session-123",
    query="What was the groundwater level in Chennai in 2022?",
    include_visualization=True,
    language="en",
    context=""
)

# Create service instance
chat_service = ChatService()

# Test the full pipeline
try:
    result = chat_service.generate_response(test_request)
    print("\n--- TEST RESULTS ---")
    print(f"Query: {test_request.query}")
    print(f"Response: {result['response_text']}")
    print(f"Visualization data available: {'Yes' if result['visualization_data'] else 'No'}")
    print(f"Map data available: {'Yes' if result['map_data'] else 'No'}")
except Exception as e:
    print(f"Error testing pipeline: {str(e)}")