"""
Configuration module for AI Operations Assistant
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    
    # LLM Configuration
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
    
    # API Keys
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
    
    # Server Configuration
    SERVER_HOST = os.getenv("SERVER_HOST", "127.0.0.1")
    SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Agent Configuration
    MAX_RETRIES = 3
    TIMEOUT = 30
    
    @staticmethod
    def validate():
        """Validate required configuration"""
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY must be set in .env file")
        if not Config.GITHUB_TOKEN:
            raise ValueError("GITHUB_TOKEN must be set in .env file")
        if not Config.WEATHER_API_KEY:
            raise ValueError("WEATHER_API_KEY must be set in .env file")
