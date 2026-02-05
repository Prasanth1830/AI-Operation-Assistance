# AI Operations Assistant

A sophisticated multi-agent system that accepts natural-language tasks, plans steps, calls real third-party APIs, and returns structured answers. Built with LLM-powered reasoning for agent-based task execution.

## Architecture Overview

```
User Input (Natural Language Task)
          ↓
    ┌─────────────────┐
    │  PLANNER AGENT  │  (LLM-based task planning)
    └─────────┬───────┘
              ↓
         JSON Plan
              ↓
    ┌─────────────────────┐
    │  EXECUTOR AGENT     │  (Tool execution)
    │ ├─ GitHub Tool      │
    │ └─ Weather Tool     │
    └─────────┬───────────┘
              ↓
       Execution Results
              ↓
    ┌─────────────────┐
    │  VERIFIER AGENT │  (Result validation & formatting)
    └─────────┬───────┘
              ↓
        Final Answer (JSON)
```

## Core Capabilities

✅ **Multi-Agent Architecture**
- Planner Agent: Converts user input into structured step-by-step plans
- Executor Agent: Executes steps in order and calls appropriate tools
- Verifier Agent: Validates completeness and formats final output

✅ **LLM-Powered Reasoning**
- Uses OpenAI GPT-4 for intelligent planning and validation
- Structured JSON output for all agent communications
- Temperature and token-controlled for deterministic planning

✅ **Real API Integration**
- **GitHub API**: Search repositories, get user info, track stars and forks
- **Weather API**: Current weather and 24-hour forecasts for any city

✅ **Multiple Interfaces**
- FastAPI REST API with Swagger documentation
- Interactive CLI with real-time feedback
- Structured JSON output for programmatic use

## Project Structure

```
ai_ops_assistant/
├── agents/
│   ├── __init__.py
│   ├── base.py              # BaseAgent abstract class
│   ├── planner.py           # PlannerAgent implementation
│   ├── executor.py          # ExecutorAgent implementation
│   └── verifier.py          # VerifierAgent implementation
├── tools/
│   ├── __init__.py
│   ├── base.py              # BaseTool abstract class
│   ├── github_tool.py       # GitHub API integration
│   └── weather_tool.py      # Weather API integration
├── llm/
│   ├── __init__.py
│   ├── base.py              # BaseLLMClient abstract class
│   └── openai_client.py     # OpenAI integration
├── config.py                # Configuration management
├── orchestrator.py          # Multi-agent orchestrator
├── main.py                  # FastAPI application
├── cli.py                   # CLI interface
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
└── README.md               # This file
```

## Installation & Setup

### 1. Prerequisites
- Python 3.8+
- pip or conda
- API keys for:
  - OpenAI API (for LLM)
  - GitHub API (for repository search)
  - OpenWeatherMap API (for weather data)

### 2. Clone/Setup Project
```bash
cd ai_ops_assistant
```

### 3. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
```bash
# Copy example to .env
cp .env.example .env

# Edit .env with your API keys
# Required keys:
# - OPENAI_API_KEY
# - GITHUB_TOKEN
# - WEATHER_API_KEY
```

### Getting API Keys

#### OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Create new secret key
3. Copy to .env as `OPENAI_API_KEY`

#### GitHub Token
1. Go to https://github.com/settings/tokens
2. Create new personal access token with `repo` and `public_repo` scopes
3. Copy to .env as `GITHUB_TOKEN`

#### Weather API Key
1. Go to https://openweathermap.org/api
2. Sign up and create API key
3. Copy to .env as `WEATHER_API_KEY`

## Usage

### Option 1: REST API

#### Start the Server
```bash
python main.py
```
Server runs on `http://127.0.0.1:8000`

#### Health Check
```bash
curl http://127.0.0.1:8000/health
```

#### Process a Task
```bash
curl -X POST http://127.0.0.1:8000/process-task \
  -H "Content-Type: application/json" \
  -d '{"task": "Find top 5 Python repositories on GitHub and current weather in San Francisco"}'
```

#### API Documentation
Visit `http://127.0.0.1:8000/docs` for interactive Swagger UI

### Option 2: Command-Line Interface

#### Single Task
```bash
python cli.py "Find the top Python repository with the most stars"
```

#### Interactive Mode
```bash
python cli.py
# Then type tasks interactively
```

## Example Tasks

### Example 1: GitHub Repository Search
```
Task: Find the top 5 most-starred Python agent frameworks and tell me about them
```
**What it does:**
- Plans GitHub search using language and star criteria
- Executes three searches for different frameworks
- Aggregates and verifies results
- Provides formatted summary

### Example 2: Weather & Repository Combined
```
Task: Find the top Node.js repositories for weather applications and tell me the current weather in New York
```
**What it does:**
- Plans both GitHub search and weather API call
- Executes in parallel-ready steps
- Combines results into coherent answer

### Example 3: Multiple Locations
```
Task: Get current weather for London, Tokyo, and New York
```
**What it does:**
- Plans three weather API calls
- Executes sequentially
- Returns formatted weather comparison

## API Reference

### POST /process-task

Process a natural language task through the multi-agent system.

**Request:**
```json
{
  "task": "Natural language task description"
}
```

**Response:**
```json
{
  "status": "success",
  "user_task": "...",
  "plan": {
    "task": "...",
    "objective": "...",
    "steps": [...],
    "success_criteria": "..."
  },
  "execution": {
    "status": "success",
    "steps_executed": 2,
    "results": [...]
  },
  "verification": {
    "status": "success",
    "completion_check": {...},
    "final_answer": {...}
  },
  "final_answer": {
    "task": "...",
    "objective": "...",
    "summary": "...",
    "raw_results": [...]
  }
}
```

## Agent Details

### Planner Agent

**Function:** Converts natural language tasks into structured execution plans

**Process:**
1. Receives user task
2. Identifies required tools and steps
3. Creates JSON plan with:
   - Task description
   - Objective
   - Ordered steps with parameters
   - Success criteria

**Example Plan:**
```json
{
  "task": "Find top Python repos and SF weather",
  "objective": "Get repository info and weather data",
  "steps": [
    {
      "step_number": 1,
      "description": "Search GitHub for top Python repositories",
      "tool": "github_search_repos",
      "params": {"query": "language:python stars:>10000", "max_results": 5},
      "expected_outcome": "List of 5 top Python repos"
    },
    {
      "step_number": 2,
      "description": "Get current weather in San Francisco",
      "tool": "get_weather",
      "params": {"city": "San Francisco", "units": "imperial"},
      "expected_outcome": "Current weather conditions"
    }
  ],
  "success_criteria": "Get 5 repos and SF weather"
}
```

### Executor Agent

**Function:** Executes planned steps by calling appropriate tools

**Process:**
1. Receives plan from Planner
2. Iterates through steps in order
3. Calls appropriate tool with parameters
4. Handles errors gracefully
5. Returns results for each step

**Step Result Format:**
```json
{
  "step_number": 1,
  "status": "completed|failed|skipped",
  "description": "...",
  "tool": "tool_name",
  "params": {...},
  "result": {...},
  "error": "error message if failed"
}
```

### Verifier Agent

**Function:** Validates results and creates formatted final answer

**Process:**
1. Evaluates plan completion
2. Checks data quality
3. Formats results using LLM
4. Creates summary with insights
5. Returns validated final answer

**Validation Checks:**
- All steps executed
- No critical errors
- Complete data received
- Proper formatting

## Tools Documentation

### GitHub Tool

Search and retrieve information about GitHub repositories and users.

**Methods:**
- `search_repos(query, max_results)` - Search repositories
- `get_user_info(username)` - Get user information

**Example:**
```python
from tools import GitHubTool

tool = GitHubTool()
result = tool.execute(
    query="language:python stars:>5000",
    max_results=10
)
```

### Weather Tool

Get current weather and forecasts for any location.

**Methods:**
- `execute(city, units)` - Get current weather
- `get_forecast(city, units)` - Get 24-hour forecast

**Example:**
```python
from tools import WeatherTool

tool = WeatherTool()
result = tool.execute(
    city="San Francisco",
    units="imperial"
)
```

## Configuration

All configuration is managed via environment variables in `.env`:

```bash
# LLM Configuration
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo-preview

# API Keys
GITHUB_TOKEN=ghp_...
WEATHER_API_KEY=...

# Server Configuration
SERVER_HOST=127.0.0.1
SERVER_PORT=8000
DEBUG=true

# Logging
LOG_LEVEL=INFO
```

## Error Handling

The system implements graceful error handling:

1. **API Failures**: Retries up to 3 times with exponential backoff
2. **Missing Data**: Returns partial results with error indicators
3. **Invalid Plans**: Planner re-validates and provides structured error
4. **Tool Errors**: Executor reports failure and continues with other steps
5. **Format Errors**: Verifier provides raw results if formatting fails

## Performance & Limitations

**Current Performance:**
- Average task execution: 5-15 seconds
- API rate limits depend on provider accounts
- Parallel execution ready (sequential in current version)

**Known Limitations:**
- GitHub search limited to 1000 results max
- Weather API limited to 5-minute update frequency
- OpenAI token limits affect very complex plans
- No caching layer (can be added)

## Future Improvements

- [ ] Implement response caching for repeated queries
- [ ] Add cost tracking per request
- [ ] Parallel step execution
- [ ] More tool integrations (News, Email, Slack, etc.)
- [ ] Advanced retry strategies
- [ ] Token usage optimization
- [ ] Output streaming for long tasks
- [ ] Conversation history and context retention

## Development

### Running Tests
```bash
# Will be added in future versions
pytest tests/
```

### Logging
Set `LOG_LEVEL` in .env to control logging:
- `DEBUG`: Detailed information for debugging
- `INFO`: General informational messages
- `WARNING`: Warning messages only
- `ERROR`: Errors only

### Debugging

Enable debug mode in .env:
```bash
DEBUG=true
LOG_LEVEL=DEBUG
```

Then check logs during execution for detailed agent interactions.

## Code Quality

The project follows these principles:

1. **Abstraction**: Base classes for agents and tools
2. **Separation of Concerns**: Each agent has single responsibility
3. **Type Hints**: Full Python type annotations
4. **Error Handling**: Comprehensive try-catch with logging
5. **Documentation**: Docstrings for all public methods
6. **Modularity**: Easy to add new tools and agents

## Example Execution Flow

```
User: "Find top Python ML libraries and weather in Tokyo"
        ↓
PLANNER: Creates 2-step plan
        ↓
EXECUTOR: Step 1 → GitHub API call → returns repo list
          Step 2 → Weather API call → returns weather data
        ↓
VERIFIER: Validates both steps complete
          Formats results into summary
          Returns structured answer
        ↓
Output: JSON with repos, weather, and summary
```

## Troubleshooting

### "OPENAI_API_KEY must be set"
- Copy `.env.example` to `.env`
- Add your actual OpenAI API key
- Ensure no quotes around the key

### "Could not parse JSON from response"
- Check OpenAI API key validity
- Verify `gpt-4-turbo-preview` model is available
- Check account has sufficient credits

### API Rate Limit Errors
- Reduce `max_results` parameter
- Add delay between requests
- Check API provider rate limits

### Weather API Errors
- Verify city name spelling
- Check OpenWeatherMap API key
- Ensure API key has access to weather endpoint

## License

This project is built for educational and demonstration purposes.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review error logs with `LOG_LEVEL=DEBUG`
3. Verify all API keys are correct
4. Check API provider status pages

---

**Built with:** FastAPI, OpenAI API, Python, GitHub API, OpenWeatherMap API

**Last Updated:** February 2026
