from fastapi import APIRouter
from .schemas import ChatRequest, ChatResponse
from ..services import ChatService

# Create a new router object
router = APIRouter()

@router.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def process_chat(request: ChatRequest) -> ChatResponse:
    """
    Receives a user query and returns an AI-generated response
    by calling the ChatService.
    """
    chat_service = ChatService()
    result = chat_service.generate_response(request)
    return ChatResponse(
        session_id=request.session_id,
        response_text=result["response_text"],
        visualization_data=result["visualization_data"],
        map_data=result["map_data"],
    )