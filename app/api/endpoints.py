from fastapi import APIRouter
from .schemas import ChatRequest, ChatResponse
from ..services import ChatService

# Create a new router object
router = APIRouter()

@router.post("/chat", response_model=ChatResponse, tags=["Chat"])
def process_chat(request: ChatRequest) -> ChatResponse:
    """
    Receives a user query and returns an AI-generated response
    by calling the ChatService.
    """
    # 1. Create an instance of the service
    chat_service = ChatService()

    # 2. Call the service to get the result
    result = chat_service.generate_response(request)

    # 3. Format the result into the API response model
    return ChatResponse(
        session_id=request.session_id,
        response_text=result["response_text"],
        visualization_data=result["visualization_data"],
        map_data=result["map_data"],
    )