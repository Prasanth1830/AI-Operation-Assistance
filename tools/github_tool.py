"""GitHub API tool"""
import logging
from typing import Any, Dict, List

import requests

from config import Config
from .base import BaseTool

logger = logging.getLogger(__name__)


class GitHubTool(BaseTool):
    """Tool for interacting with GitHub API"""
    
    def __init__(self):
        """Initialize GitHub tool"""
        self.token = Config.GITHUB_TOKEN
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    @property
    def name(self) -> str:
        """Tool name"""
        return "github_search_repos"
    
    @property
    def description(self) -> str:
        """Tool description"""
        return "Search GitHub repositories by query and get detailed information"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        """Tool parameters schema"""
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query (e.g., 'language:python stars:>1000')"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results (default: 10)",
                    "default": 10
                }
            },
            "required": ["query"]
        }
    
    def execute(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """
        Search GitHub repositories
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            Search results with repository information
        """
        try:
            url = f"{self.base_url}/search/repositories"
            params = {
                "q": query,
                "sort": "stars",
                "order": "desc",
                "per_page": min(max_results, 100)
            }
            
            response = requests.get(
                url,
                params=params,
                headers=self.headers,
                timeout=Config.TIMEOUT
            )
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for repo in data.get("items", [])[:max_results]:
                results.append({
                    "name": repo["name"],
                    "url": repo["html_url"],
                    "description": repo["description"],
                    "stars": repo["stargazers_count"],
                    "language": repo["language"],
                    "owner": repo["owner"]["login"],
                    "forks": repo["forks_count"],
                    "updated_at": repo["updated_at"]
                })
            
            return {
                "status": "success",
                "query": query,
                "count": len(results),
                "results": results
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"GitHub API error: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "query": query
            }
    
    def get_user_info(self, username: str) -> Dict[str, Any]:
        """
        Get GitHub user information
        
        Args:
            username: GitHub username
            
        Returns:
            User information
        """
        try:
            url = f"{self.base_url}/users/{username}"
            response = requests.get(
                url,
                headers=self.headers,
                timeout=Config.TIMEOUT
            )
            response.raise_for_status()
            
            data = response.json()
            return {
                "status": "success",
                "user": {
                    "login": data["login"],
                    "name": data["name"],
                    "bio": data["bio"],
                    "public_repos": data["public_repos"],
                    "followers": data["followers"],
                    "following": data["following"],
                    "url": data["html_url"]
                }
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"GitHub API error: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "username": username
            }
