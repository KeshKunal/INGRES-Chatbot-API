from fastapi import HTTPException, status
from typing import Optional

class INGRESChatbotException(Exception):
    """Base exception for INGRES Chatbot"""
    def __init__(self, message: str = "An error occurred in the INGRES Chatbot"):
        self.message = message
        super().__init__(self.message)

class DatabaseConnectionError(INGRESChatbotException):
    """Raised when database connection fails"""
    pass

class LLMServiceError(INGRESChatbotException):
    """Raised when LLM service encounters an error"""
    pass

class InvalidQueryError(INGRESChatbotException):
    """Raised when user query is invalid or potentially harmful"""
    pass

class TranslationServiceError(INGRESChatbotException):
    """Raised when translation service fails"""
    pass

class RateLimitExceededError(INGRESChatbotException):
    """Raised when API rate limit is exceeded"""
    pass

# HTTP Exception handlers
def create_http_exception(status_code: int, detail: str, error_type: str = "GENERAL_ERROR", headers: Optional[dict] = None):
    """Create standardized HTTP exception"""
    return HTTPException(
        status_code=status_code,
        detail={
            "error": error_type,
            "message": detail,
            "success": False
        },
        headers=headers
    )

# Common HTTP exceptions
def database_error_exception(detail: str = "Database operation failed"):
    return create_http_exception(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail=detail,
        error_type="DATABASE_ERROR"
    )

def llm_service_exception(detail: str = "AI service temporarily unavailable"):
    return create_http_exception(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail=detail,
        error_type="LLM_SERVICE_ERROR"
    )

def invalid_query_exception(detail: str = "Invalid or potentially harmful query"):
    return create_http_exception(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail,
        error_type="INVALID_QUERY"
    )

def rate_limit_exception(detail: str = "Rate limit exceeded"):
    return create_http_exception(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail=detail,
        error_type="RATE_LIMIT_EXCEEDED",
        headers={"Retry-After": "60"}  # Adds helpful retry header
    )