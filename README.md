# AI Operations Assistant

A sophisticated multi-agent system that accepts natural-language tasks, plans steps, calls real third-party APIs, and returns structured answers. Built with LLM-powered reasoning (with graceful fallback) for agent-based task execution.

🚀 **Run in one command:**
```bash
uvicorn main:app --reload
```

Then visit: **http://127.0.0.1:8000/docs** for interactive API documentation

---

## Quick Start

### 1. Clone & Setup
```bash
cd ai_ops_assistant
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables
```bash
cp .env.example .env
# Edit .env with your API keys (see Environment Variables section)
```

### 3. Run the Application

**Option A: REST API Server (FastAPI)**
```bash
uvicorn main:app --reload
# Visit http://127.0.0.1:8000
# API Docs: http://127.0.0.1:8000/docs
```

**Option B: Command-Line Interface**
```bash
python cli.py "Find top Python repositories and weather in London"
```

**Option C: Test Components**
```bash
python test_components.py
```

---

## Environment Variables Required

Copy `.env.example` to `.env` and fill in your API keys:

```bash
# OpenAI API (for LLM-powered planning and verification)
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-3.5-turbo  # or gpt-4, gpt-4-turbo-preview

# GitHub API (for repository searches)
GITHUB_TOKEN=ghp_your-token-here

# OpenWeatherMap API (for weather data)
WEATHER_API_KEY=your-api-key-here

# Server Configuration
SERVER_HOST=127.0.0.1
SERVER_PORT=8000
DEBUG=true

# Logging
LOG_LEVEL=INFO
```

**How to Get API Keys:**
- [OpenAI](https://platform.openai.com/api-keys): Create API key
- [GitHub](https://github.com/settings/tokens): Create personal access token
- [OpenWeatherMap](https://openweathermap.org/api): Sign up and generate key

---

## Architecture Overview

```
User Input (Natural Language Task)
          ↓
    ┌─────────────────┐
    │  PLANNER AGENT  │  (LLM-based or rule-based fallback)
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
    │  VERIFIER AGENT │  (Validation & formatting, with LLM fallback)
    └─────────┬───────┘
              ↓
        Final Answer (JSON)
```

### How It Works

1. **Planner**: Converts natural language into structured steps
   - Tries LLM first for intelligent planning
   - Falls back to rule-based detection if quota exhausted
   - Detects programming languages and city names

2. **Executor**: Runs each step and calls appropriate tools
   - GitHub API for repository searches
   - Weather API for weather queries
   - Returns structured results

3. **Verifier**: Validates results and formats output
   - Checks all steps completed successfully
   - Formats results using LLM
   - Falls back to manual formatting if needed

### Fallback System

When OpenAI API quota is exhausted:
- Planner switches to rule-based keyword detection
- Still creates valid execution plans
- System continues working without cost
- Verifier manually formats results instead of using LLM

---

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

## Integrated APIs

✅ **GitHub API** (https://api.github.com)
- Search repositories by language, stars, forks
- Get repository metadata (owner, description, URLs)
- Supports authentication and higher rate limits

✅ **OpenWeatherMap API** (https://api.openweathermap.org)
- Get current weather conditions
- Temperature, humidity, wind speed, cloud coverage
- Support for any major world city

---

## Core Capabilities

✅ **Multi-Agent Architecture**
- **Planner Agent**: Converts user input into structured step-by-step plans
- **Executor Agent**: Executes steps in order and calls appropriate tools
- **Verifier Agent**: Validates completeness and formats final output

✅ **Intelligent Planning with Fallback**
- LLM-powered reasoning when API available
- Rule-based fallback when quota exhausted
- Automatic language and location detection

✅ **Real API Integration**
- GitHub API for repository searches with authentication
- Weather API for real-time weather conditions
- Error handling with graceful degradation

✅ **Multiple Interfaces**
- **FastAPI REST API**: Full Swagger documentation at `/docs`
- **Command-Line Interface**: Single command or interactive mode
- **Structured JSON Output**: For programmatic use

---

## Example Prompts to Test the System

### Example 1: Simple Repository Search
```
"Find the top 5 most-starred Python repositories"
```
**Expected Output:**
- List of 5 Python repos with star counts
- Repository URLs and descriptions

### Example 2: Multiple APIs Combined
```
"Find top JavaScript frameworks on GitHub and check weather in Tokyo"
```
**Expected Output:**
- 5 JavaScript framework repositories
- Tokyo weather conditions (temperature, humidity, cloudiness)

### Example 3: Weather Comparison
```
"Get weather for London, Paris, and New York"
```
**Expected Output:**
- Temperature for each city
- Weather conditions and wind speed
- Comparison summary

### Example 4: Language-Specific Search
```
"Show me the top Go projects with over 5000 stars and weather in Berlin"
```
**Expected Output:**
- Go projects filtered by star count
- Berlin current weather

### Example 5: Complex Multi-Step Task
```
"Find top Java repositories and check weather in San Francisco, then tell me which would be good for serverless computing"
```
**Expected Output:**
- Java repositories with descriptions
- San Francisco weather
- Analysis and recommendations

---

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
# ==================== LLM Configuration ====================
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-actual-key-here
OPENAI_MODEL=gpt-3.5-turbo  # Options: gpt-3.5-turbo, gpt-4, gpt-4-turbo-preview

# ==================== API Keys ====================
GITHUB_TOKEN=ghp_your-actual-token-here
WEATHER_API_KEY=your-actual-weather-api-key-here

# ==================== Server Configuration ====================
SERVER_HOST=127.0.0.1      # localhost
SERVER_PORT=8000           # Default port
DEBUG=true                 # Set to false in production

# ==================== Logging ====================
LOG_LEVEL=INFO             # Options: DEBUG, INFO, WARNING, ERROR
```

### Running the API Server

```bash
# Using uvicorn (recommended)
uvicorn main:app --reload

# Or using Python directly
python main.py

# Visit http://127.0.0.1:8000/docs for Swagger UI
# Visit http://127.0.0.1:8000/redoc for ReDoc
```

### Using the REST API

#### Health Check
```bash
curl http://127.0.0.1:8000/health
```

#### Process a Task
```bash
curl -X POST http://127.0.0.1:8000/process-task \
  -H "Content-Type: application/json" \
  -d '{"task": "Find top 5 Python repositories and weather in London"}'
```

### Using the CLI

#### Single Task
```bash
python cli.py "Find top JavaScript frameworks"
```

#### Interactive Mode
```bash
python cli.py
# Then type tasks interactively when prompted
```

---

## Error Handling

The system implements graceful error handling:

1. **API Failures**: Retries up to 3 times with exponential backoff
2. **Missing Data**: Returns partial results with error indicators
3. **Invalid Plans**: Planner re-validates and provides structured error
4. **Tool Errors**: Executor reports failure and continues with other steps
5. **Format Errors**: Verifier provides raw results if formatting fails

## Known Limitations & Tradeoffs

### API Limitations
| Limitation | Details | Workaround |
|-----------|---------|-----------|
| **GitHub Search** | Limited to 1000 results max per query | Use more specific filters (language, stars) |
| **Weather API** | Data updates every 5-10 minutes | Cache results for real-time dashboards |
| **OpenAI Quota** | May hit rate limits with peak usage | System has built-in fallback to rule-based planning |
| **Rate Limits** | All APIs have rate limits | Implement request queuing or caching |

### System Limitations
| Limitation | Impact | Workaround |
|-----------|--------|-----------|
| **Sequential Execution** | Steps run one-by-one, not in parallel | Can be enhanced in future versions |
| **Context Window** | Very large tasks may exceed token limits | Break into multiple smaller tasks |
| **LLM Dependency** | Cost increases with complex tasks | Rule-based fallback available when quota exhausted |
| **No Caching** | Repeated queries hit APIs again | Add response caching layer (planned) |
| **Single City Weather** | Only searches for one city at a time in plan | User can request multiple in single task |

### Tradeoffs Made
1. **Fallback System**: When OpenAI quota exhausted, system uses rule-based pattern matching instead of LLM
   - Pros: No cost, continues working
   - Cons: Less flexible planning than LLM

2. **Sequential Execution**: Steps execute one after another
   - Pros: Simpler, easier to debug
   - Cons: Slower than parallel execution

3. **No Caching**: Each query hits the actual API
   - Pros: Always fresh data
   - Cons: Higher API costs and slower responses

4. **English-Only Planning**: LLM plans in English
   - Pros: Simplifies prompt engineering
   - Cons: May not work as well for non-English inputs

### Performance Characteristics
- **Typical Task Execution**: 5-15 seconds
- **API Response Time**: 2-5 seconds per API call
- **Planning Time**: 2-3 seconds (LLM) or <1 second (fallback)
- **Network-Dependent**: Overall speed depends on API availability

### Supported Languages for Searches
Currently auto-detects and searches for:
- Python, JavaScript, Java, Go, Rust, TypeScript, C++, PHP, Ruby

To add support for more languages, update the `language_keywords` in `agents/planner.py`

---

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
