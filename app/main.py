from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- IMPORT THIS
from .config import settings
from .api import endpoints

# Create the FastAPI app instance
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-driven ChatBOT for INGRES as a virtual assistant"
)

# --- ADD THIS MIDDLEWARE BLOCK ---
# This is the crucial part that will fix the CORS issue.

# Define the list of origins that are allowed to make requests.
# For development, this is just your React app's address.
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",  # Alternative localhost format
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow your frontend origin
    allow_credentials=True, # Allow cookies/authorization headers
    allow_methods=["*"],    # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],    # Allow all headers
)
# --- END OF MIDDLEWARE BLOCK ---

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