from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime

class ChatRequest(BaseModel):
    """
    Defines the structure of a request to the /chat endpoint.
    """
    session_id: str = Field(..., min_length=1, max_length=100, description="Unique session identifier")
    query: str = Field(..., min_length=1, max_length=1000, description="User query")
    language: Optional[str] = Field("en", pattern="^[a-z]{2}$", description="Language code (ISO 639-1)")
    include_visualization: Optional[bool] = Field(False, description="Request data visualization")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context for the query")

    @validator('query')
    def validate_query(cls, v):
        """Validate query for basic security"""
        dangerous_patterns = ['drop', 'delete', 'update', 'insert', 'alter', 'create', 'truncate']
        v_lower = v.lower()
        for pattern in dangerous_patterns:
            if pattern in v_lower:
                raise ValueError(f"Query contains potentially harmful operation: {pattern}")
        return v

class ChatResponse(BaseModel):
    """
    Defines the response from the /chat endpoint.
    """
    session_id: str
    response_text: str
    language: str = "en" 
    visualization_data: Optional[Dict[str, Any]] = None
    map_data: Optional[Dict[str, Any]] = None
    suggestions: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    success: bool = True

class ErrorResponse(BaseModel):
    """
    Standard error response format
    """
    error: str
    message: str
    success: bool = False
    timestamp: datetime = Field(default_factory=datetime.now)
    session_id: Optional[str] = None

class HealthResponse(BaseModel):
    """
    Health check response
    """
    status: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.now)
    services: Optional[Dict[str, str]] = None

class QueryIntentResponse(BaseModel):
    """
    Response from query intent analysis
    """
    intent: str
    entities: List[Dict[str, Any]]
    confidence: float
    requires_visualization: bool
    suggested_queries: Optional[List[str]] = None