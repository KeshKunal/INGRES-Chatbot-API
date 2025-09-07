from pydantic import BaseModel
from typing import Optional, Dict, Any

class ChatRequest(BaseModel):
    """
    Defines the structure of a request to the /chat endpoint.
    """
    session_id: str
    query: str
    language: Optional[str] = "en"

class ChatResponse(BaseModel):
    """
    Defines the response from the /chat endpoint, matching your project plan.
    """
    session_id: str
    response_text: str
    visualization_data: Optional[Dict[str, Any]] = None
    map_data: Optional[Dict[str, Any]] = None