from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import time
from typing import Dict, Any, Callable
from .config import settings
from .logger import get_logger
from .exceptions import rate_limit_exception
from datetime import datetime

logger = get_logger(__name__)

class RateLimitMiddleware:
    """Simple in-memory rate limiting middleware"""

    def __init__(self):
        self.request_counts: Dict[str, Dict[str, Any]] = {}
        # Get values from settings if available, otherwise use defaults
        self.window_size = getattr(settings, 'RATE_LIMIT_WINDOW', 60)  # 1 minute window
        self.max_requests = int(settings.API_RATE_LIMIT.split('/')[0]) if hasattr(settings, 'API_RATE_LIMIT') else 100

    def is_rate_limited(self, client_ip: str) -> bool:
        """Check if client has exceeded rate limit"""
        current_time = time.time()

        if client_ip not in self.request_counts:
            self.request_counts[client_ip] = {
                "count": 0,
                "window_start": current_time
            }

        client_data = self.request_counts[client_ip]

        # Reset window if expired
        if current_time - client_data["window_start"] > self.window_size:
            client_data["count"] = 0
            client_data["window_start"] = current_time

        # Check limit
        if client_data["count"] >= self.max_requests:
            return True

        # Increment count
        client_data["count"] += 1
        return False

    def cleanup_old_entries(self, max_age: int = 3600) -> None:
        """Clean up old entries to prevent memory leaks"""
        current_time = time.time()
        to_delete = []
        
        for ip, data in self.request_counts.items():
            if current_time - data["window_start"] > max_age:
                to_delete.append(ip)
                
        for ip in to_delete:
            del self.request_counts[ip]


rate_limiter = RateLimitMiddleware()

async def rate_limit_middleware(request: Request, call_next: Callable) -> JSONResponse:
    """Rate limiting middleware"""
    client_ip = request.client.host if request.client else "unknown"

    # Skip rate limiting for certain paths
    if request.url.path == "/health" or request.url.path == "/":
        return await call_next(request)

    if rate_limiter.is_rate_limited(client_ip):
        logger.log_error("RATE_LIMIT", f"Rate limit exceeded for IP: {client_ip}")
        raise rate_limit_exception()

    # Periodically clean up old entries (1% chance per request)
    if time.time() % 100 < 1:
        rate_limiter.cleanup_old_entries()

    response = await call_next(request)
    return response

async def request_logging_middleware(request: Request, call_next: Callable) -> JSONResponse:
    """Request/response logging middleware"""
    start_time = time.time()

    # Extract session ID from headers if available
    session_id = request.headers.get("X-Session-ID", "unknown")

    # Log request
    logger.info(f"Request: {request.method} {request.url} | Session: {session_id}")

    response = await call_next(request)

    # Log response
    process_time = time.time() - start_time
    logger.log_api_response(
        session_id=session_id,
        response_time=process_time,
        success=response.status_code < 400
    )

    response.headers["X-Process-Time"] = str(process_time)
    return response

async def error_handling_middleware(request: Request, call_next: Callable) -> JSONResponse:
    """Global error handling middleware"""
    try:
        response = await call_next(request)
        return response
    except HTTPException as he:
        logger.log_error("HTTP_EXCEPTION", f"{he.status_code}: {he.detail}")
        raise he
    except Exception as e:
        logger.log_error("SERVER_ERROR", str(e))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
                "success": False,
                "timestamp": datetime.now().isoformat(),
            }
        )