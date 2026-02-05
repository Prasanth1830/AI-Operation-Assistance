"""Planner Agent - converts user input into structured plan"""
import json
import logging
import re
from typing import Any, Dict, List

from llm import OpenAIClient
from .base import BaseAgent

logger = logging.getLogger(__name__)


class PlannerAgent(BaseAgent):
    """Agent that plans steps for executing a user task"""
    
    def __init__(self):
        """Initialize Planner Agent"""
        super().__init__("planner")
        try:
            self.llm = OpenAIClient()
            self.llm_available = True
        except Exception as e:
            logger.warning(f"LLM not available, using fallback planner: {e}")
            self.llm_available = False
    
    def execute(self, user_task: str) -> Dict[str, Any]:
        """
        Convert user task into a structured plan
        
        Args:
            user_task: Natural language task from user
            
        Returns:
            Structured plan with steps and required tools
        """
        self.logger.info(f"Planning task: {user_task}")
        
        # Try LLM first, fall back to rule-based planning
        if self.llm_available:
            try:
                return self._llm_based_planning(user_task)
            except Exception as e:
                self.logger.warning(f"LLM planning failed: {e}, using fallback")
                return self._rule_based_planning(user_task)
        else:
            return self._rule_based_planning(user_task)
    
    def _llm_based_planning(self, user_task: str) -> Dict[str, Any]:
        """Use LLM for intelligent planning"""
        plan_prompt = self._create_plan_prompt(user_task)
        messages = [
            {
                "role": "system",
                "content": "You are an AI planning agent. Your task is to break down user requests into concrete, actionable steps with required tools."
            },
            {
                "role": "user",
                "content": plan_prompt
            }
        ]
        
        try:
            plan_json = self.llm.create_message_json(messages, temperature=0.3)
            plan = self._validate_plan(plan_json)
            self.logger.info(f"Generated LLM plan with {len(plan['steps'])} steps")
            return {"status": "success", "plan": plan}
        except Exception as e:
            self.logger.error(f"Error in LLM planner: {str(e)}")
            raise
    
    def _rule_based_planning(self, user_task: str) -> Dict[str, Any]:
        """Fallback rule-based planning when LLM quota is exhausted"""
        self.logger.info("Using rule-based fallback planner")
        
        task_lower = user_task.lower()
        steps = []
        step_num = 1
        
        # Detect GitHub-related keywords
        if any(keyword in task_lower for keyword in ['github', 'repository', 'repo', 'python', 'javascript', 'java', 'go', 'rust', 'node', 'libraries', 'frameworks', 'repositories']):
            # Extract query from task
            query = self._extract_search_query(user_task)
            steps.append({
                "step_number": step_num,
                "description": f"Search GitHub for: {query}",
                "tool": "github_search_repos",
                "params": {"query": query, "max_results": 5},
                "expected_outcome": "List of matching repositories with stars and descriptions"
            })
            step_num += 1
        
        # Detect weather-related keywords
        cities = self._extract_cities(user_task)
        for city in cities:
            steps.append({
                "step_number": step_num,
                "description": f"Get current weather in {city}",
                "tool": "get_weather",
                "params": {"city": city, "units": "metric"},
                "expected_outcome": f"Current weather conditions for {city}"
            })
            step_num += 1
        
        # If no tools detected, add a generic info step
        if not steps:
            steps.append({
                "step_number": 1,
                "description": "Analyze task and provide information",
                "tool": "none",
                "params": {},
                "expected_outcome": "Task analysis and recommendations"
            })
        
        plan = {
            "task": user_task,
            "objective": f"Complete: {user_task}",
            "steps": steps,
            "success_criteria": "All steps executed successfully"
        }
        
        self.logger.info(f"Generated rule-based plan with {len(plan['steps'])} steps")
        return {"status": "success", "plan": plan}
    
    def _extract_search_query(self, task: str) -> str:
        """Extract search query from task description"""
        # Try to find specific language or topic mentions
        keywords = ['python', 'javascript', 'java', 'go', 'rust', 'typescript', 'c++', 'php', 'ruby']
        for keyword in keywords:
            if keyword in task.lower():
                # Extract more context around the keyword
                if 'framework' in task.lower():
                    return f"language:{keyword} topic:framework"
                elif 'library' in task.lower() or 'library' in task.lower():
                    return f"language:{keyword} topic:library"
                else:
                    return f"language:{keyword} stars:>1000"
        
        # Default general search
        return "stars:>10000 sort:stars"
    
    def _extract_cities(self, task: str) -> List[str]:
        """Extract city names from task description"""
        common_cities = [
            'london', 'paris', 'tokyo', 'new york', 'san francisco',
            'berlin', 'sydney', 'toronto', 'dubai', 'singapore',
            'mumbai', 'moscow', 'bangkok', 'bangkok', 'los angeles',
            'chicago', 'seattle', 'amsterdam', 'barcelona', 'madrid'
        ]
        
        cities_found = []
        task_lower = task.lower()
        
        for city in common_cities:
            if city in task_lower:
                cities_found.append(city.title())
        
        return cities_found
    
    def _create_plan_prompt(self, user_task: str) -> str:
        """
        Create the planning prompt
        
        Args:
            user_task: User's task
            
        Returns:
            Formatted prompt for the LLM
        """
        return f"""
Task: {user_task}

Available tools:
1. github_search_repos - Search GitHub repositories by query
2. get_weather - Get current weather information for a city
3. none - For informational tasks that don't need external tools

Please create a JSON plan with the following structure:
{{
    "task": "Original task",
    "objective": "Clear objective",
    "steps": [
        {{
            "step_number": 1,
            "description": "What to do",
            "tool": "Tool name or 'none'",
            "params": {{"param1": "value1"}},
            "expected_outcome": "What we expect"
        }}
    ],
    "success_criteria": "How to know if successful"
}}

Only return valid JSON, no other text.
"""
    
    def _validate_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the plan structure
        
        Args:
            plan: Plan to validate
            
        Returns:
            Validated plan
        """
        required_fields = ["task", "objective", "steps", "success_criteria"]
        
        for field in required_fields:
            if field not in plan:
                raise ValueError(f"Missing required field in plan: {field}")
        
        if not isinstance(plan["steps"], list) or len(plan["steps"]) == 0:
            raise ValueError("Plan must have at least one step")
        
        return plan
