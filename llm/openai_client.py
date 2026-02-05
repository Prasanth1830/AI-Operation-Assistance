"""OpenAI client implementation"""
import json
import logging
from typing import Any, Dict, List, Optional

from openai import OpenAI

from config import Config
from .base import BaseLLMClient

logger = logging.getLogger(__name__)


class OpenAIClient(BaseLLMClient):
    """OpenAI LLM client"""
    
    def __init__(self):
        """Initialize OpenAI client"""
        self.api_key = Config.OPENAI_API_KEY
        self.model = Config.OPENAI_MODEL
        self.client = OpenAI(api_key=self.api_key)
    
    def create_message(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Create a message using OpenAI API
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            
        Returns:
            Response text from the LLM
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens or 2000,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error creating message with OpenAI: {str(e)}")
            raise
    
    def create_message_json(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Create a structured JSON message using OpenAI API
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            
        Returns:
            Parsed JSON response from the LLM
        """
        try:
            # Add instruction to return JSON
            messages_with_json = messages.copy()
            if messages_with_json[-1]["role"] == "user":
                messages_with_json[-1]["content"] += "\n\nRespond with valid JSON only."
            
            response_text = self.create_message(messages_with_json, temperature, max_tokens)
            
            # Extract JSON from response
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                # Try to extract JSON if it's embedded in text
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                raise ValueError(f"Could not parse JSON from response: {response_text}")
        except Exception as e:
            logger.error(f"Error creating JSON message with OpenAI: {str(e)}")
            raise
