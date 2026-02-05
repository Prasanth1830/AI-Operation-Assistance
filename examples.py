"""
Example usage scripts for AI Operations Assistant
"""

# Example 1: Using the Orchestrator programmatically
from orchestrator import AIOperationsOrchestrator

orchestrator = AIOperationsOrchestrator()

task = "Find the top 5 Python repositories on GitHub with the most stars"
result = orchestrator.process_task(task)

print(f"Task: {result['user_task']}")
print(f"Status: {result['status']}")
print(f"Summary: {result['final_answer']['summary']}")


# Example 2: Using individual agents
from agents import PlannerAgent, ExecutorAgent, VerifierAgent

planner = PlannerAgent()
executor = ExecutorAgent()
verifier = VerifierAgent()

# Step 1: Plan
plan_result = planner.execute(user_task="Get weather for 3 cities")
plan = plan_result["plan"]

# Step 2: Execute
exec_result = executor.execute(plan=plan)

# Step 3: Verify
verify_result = verifier.execute(plan=plan, execution_result=exec_result)

print(verify_result["final_answer"]["summary"])


# Example 3: Direct tool usage
from tools import GitHubTool, WeatherTool

# GitHub API
github = GitHubTool()
repos = github.execute(query="language:python stars:>1000", max_results=5)
print(f"Found {repos['count']} repositories")

# Weather API
weather = WeatherTool()
weather_data = weather.execute(city="London", units="metric")
print(f"Weather in {weather_data['city']}: {weather_data['weather']['description']}")


# Example 4: Complex task with multiple steps
multi_task = """
Find the top 3 most-starred Python agent frameworks on GitHub 
and tell me the current weather in San Francisco, New York, and London
"""

result = orchestrator.process_task(multi_task)

# Access specific results
for step_result in result['execution']['results']:
    if step_result['status'] == 'completed':
        print(f"✓ {step_result['description']}")
    else:
        print(f"✗ {step_result['description']}")
