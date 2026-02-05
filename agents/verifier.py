"""Verifier Agent - validates and fixes results"""
import json
import logging
from typing import Any, Dict

from llm import OpenAIClient
from .base import BaseAgent

logger = logging.getLogger(__name__)


class VerifierAgent(BaseAgent):
    """Agent that verifies and validates results"""
    
    def __init__(self):
        """Initialize Verifier Agent"""
        super().__init__("verifier")
        try:
            self.llm = OpenAIClient()
            self.llm_available = True
        except Exception as e:
            logger.warning(f"LLM not available for formatting: {e}")
            self.llm_available = False
    
    def execute(self, plan: Dict[str, Any], execution_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify and validate execution results
        
        Args:
            plan: Original plan
            execution_result: Result from Executor Agent
            
        Returns:
            Validated and formatted final result
        """
        self.logger.info("Verifying execution results")
        
        # Check completion
        completion_check = self._check_completion(plan, execution_result)
        
        if not completion_check["all_steps_completed"]:
            self.logger.warning("Not all steps were completed")
        
        # Format final answer
        final_answer = self._create_final_answer(plan, execution_result, completion_check)
        
        return {
            "status": "success" if completion_check["all_steps_completed"] else "partial",
            "completion_check": completion_check,
            "final_answer": final_answer
        }
    
    def _check_completion(self, plan: Dict[str, Any], execution_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if all steps were completed successfully
        
        Args:
            plan: Original plan
            execution_result: Execution results
            
        Returns:
            Completion status
        """
        expected_steps = len(plan.get("steps", []))
        executed_steps = len(execution_result.get("results", []))
        
        successful_steps = sum(
            1 for r in execution_result.get("results", [])
            if r.get("status") in ["completed", "skipped"]
        )
        
        all_completed = successful_steps == expected_steps
        
        return {
            "expected_steps": expected_steps,
            "executed_steps": executed_steps,
            "successful_steps": successful_steps,
            "all_steps_completed": all_completed
        }
    
    def _create_final_answer(
        self,
        plan: Dict[str, Any],
        execution_result: Dict[str, Any],
        completion_check: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a formatted final answer
        
        Args:
            plan: Original plan
            execution_result: Execution results
            completion_check: Completion status
            
        Returns:
            Formatted final answer
        """
        # Try LLM formatting, fall back to manual formatting
        if self.llm_available:
            try:
                return self._llm_format_answer(plan, execution_result, completion_check)
            except Exception as e:
                self.logger.warning(f"LLM formatting failed: {e}, using fallback")
                return self._manual_format_answer(plan, execution_result, completion_check)
        else:
            return self._manual_format_answer(plan, execution_result, completion_check)
    
    def _llm_format_answer(
        self,
        plan: Dict[str, Any],
        execution_result: Dict[str, Any],
        completion_check: Dict[str, Any]
    ) -> Dict[str, Any]:
        """LLM-based formatting"""
        format_prompt = self._create_format_prompt(plan, execution_result)
        messages = [
            {
                "role": "system",
                "content": "You are an expert at formatting and summarizing technical results. Create a clear, structured summary."
            },
            {
                "role": "user",
                "content": format_prompt
            }
        ]
        
        try:
            formatted_response = self.llm.create_message(messages, temperature=0.2)
            
            return {
                "task": plan.get("task"),
                "objective": plan.get("objective"),
                "success_criteria": plan.get("success_criteria"),
                "completion": completion_check,
                "summary": formatted_response,
                "raw_results": execution_result.get("results", [])
            }
        except Exception as e:
            self.logger.error(f"Error formatting with LLM: {str(e)}")
            raise
    
    def _manual_format_answer(
        self,
        plan: Dict[str, Any],
        execution_result: Dict[str, Any],
        completion_check: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Manual formatting when LLM is not available"""
        # Build summary from raw results
        summary_parts = []
        summary_parts.append(f"Task: {plan.get('task')}")
        summary_parts.append("\nResults:")
        
        for result in execution_result.get("results", []):
            step_num = result.get("step_number")
            description = result.get("description")
            status = result.get("status")
            
            summary_parts.append(f"\nStep {step_num}: {description} [{status}]")
            
            # Add result details
            if status == "completed" and "result" in result:
                result_data = result["result"]
                
                if result_data.get("status") == "success":
                    # GitHub search results
                    if "results" in result_data and result_data.get("count"):
                        summary_parts.append(f"  Found {result_data['count']} items:")
                        for item in result_data.get("results", [])[:3]:  # Show top 3
                            if "name" in item:  # GitHub repo
                                summary_parts.append(f"    - {item['name']}: {item.get('stars', 0)} stars")
                            elif "temperature" in item:  # Weather (handled below)
                                pass
                    
                    # Weather results
                    if "weather" in result_data:
                        w = result_data["weather"]
                        city = result_data.get("city")
                        summary_parts.append(f"  {city}: {w['temperature']}°C, {w['description']}")
                else:
                    summary_parts.append(f"  Error: {result_data.get('error')}")
        
        summary_parts.append(f"\n\nCompletion: {completion_check['successful_steps']}/{completion_check['expected_steps']} steps")
        
        return {
            "task": plan.get("task"),
            "objective": plan.get("objective"),
            "success_criteria": plan.get("success_criteria"),
            "completion": completion_check,
            "summary": "\n".join(summary_parts),
            "raw_results": execution_result.get("results", []),
            "note": "(Using fallback formatter - LLM quota exhausted)"
        }
    
    def _create_format_prompt(self, plan: Dict[str, Any], execution_result: Dict[str, Any]) -> str:
        """
        Create the formatting prompt
        
        Args:
            plan: Original plan
            execution_result: Execution results
            
        Returns:
            Formatted prompt for LLM
        """
        results_json = json.dumps(execution_result.get("results", []), indent=2)
        
        return f"""
Task: {plan.get('task')}
Objective: {plan.get('objective')}
Success Criteria: {plan.get('success_criteria')}

Execution Results:
{results_json}

Please create a clear, structured summary of:
1. What was accomplished
2. Key findings or data obtained
3. Any issues encountered
4. Next steps if needed

Be concise but comprehensive.
"""
