from fastapi import APIRouter
from starlette.responses import StreamingResponse  # Import StreamingResponse
from .schemas import ChatRequest  # We no longer use ChatResponse here
from ..services import ChatService

router = APIRouter()

@router.post("/chat", tags=["Chat"])
async def process_chat_stream(request: ChatRequest):  # Renamed for clarity
    """
    Receives a user query and streams back an AI-generated response.
    """
    chat_service = ChatService()
    return StreamingResponse(
        chat_service.generate_streaming_response(request), 
        media_type="text/event-stream"
    )