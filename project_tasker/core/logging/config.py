import logging
import sys
from typing import List
from pydantic import AnyHttpUrl, BaseSettings

class LoggingSettings(BaseSettings):
    LOGGING_LEVEL: int = logging.INFO
    LOGGING_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOGGING_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"

    class Config:
        case_sensitive = True

def setup_logging():
    """Configure logging for the application."""
    logging_settings = LoggingSettings()
    
    # Configure root logger
    logging.basicConfig(
        level=logging_settings.LOGGING_LEVEL,
        format=logging_settings.LOGGING_FORMAT,
        datefmt=logging_settings.LOGGING_DATE_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("project_tasker.log")
        ]
    )
    
    # Set levels for external libraries
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("alembic").setLevel(logging.WARNING)
    
    # Create logger for our application
    logger = logging.getLogger("project_tasker")
    logger.setLevel(logging_settings.LOGGING_LEVEL)
    
    return logger

# Create and export logger instance
logger = setup_logging()
