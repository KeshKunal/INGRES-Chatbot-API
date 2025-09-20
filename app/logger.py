import logging
import sys
import time
from typing import Dict, Any, Optional
from datetime import datetime
from .config import settings

class INGRESLogger:
    """Custom logger for INGRES Chatbot with structured logging"""

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))

        if not self.logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))

            # Formatter
            formatter = logging.Formatter(settings.LOG_FORMAT)
            console_handler.setFormatter(formatter)

            self.logger.addHandler(console_handler)

    def log_api_request(self, session_id: str, query: str, language: str = "en") -> None:
        """Log API request details"""
        # Truncate long queries for log readability
        truncated_query = f"{query[:100]}..." if len(query) > 100 else query
        self.logger.info(
            f"API_REQUEST | Session: {session_id} | Query: {truncated_query} | Language: {language}"
        )

    def log_api_response(self, session_id: str, response_time: float, success: bool) -> None:
        """Log API response details"""
        status = "SUCCESS" if success else "ERROR"
        self.logger.info(
            f"API_RESPONSE | Session: {session_id} | Time: {response_time:.3f}s | Status: {status}"
        )

    def log_database_operation(self, operation: str, execution_time: float, success: bool) -> None:
        """Log database operation"""
        status = "SUCCESS" if success else "ERROR"
        self.logger.info(
            f"DB_OPERATION | {operation} | Time: {execution_time:.3f}s | Status: {status}"
        )

    def log_llm_operation(self, operation: str, execution_time: float, success: bool) -> None:
        """Log LLM operation"""
        status = "SUCCESS" if success else "ERROR"
        self.logger.info(
            f"LLM_OPERATION | {operation} | Time: {execution_time:.3f}s | Status: {status}"
        )

    def log_error(self, error_type: str, error_message: str, session_id: Optional[str] = None) -> None:
        """Log structured error information"""
        session_info = f"Session: {session_id} | " if session_id else ""
        self.logger.error(f"ERROR | {session_info}Type: {error_type} | Message: {error_message}")

    def info(self, message: str) -> None:
        self.logger.info(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def start_timer(self) -> float:
        """Start a timer for performance logging"""
        return time.time()

    def end_timer(self, start_time: float) -> float:
        """End a timer and return elapsed time in seconds"""
        return time.time() - start_time

def get_logger(name: str = __name__) -> INGRESLogger:
    return INGRESLogger(name)