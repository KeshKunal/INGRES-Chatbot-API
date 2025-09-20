# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List

class Settings(BaseSettings):
    # To load variables from the .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # App Configuration
    APP_NAME: str = "INGRES AI Chatbot"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # Logging
    LOG_LEVEL: str = "INFO"  
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # API Keys
    LLM_API_KEY: str
    BHASHINI_API_KEY: str
    SARVAM_API_KEY: str

    # Database Configuration
    db_user: str = "user"
    db_password: str = "password"
    db_host: str = "localhost"
    db_port: str = "5432"
    db_name: str = "ingres_db"
    DATABASE_URL: Optional[str] = None
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    @property
    def get_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}?sslmode=require"

    # Security
    API_RATE_LIMIT: str = "100/minute"
    MAX_QUERY_LENGTH: int = 1000
    ALLOWED_SQL_OPERATIONS: Optional[List[str]] = ["SELECT", "INSERT", "UPDATE", "DELETE"]

# Create a single instance of the settings
settings = Settings()