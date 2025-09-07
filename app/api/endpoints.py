# app/api/endpoints.py
from fastapi import APIRouter
from .schemas import ChatRequest, ChatResponse

# Create a new router object
router = APIRouter()

@router.post("/chat", response_model=ChatResponse, tags=["Chat"])
def process_chat(request: ChatRequest) -> ChatResponse:
    """
    Receives a user query and returns an AI-generated response.
    This is a placeholder and will be replaced by the real AI logic.
    """
    # Placeholder logic (Phase 4 will make this real)
    response_text = f"Placeholder response for query: '{request.query}'"
    
    # Returning a structured response that matches our Pydantic model
    return ChatResponse(
        session_id=request.session_id,
        response_text=response_text,
        visualization_data=None, # To be added later
        map_data=None            # To be added later
    )