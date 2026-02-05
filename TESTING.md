# Testing Guide

## Manual Testing Checklist

### Pre-Test Setup
- [ ] All environment variables configured in .env
- [ ] API keys working (test with curl/Postman)
- [ ] Python 3.8+ installed
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] No syntax errors: `python -m py_compile *.py`

### API Connectivity Tests

#### GitHub API Test
```bash
curl -H "Authorization: token YOUR_GITHUB_TOKEN" \
  https://api.github.com/user
```
Expected: Returns user info (not 401)

#### Weather API Test
```bash
curl "https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_API_KEY"
```
Expected: Returns weather data (not 401)

#### OpenAI API Test
```python
import openai
openai.api_key = "YOUR_API_KEY"
response = openai.ChatCompletion.create(
    model="gpt-4-turbo-preview",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.choices[0].message.content)
```
Expected: Returns text response

### Agent-Level Unit Tests

#### Test Planner Agent
```python
from agents import PlannerAgent

planner = PlannerAgent()
result = planner.execute(user_task="Get weather in London")

assert result["status"] == "success"
assert "plan" in result
assert "steps" in result["plan"]
assert len(result["plan"]["steps"]) > 0

print("✓ Planner Agent works")
```

#### Test Executor Agent
```python
from agents import ExecutorAgent

executor = ExecutorAgent()
plan = {
    "task": "Get weather",
    "steps": [
        {
            "step_number": 1,
            "description": "Get weather",
            "tool": "get_weather",
            "params": {"city": "London"}
        }
    ]
}

result = executor.execute(plan=plan)
assert result["status"] == "success"
assert len(result["results"]) == 1
assert result["results"][0]["status"] in ["completed", "failed"]

print("✓ Executor Agent works")
```

#### Test Verifier Agent
```python
from agents import VerifierAgent

verifier = VerifierAgent()
plan = {"task": "test", "objective": "test", "steps": [], "success_criteria": "test"}
execution = {"status": "success", "results": []}

result = verifier.execute(plan=plan, execution_result=execution)
assert result["status"] in ["success", "partial"]
assert "final_answer" in result

print("✓ Verifier Agent works")
```

### Tool-Level Tests

#### Test GitHub Tool
```python
from tools import GitHubTool

github = GitHubTool()

# Test repo search
result = github.execute(
    query="language:python stars:>1000",
    max_results=5
)
assert result["status"] == "success"
assert "results" in result
assert len(result["results"]) > 0
assert "name" in result["results"][0]
assert "stars" in result["results"][0]

print(f"✓ GitHub Tool works - found {result['count']} repos")

# Test user info
user_result = github.get_user_info("torvalds")
assert user_result["status"] == "success"
assert "user" in user_result

print("✓ GitHub user lookup works")
```

#### Test Weather Tool
```python
from tools import WeatherTool

weather = WeatherTool()

# Test current weather
result = weather.execute(city="London", units="metric")
assert result["status"] == "success"
assert "city" in result
assert "weather" in result
assert "temperature" in result["weather"]

print(f"✓ Weather Tool works - {result['city']}: {result['weather']['description']}")

# Test forecast
forecast = weather.get_forecast(city="London")
assert forecast["status"] == "success"
assert "forecasts" in forecast

print("✓ Weather forecast works")
```

### Integration Tests

#### Test Complete Pipeline
```python
from orchestrator import AIOperationsOrchestrator

orchestrator = AIOperationsOrchestrator()

# Simple task
task1 = "What is the weather in Paris?"
result1 = orchestrator.process_task(task1)

assert result1["status"] == "success"
assert "plan" in result1
assert "execution" in result1
assert "final_answer" in result1

print("✓ Simple task works")

# Complex task
task2 = "Find top 3 Python repos and weather in New York"
result2 = orchestrator.process_task(task2)

assert result2["status"] == "success"
assert len(result2["execution"]["results"]) >= 2

print("✓ Complex task works")
```

#### Test API Server
```bash
# Start server in background
python main.py &
sleep 2

# Health check
curl http://127.0.0.1:8000/health
# Expected: {"status":"healthy",...}

# Process task
curl -X POST http://127.0.0.1:8000/process-task \
  -H "Content-Type: application/json" \
  -d '{"task":"What is the weather in Tokyo?"}'
# Expected: JSON response with plan, execution, final_answer

# Kill server
pkill -f "python main.py"
```

#### Test CLI
```bash
# Single task
python cli.py "Get weather in Berlin"

# Should output:
# - Plan
# - Execution results
# - Final answer summary
```

### Scenario Tests

#### Scenario 1: GitHub Search
**Task:** Find top 5 Python repositories
**Expected:**
- Plan created with github_search_repos tool
- Repository results with stars, descriptions
- Successfully formatted summary

**Test Command:**
```bash
python cli.py "Find top 5 Python repositories on GitHub"
```

#### Scenario 2: Weather Lookup
**Task:** Current weather for multiple cities
**Expected:**
- Plan created with multiple weather steps
- Each city's current conditions
- Formatted comparison summary

**Test Command:**
```bash
python cli.py "Get current weather for London, Tokyo, and New York"
```

#### Scenario 3: Combined Task
**Task:** Repositories + weather
**Expected:**
- Both tools executed
- Results combined appropriately
- Unified summary

**Test Command:**
```bash
python cli.py "Find Node.js frameworks on GitHub and tell me weather in Seattle"
```

#### Scenario 4: Error Recovery
**Task:** Invalid input handling
**Expected:**
- Graceful error handling
- Informative error messages
- System remains stable

**Test Command:**
```bash
python cli.py "Find weather for nonexistentcityxyz"
```

### Performance Tests

#### Response Time Baseline
```python
import time
from orchestrator import AIOperationsOrchestrator

orchestrator = AIOperationsOrchestrator()

start = time.time()
result = orchestrator.process_task("Get weather in Paris")
duration = time.time() - start

print(f"Task completed in {duration:.1f} seconds")
# Expected: 5-15 seconds
```

#### Large Result Handling
```bash
python cli.py "Find repositories with language:java stars:>100"
# Should handle 100+ results without crashing
```

### Edge Cases

#### Empty/Invalid Tasks
```python
orchestrator.process_task("")  # Empty
orchestrator.process_task("   ")  # Whitespace
```
Expected: Handled gracefully

#### Missing API Data
```bash
python cli.py "Get weather for InvalidCity123"
```
Expected: Error returned, system continues

#### Rate Limiting
```bash
# Make 10 rapid requests
for i in {1..10}; do
  curl -X POST http://127.0.0.1:8000/process-task \
    -H "Content-Type: application/json" \
    -d '{"task":"weather Paris"}'
done
```
Expected: Either all succeed or graceful rate limit handling

## Automated Testing (pytest)

### Test Structure (once implemented)
```
tests/
├── test_agents/
│   ├── test_planner.py
│   ├── test_executor.py
│   └── test_verifier.py
├── test_tools/
│   ├── test_github_tool.py
│   └── test_weather_tool.py
├── test_llm/
│   └── test_openai_client.py
├── test_orchestrator.py
├── test_api.py
└── conftest.py
```

### Example Test Cases (pytest format)
```python
import pytest
from orchestrator import AIOperationsOrchestrator

@pytest.fixture
def orchestrator():
    return AIOperationsOrchestrator()

def test_simple_weather_task(orchestrator):
    result = orchestrator.process_task("Weather in London")
    assert result["status"] == "success"
    assert "plan" in result

def test_github_search_task(orchestrator):
    result = orchestrator.process_task("Top Python repos")
    assert result["status"] == "success"
    assert result["execution"]["steps_executed"] > 0

def test_combined_task(orchestrator):
    result = orchestrator.process_task("Find repos and weather")
    assert result["status"] == "success"
    assert len(result["execution"]["results"]) >= 2
```

## Debugging Tips

### Enable Debug Logging
```bash
DEBUG=true LOG_LEVEL=DEBUG python cli.py "your task"
```

### Check Individual Steps
```python
from agents import PlannerAgent

planner = PlannerAgent()
result = planner.execute(user_task="your task")
print(json.dumps(result, indent=2))
```

### API Response Inspection
```python
from tools import GitHubTool

tool = GitHubTool()
result = tool.execute(query="language:python")
print(f"Status: {result['status']}")
print(f"Count: {result.get('count')}")
print(f"Sample: {result['results'][0] if result['results'] else 'No results'}")
```

## Common Issues & Solutions

### Issue: "OPENAI_API_KEY must be set"
**Solution:**
```bash
# Ensure .env file exists and contains:
OPENAI_API_KEY=sk-your-actual-key
# Note: no quotes
```

### Issue: "401 Unauthorized" from GitHub
**Solution:**
```bash
# Verify token works:
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user
# Should return user info, not 401
```

### Issue: "Weather API error"
**Solution:**
```bash
# Test API key:
curl "https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_KEY"
# Should return weather, not 401
```

### Issue: "Could not parse JSON"
**Solution:**
1. Check OpenAI API key and model name
2. Check account has sufficient credits
3. Try with DEBUG=true to see actual response
4. Might be temporary API issue - retry

### Issue: Slow responses
**Solution:**
- Normal: 5-15 seconds is expected
- Check API provider status
- Reduce max_results parameter
- Monitor rate limits

## Continuous Testing

### Development Workflow
1. Make code change
2. Run relevant unit test
3. Test manually with CLI
4. Check logs for issues
5. Test with API if changed
6. Commit with test results

### Pre-Release Checklist
- [ ] All individual agent tests pass
- [ ] All tool tests pass
- [ ] Integration test passes
- [ ] API server starts correctly
- [ ] CLI works for sample tasks
- [ ] README is current
- [ ] No commented-out code
- [ ] All error cases handled

---

**Testing is critical for production reliability. Test thoroughly before deployment.**
