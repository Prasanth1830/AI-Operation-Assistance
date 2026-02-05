"""Orchestrator - coordinates all agents"""
import json
import logging
from typing import Any, Dict

from agents import PlannerAgent, ExecutorAgent, VerifierAgent

logger = logging.getLogger(__name__)


class AIOperationsOrchestrator:
    """Orchestrates the multi-agent system"""
    
    def __init__(self):
        """Initialize orchestrator with all agents"""
        self.planner = PlannerAgent()
        self.executor = ExecutorAgent()
        self.verifier = VerifierAgent()
    
    def process_task(self, user_task: str) -> Dict[str, Any]:
        """
        Process a user task through all agents
        
        Args:
            user_task: Natural language task from user
            
        Returns:
            Final result with validation
        """
        logger.info(f"Processing task: {user_task}")
        
        # Step 1: Planner - create plan
        plan_result = self.planner.execute(user_task=user_task)
        
        if plan_result["status"] != "success":
            logger.error(f"Planning failed: {plan_result.get('error')}")
            return {
                "status": "error",
                "phase": "planning",
                "error": plan_result.get("error")
            }
        
        plan = plan_result["plan"]
        logger.info(f"Plan created with {len(plan['steps'])} steps")
        
        # Step 2: Executor - execute plan
        execution_result = self.executor.execute(plan=plan)
        
        logger.info(f"Executed {execution_result['steps_executed']} steps")
        
        # Step 3: Verifier - validate and format results
        verification_result = self.verifier.execute(
            plan=plan,
            execution_result=execution_result
        )
        
        return {
            "status": "success",
            "user_task": user_task,
            "plan": plan,
            "execution": execution_result,
            "verification": verification_result,
            "final_answer": verification_result["final_answer"]
        }
