"""Weather API tool"""
import logging
from typing import Any, Dict

import requests

from config import Config
from .base import BaseTool

logger = logging.getLogger(__name__)


class WeatherTool(BaseTool):
    """Tool for getting weather information"""
    
    def __init__(self):
        """Initialize Weather tool"""
        self.api_key = Config.WEATHER_API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    @property
    def name(self) -> str:
        """Tool name"""
        return "get_weather"
    
    @property
    def description(self) -> str:
        """Tool description"""
        return "Get current weather information for a city"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        """Tool parameters schema"""
        return {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name (e.g., 'London', 'New York')"
                },
                "units": {
                    "type": "string",
                    "description": "Temperature units (metric, imperial)",
                    "default": "metric"
                }
            },
            "required": ["city"]
        }
    
    def execute(self, city: str, units: str = "metric") -> Dict[str, Any]:
        """
        Get current weather for a city
        
        Args:
            city: City name
            units: Temperature units (metric or imperial)
            
        Returns:
            Weather information
        """
        try:
            url = f"{self.base_url}/weather"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": units
            }
            
            response = requests.get(
                url,
                params=params,
                timeout=Config.TIMEOUT
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "status": "success",
                "city": data["name"],
                "country": data["sys"]["country"],
                "weather": {
                    "description": data["weather"][0]["description"],
                    "temperature": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "pressure": data["main"]["pressure"],
                    "wind_speed": data["wind"]["speed"],
                    "cloudiness": data["clouds"]["all"]
                },
                "units": units
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Weather API error: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "city": city
            }
    
    def get_forecast(self, city: str, units: str = "metric") -> Dict[str, Any]:
        """
        Get weather forecast for a city
        
        Args:
            city: City name
            units: Temperature units
            
        Returns:
            Weather forecast
        """
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": units
            }
            
            response = requests.get(
                url,
                params=params,
                timeout=Config.TIMEOUT
            )
            response.raise_for_status()
            
            data = response.json()
            
            forecasts = []
            for item in data["list"][:8]:  # Next 24 hours
                forecasts.append({
                    "datetime": item["dt_txt"],
                    "temperature": item["main"]["temp"],
                    "description": item["weather"][0]["description"],
                    "humidity": item["main"]["humidity"],
                    "wind_speed": item["wind"]["speed"]
                })
            
            return {
                "status": "success",
                "city": data["city"]["name"],
                "country": data["city"]["country"],
                "forecasts": forecasts,
                "units": units
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Weather API error: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "city": city
            }
