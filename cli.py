"""CLI interface for AI Operations Assistant"""
import json
import logging
import sys
from typing import Any, Dict

from config import Config
from orchestrator import AIOperationsOrchestrator

# Setup logging
logging.basicConfig(
    level=Config.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class AIACLI:
    """Command-line interface for AI Operations Assistant"""
    
    def __init__(self):
        """Initialize CLI"""
        try:
            Config.validate()
            self.orchestrator = AIOperationsOrchestrator()
            logger.info("AI Operations Assistant CLI initialized")
        except ValueError as e:
            logger.error(f"Failed to initialize: {str(e)}")
            print(f"Error: {str(e)}")
            sys.exit(1)
    
    def run(self, task: str):
        """
        Run a task through the orchestrator
        
        Args:
            task: Natural language task
        """
        logger.info(f"Processing task: {task}")
        print(f"\n{'='*70}")
        print(f"Task: {task}")
        print(f"{'='*70}\n")
        
        try:
            result = self.orchestrator.process_task(task)
            
            # Display plan
            if "plan" in result:
                print("📋 PLAN")
                print("-" * 70)
                plan = result["plan"]
                print(f"Objective: {plan.get('objective')}")
                print(f"\nSteps:")
                for step in plan.get("steps", []):
                    print(f"  {step.get('step_number')}. {step.get('description')}")
                    if step.get('tool') != 'none':
                        print(f"     Tool: {step.get('tool')}")
                print()
            
            # Display execution results
            if "execution" in result:
                print("⚙️  EXECUTION RESULTS")
                print("-" * 70)
                for step_result in result["execution"].get("results", []):
                    step_num = step_result.get("step_number")
                    status = step_result.get("status")
                    desc = step_result.get("description")
                    
                    status_icon = "✓" if status == "completed" else "✗" if status == "failed" else "○"
                    print(f"{status_icon} Step {step_num}: {desc} [{status}]")
                    
                    if status == "completed" and "result" in step_result:
                        result_data = step_result["result"]
                        if result_data.get("status") == "success":
                            print(f"   Result: Success")
                            if "count" in result_data:
                                print(f"   Items found: {result_data['count']}")
                        else:
                            print(f"   Error: {result_data.get('error')}")
                print()
            
            # Display final answer
            if "verification" in result:
                print("📊 FINAL ANSWER")
                print("-" * 70)
                final_answer = result["verification"].get("final_answer", {})
                completion = final_answer.get("completion", {})
                
                print(f"Completion Status: {completion.get('successful_steps')}/{completion.get('expected_steps')} steps")
                print(f"\nSummary:")
                print(final_answer.get("summary", "N/A"))
                print()
            
            # Display raw results if available
            print("📋 DETAILED RESULTS")
            print("-" * 70)
            print(json.dumps(result, indent=2, default=str))
            
        except Exception as e:
            logger.error(f"Error processing task: {str(e)}")
            print(f"Error: {str(e)}")
            sys.exit(1)
    
    def interactive_mode(self):
        """Run in interactive mode"""
        print("\n🤖 AI Operations Assistant - Interactive Mode")
        print("=" * 70)
        print("Type 'quit' or 'exit' to exit\n")
        
        while True:
            try:
                task = input("Enter task: ").strip()
                
                if task.lower() in ["quit", "exit"]:
                    print("Goodbye!")
                    break
                
                if not task:
                    print("Please enter a task")
                    continue
                
                self.run(task)
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                logger.error(f"Error: {str(e)}")
                print(f"Error: {str(e)}")


def main():
    """Main entry point"""
    cli = AIACLI()
    
    # Check if task provided as argument
    if len(sys.argv) > 1:
        # Join all arguments as task
        task = " ".join(sys.argv[1:])
        cli.run(task)
    else:
        # Run in interactive mode
        cli.interactive_mode()


if __name__ == "__main__":
    main()
