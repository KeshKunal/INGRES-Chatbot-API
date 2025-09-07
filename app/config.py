# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # To load variables from the .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_NAME: str = "INGRES AI Chatbot"
    APP_VERSION: str = "0.1.0"
    LLM_API_KEY: str
    BHASHINI_API_KEY: str

# Create a single instance of the settings
settings = Settings()