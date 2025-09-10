from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .api.schemas import ChatRequest, ChatResponse
from .services import ChatService
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="INGRES Chatbot API",
    description="AI-powered chatbot for Indian groundwater and rainfall data",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the chat service
chat_service = ChatService()

@app.get("/")
def read_root():
    """Root endpoint - API status check"""
    return {
        "message": "INGRES Chatbot API is running!",
        "status": "active",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "chatbot",
        "database": "mock_connected",
        "llm": "sarvam_ai_ready"
    }

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """
    Main chatbot endpoint implementing the complete flow:
    1. User sends prompt
    2. Convert to SQL query using Sarvam AI
    3. Execute SQL query on database
    4. Convert results to natural language using Sarvam AI
    5. Return response with optional visualizations
    """
    try:
        logger.info(f"Received chat request: {request.query[:50]}...")
        
        # Generate response using the chat service
        result = chat_service.generate_response(request)
        
        # Create response object
        response = ChatResponse(
            session_id=request.session_id,
            response_text=result["response_text"],
            visualization_data=result.get("visualization_data"),
            map_data=result.get("map_data"),
            language=request.language or "en"
        )
        
        logger.info("Response generated successfully")
        return response
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )

# Test endpoints for debugging
@app.get("/test/mock-data")
def get_mock_data():
    """Get mock database data for testing"""
    return {
        "groundwater_data": chat_service.mock_data["groundwater_data"],
        "rainfall_data": chat_service.mock_data["rainfall_data"]
    }

@app.get("/test/schema")
def get_database_schema():
    """Get database schema for reference"""
    return {
        "schema": chat_service.database_schema
    }

@app.post("/test/sql-only")
def test_sql_generation(request: ChatRequest):
    """Test only the SQL generation part"""
    try:
        sql_messages = [
            {
                "role": "system",
                "content": "You are a SQL expert. Convert natural language to PostgreSQL queries. Return ONLY the SQL query."
            },
            {
                "role": "user",
                "content": f"""
                Database Schema:
                {chat_service.database_schema}
                
                User Question: {request.query}
                
                Convert to PostgreSQL query.
                """
            }
        ]
        
        sql_query = chat_service.call_sarvam_ai(sql_messages)
        mock_results = chat_service.execute_mock_sql(sql_query)
        
        return {
            "original_query": request.query,
            "generated_sql": sql_query,
            "mock_results_count": len(mock_results),
            "mock_results": mock_results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)