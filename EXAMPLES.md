# Working Examples & Test Cases

## Example 1: GitHub Repository Search

### Use Case
Find popular Python machine learning libraries on GitHub

### Command
```bash
python cli.py "Find the top 5 Python repositories related to machine learning with description and star count"
```

### Expected Flow
1. **Planner** creates plan:
   - Search GitHub with language:python and ml-related keywords
   - Max 5 results sorted by stars

2. **Executor** calls GitHub API:
   - Query: `language:python machine learning`
   - Returns: name, stars, description, language, owner

3. **Verifier** formats output:
   - Lists repositories with stats
   - Summarizes findings
   - Highlights top picks

### Sample Output
```
Plan:
- Search GitHub for machine learning Python repositories
- Retrieve top 5 by stars

Execution:
✓ Step 1: GitHub search completed [5 results]
  - tensorflow: 174,000 stars
  - scikit-learn: 56,000 stars
  - pytorch: 72,000 stars
  - keras: 60,000 stars
  - pandas: 140,000 stars

Final Answer:
Top 5 Python ML libraries:
1. TensorFlow - 174,000 stars - ML/DL framework
2. pandas - 140,000 stars - Data manipulation
3. PyTorch - 72,000 stars - Deep learning
4. scikit-learn - 56,000 stars - ML algorithms
5. Keras - 60,000 stars - DL API
```

---

## Example 2: Weather Information Lookup

### Use Case
Get weather for multiple cities

### Command
```bash
python cli.py "Tell me current weather for London, Tokyo, and Sydney"
```

### Expected Flow
1. **Planner** creates plan:
   - Step 1: Get weather for London
   - Step 2: Get weather for Tokyo
   - Step 3: Get weather for Sydney

2. **Executor** calls Weather API 3 times:
   - Returns: temperature, humidity, wind speed, description

3. **Verifier** formats output:
   - Compares temperatures
   - Summarizes conditions
   - Notes any alerts

### Sample Output
```
Plan:
- Get current weather for 3 cities
- Return temperature, conditions, humidity

Execution:
✓ Step 1: London weather [20°C, Cloudy]
✓ Step 2: Tokyo weather [18°C, Rainy]
✓ Step 3: Sydney weather [25°C, Sunny]

Final Answer:
Weather Summary:
- London: 20°C, Cloudy, 65% humidity
- Tokyo: 18°C, Rainy, 80% humidity
- Sydney: 25°C, Sunny, 45% humidity

Warmest: Sydney (25°C)
Rainiest: Tokyo (Rainy conditions)
```

---

## Example 3: Combined Task (repositories + weather)

### Use Case
Find JavaScript web frameworks and check weather in tech hubs

### Command
```bash
python cli.py "Find top 3 JavaScript web frameworks on GitHub and tell me the current weather in San Francisco and Berlin"
```

### Expected Flow
1. **Planner** creates plan:
   - Step 1: Search for JS frameworks
   - Step 2: Get SF weather
   - Step 3: Get Berlin weather

2. **Executor** runs all steps:
   - GitHub API returns 3 frameworks
   - Weather API returns 2 cities

3. **Verifier** combines results:
   - Framework details
   - Weather comparison
   - Unified summary

### Sample Output
```
Plan:
- Search GitHub for JavaScript web frameworks
- Get weather for 2 cities
- Combine findings

Execution:
✓ Step 1: JS frameworks [3 results]
✓ Step 2: SF weather [20°C, Clear]
✓ Step 3: Berlin weather [15°C, Cloudy]

Final Answer:
Top JavaScript Frameworks:
1. React - 195,000 stars
2. Vue - 195,000 stars  
3. Angular - 88,000 stars

Tech Hub Weather:
- San Francisco: 20°C, Clear (ideal weather)
- Berlin: 15°C, Cloudy (cool conference conditions)
```

---

## Example 4: API Testing

### Using REST API

```bash
# 1. Start the server
python main.py &
sleep 2

# 2. Health check
curl http://127.0.0.1:8000/health

# 3. Send task via API
curl -X POST http://127.0.0.1:8000/process-task \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Find top Python web frameworks and weather in Seattle"
  }'

# 4. Expected Response:
{
  "status": "success",
  "user_task": "Find top Python web frameworks and weather in Seattle",
  "plan": {
    "objective": "...",
    "steps": [...]
  },
  "execution": {
    "status": "success",
    "results": [...]
  },
  "final_answer": {
    "summary": "...",
    "raw_results": [...]
  }
}
```

---

## Example 5: Python Programmatic Usage

### Direct Orchestrator Usage
```python
from orchestrator import AIOperationsOrchestrator
import json

orchestrator = AIOperationsOrchestrator()

# Process a task
result = orchestrator.process_task(
    "Find top 10 Go repositories and weather in San Francisco"
)

# Access plan
print("Plan Objective:", result['plan']['objective'])
print("Number of Steps:", len(result['plan']['steps']))

# Access execution results
for step_result in result['execution']['results']:
    status = step_result['status']
    description = step_result['description']
    print(f"✓ {description} [{status}]")

# Access final answer
print("\nFinal Summary:")
print(result['final_answer']['summary'])
```

### Agent-by-Agent Usage
```python
from agents import PlannerAgent, ExecutorAgent, VerifierAgent

# Initialize agents
planner = PlannerAgent()
executor = ExecutorAgent()
verifier = VerifierAgent()

# Step 1: Plan
task = "Find Rust repositories and weather in Berlin"
plan_result = planner.execute(user_task=task)
plan = plan_result['plan']
print(f"Created plan with {len(plan['steps'])} steps")

# Step 2: Execute
exec_result = executor.execute(plan=plan)
print(f"Executed {exec_result['steps_executed']} steps")

# Step 3: Verify
verify_result = verifier.execute(
    plan=plan,
    execution_result=exec_result
)

print("\nVerification Status:", verify_result['status'])
print("Summary:", verify_result['final_answer']['summary'])
```

---

## Example 6: Tool Direct Usage

### GitHub Tool
```python
from tools import GitHubTool

github = GitHubTool()

# Search repositories
repos = github.execute(
    query="language:rust stars:>5000",
    max_results=5
)

if repos['status'] == 'success':
    print(f"Found {repos['count']} repositories:")
    for repo in repos['results']:
        print(f"  - {repo['name']}: {repo['stars']} stars")

# Get user info
user = github.get_user_info("linus")
if user['status'] == 'success':
    print(f"\nUser: {user['user']['name']}")
    print(f"Followers: {user['user']['followers']}")
```

### Weather Tool
```python
from tools import WeatherTool

weather = WeatherTool()

# Get current weather
current = weather.execute(city="Paris", units="metric")

if current['status'] == 'success':
    w = current['weather']
    print(f"Paris: {w['temperature']}°C")
    print(f"Condition: {w['description']}")
    print(f"Humidity: {w['humidity']}%")

# Get forecast
forecast = weather.get_forecast(city="Paris")

if forecast['status'] == 'success':
    print(f"\n24-hour forecast for {forecast['city']}:")
    for f in forecast['forecasts']:
        print(f"  {f['datetime']}: {f['temperature']}°C, {f['description']}")
```

---

## Example 7: Error Handling

### Graceful Degradation
```bash
# Task with potential failures
python cli.py "Find repos about weather and get weather for London and InvalidCity"
```

**Expected:**
- London weather succeeds
- InvalidCity fails gracefully
- Overall status might be "partial"
- Raw results show which steps succeeded

```python
result = orchestrator.process_task("Get weather in InvalidCityABC")

if result['status'] == 'success':
    print("Fully successful")
else:
    # Check what happened
    for step in result['execution']['results']:
        if step['status'] == 'failed':
            print(f"Step {step['step_number']} failed: {step['error']}")
```

---

## Example 8: Complex Multi-Step Task

### Real-World Scenario
```bash
python cli.py "Compare GitHub activity: find top 5 JavaScript 
frameworks, top 5 Python ML libraries, and top 5 Golang tools, 
then tell me weather in the SVN Valley cities (San Francisco, 
San Jose, Palo Alto)"
```

**What happens:**
1. Planner creates 8-step plan
2. Executor runs GitHub searches (3) + Weather API (3)
3. Verifier synthesizes into comparison

**Output includes:**
- JavaScript frameworks with stats
- Python ML libraries with stats
- Go tools with stats
- Silicon Valley weather comparison
- Synthesis and insights

---

## Example 9: Batch Processing

### Process Multiple Tasks
```python
from orchestrator import AIOperationsOrchestrator

orchestrator = AIOperationsOrchestrator()

tasks = [
    "Get weather in London",
    "Find top Python repos",
    "Weather in Tokyo and Sydney",
    "Top Go repositories"
]

results = []
for task in tasks:
    print(f"\nProcessing: {task}")
    result = orchestrator.process_task(task)
    results.append({
        "task": task,
        "status": result['status'],
        "summary": result['final_answer']['summary']
    })

# Analyze results
successful = [r for r in results if r['status'] == 'success']
print(f"\n{len(successful)}/{len(tasks)} tasks successful")
```

---

## Example 10: Integration Testing

### Full System Test
```bash
#!/bin/bash

echo "Starting AI Operations Assistant test suite..."

# 1. Test API server
echo "1. Testing API server..."
python main.py &
SERVER_PID=$!
sleep 3

# Test health endpoint
curl -s http://127.0.0.1:8000/health | grep -q "healthy" && echo "✓ Health check" || echo "✗ Health check"

# Test task endpoint
curl -s -X POST http://127.0.0.1:8000/process-task \
  -H "Content-Type: application/json" \
  -d '{"task":"weather London"}' | grep -q "success" && echo "✓ Task processing" || echo "✗ Task processing"

kill $SERVER_PID

# 2. Test CLI
echo "2. Testing CLI..."
python cli.py "Get weather in Paris" 2>/dev/null | grep -q "Final Answer" && echo "✓ CLI interface" || echo "✗ CLI interface"

# 3. Test individual agents
echo "3. Testing agents..."
python -c "
from agents import PlannerAgent
p = PlannerAgent()
r = p.execute(user_task='weather')
assert r['status'] == 'success'
print('✓ Planner Agent')
"

echo "All tests completed!"
```

---

## Troubleshooting Examples

### Example: API Key Issues

```python
# This will fail with clear error
from orchestrator import AIOperationsOrchestrator

# If OPENAI_API_KEY not set:
try:
    orchestrator = AIOperationsOrchestrator()
except ValueError as e:
    print(f"Configuration Error: {e}")
    # Output: "OPENAI_API_KEY must be set in .env file"
```

### Example: Network Issues

```python
# Tool handles network failures
from tools import WeatherTool

weather = WeatherTool()
result = weather.execute(city="London")

if result['status'] == 'error':
    print(f"Error: {result['error']}")
    # Shows network error details
else:
    print(f"Temperature: {result['weather']['temperature']}")
```

### Example: Rate Limiting

```python
import time

# If hitting rate limits, add delays
for city in ['London', 'Paris', 'Tokyo']:
    result = weather.execute(city=city)
    print(f"{city}: {result['weather']['temperature']}°C")
    time.sleep(1)  # Add delay between requests
```

---

## Performance Baseline

### Task Timing Examples

```bash
# Simple weather lookup: ~3-5 seconds
time python cli.py "Weather in London"

# GitHub search: ~5-8 seconds  
time python cli.py "Top Python repos"

# Combined task: ~8-12 seconds
time python cli.py "Find Java repos and weather in Tokyo"

# Complex multi-step: ~12-20 seconds
time python cli.py "Find 3 repo sets AND 3 cities weather"
```

---

**These examples showcase the system's capabilities and provide templates for your own use cases.**
