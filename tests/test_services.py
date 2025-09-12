import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.services import ChatService
from app.api.schemas import ChatRequest

def test_generate_basic_response():
    """
    Tests that the ChatService returns a valid response for a simple query.
    """
    # Arrange
    service = ChatService()
    request = ChatRequest(session_id="123", query="hello")

    # Act
    result = service.generate_response(request)

    # Assert
    assert isinstance(result, dict)
    assert "response_text" in result
    assert "Service layer response" in result["response_text"]
    assert result["visualization_data"] is None

def test_generate_chart_response():
    """
    Tests that the ChatService returns visualization data when a chart is requested.
    """
    # Arrange
    service = ChatService()
    request = ChatRequest(session_id="456", query="show me a chart")

    # Act
    result = service.generate_response(request)

    # Assert
    assert isinstance(result, dict)
    assert result["visualization_data"] is not None
    assert result["visualization_data"]["type"] == "bar"