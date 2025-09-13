from fastapi import FastAPI
from .config import settings
from .api import endpoints
from .middleware import request_logging_middleware, error_handling_middleware, rate_limit_middleware

# Create the FastAPI app instance
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-driven ChatBOT for INGRES as a virtual assistant"
)

# Add middleware for logging, error handling, and rate limiting
app.middleware("http")(request_logging_middleware)
app.middleware("http")(error_handling_middleware)
app.middleware("http")(rate_limit_middleware)

# Include the router from the endpoints module
app.include_router(endpoints.router, prefix="/api/v1")

@app.get("/", tags=["Root"])
def read_root():
    """
    A welcome message for the API root.
    """
    return {"message": f"Welcome to the {settings.APP_NAME}!"}

@app.get("/health", tags=["Health Check"])
def health_check():
    """
    A simple health check endpoint to confirm the API is running.
    """
    return {"status": "ok", "version": settings.APP_VERSION}