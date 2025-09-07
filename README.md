# INGRES AI Chatbot API

A FastAPI-based backend for the INGRES AI Chatbot, designed to serve as a virtual assistant with AI-driven responses and integration with external APIs.

## Features

- **FastAPI** backend for high performance and easy API development
- Environment-based configuration using `.env`
- Modular structure for endpoints, services, and schemas
- Easily extendable for new AI models or integrations

## Project Structure

```
ingres-chatbot-api/
├── .env
├── .gitignore
├── README.md
├── requirements.txt
├── app/
│ ├── api/
│ │ ├── endpoints.py # API endpoints (routers)
│ │ └── schemas.py # Pydantic models for request/response
│ ├── services.py # Business logic (AI, DB calls)
│ ├── config.py # Configuration management
│ └── main.py # Main FastAPI app instance
└── tests/
└── test_services.py # Unit tests for the service layer
```

## Getting Started

### 1. Clone the repository

```sh
git clone https://github.com/KeshKunal/INGRES-Chatbot-API
cd "Chatbot API"
```

### 2. Create and activate a virtual environment (recommended)

```sh
python -m venv venv
venv\Scripts\activate  # On Windows
```

### 3. Install dependencies

```sh
pip install -r requirements.txt
```

### 4. Configure environment variables

Edit the `.env` file and add your API keys:

```
APP_NAME="INGRES AI Chatbot"
APP_VERSION="0.1.0"
LLM_API_KEY="your-llm-api-key-here"
BHASHINI_API_KEY="your-bhashini-api-key-here"
```

### 5. Run the API server

```sh
uvicorn app.main:app --reload
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `POST /api/v1/chat` - Process a chat request (see `app/api/endpoints.py`)

## Development

- Code is organized using FastAPI best practices.
- Add new endpoints in `app/api/endpoints.py`.
- Add business logic in `app/services/`.
- Define request/response models in `app/schemas.py`.

## License

This project is for internal use and prototyping. Add your license