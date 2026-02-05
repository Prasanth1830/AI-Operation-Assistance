"""Executor Agent - executes planned steps and calls tools"""
import logging
from typing import Any, Dict, List

from tools import GitHubTool, WeatherTool
from .base import BaseAgent

logger = logging.getLogger(__name__)


class ExecutorAgent(BaseAgent):
    """Agent that executes steps and calls tools"""
    
    def __init__(self):
        """Initialize Executor Agent"""
        super().__init__("executor")
        self.tools = {
            "github_search_repos": GitHubTool(),
            "get_weather": WeatherTool(),
        }
    
    def execute(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the plan steps
        
        Args:
            plan: Plan from Planner Agent
            
        Returns:
            Execution results with step outcomes
        """
        self.logger.info(f"Executing plan: {plan.get('objective', 'unknown')}")
        
        results = []
        execution_context = {}
        
        for step in plan.get("steps", []):
            step_result = self._execute_step(step, execution_context)
            results.append(step_result)
            
            # Store result for context in next steps
            step_num = step.get("step_number", len(results))
            execution_context[f"step_{step_num}"] = step_result
        
        return {
            "status": "success",
            "steps_executed": len(results),
            "results": results,
            "execution_context": execution_context
        }
    
    def _execute_step(self, step: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a single step
        
        Args:
            step: Step to execute
            context: Execution context from previous steps
            
        Returns:
            Step execution result
        """
        step_num = step.get("step_number", "unknown")
        tool_name = step.get("tool", "none")
        
        self.logger.info(f"Executing step {step_num}: {step.get('description', 'unknown')}")
        
        if tool_name == "none":
            return {
                "step_number": step_num,
                "status": "skipped",
                "description": step.get("description"),
                "reason": "No tool required"
            }
        
        if tool_name not in self.tools:
            return {
                "step_number": step_num,
                "status": "error",
                "error": f"Unknown tool: {tool_name}",
                "description": step.get("description")
            }
        
        try:
            tool = self.tools[tool_name]
            params = step.get("params", {})
            
            self.logger.debug(f"Calling tool {tool_name} with params: {params}")
            result = tool.execute(**params)
            
            return {
                "step_number": step_num,
                "status": "completed",
                "description": step.get("description"),
                "tool": tool_name,
                "params": params,
                "result": result
            }
        except Exception as e:
            self.logger.error(f"Error executing step {step_num}: {str(e)}")
            return {
                "step_number": step_num,
                "status": "failed",
                "description": step.get("description"),
                "tool": tool_name,
                "error": str(e)
            }
