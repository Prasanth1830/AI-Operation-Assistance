# Quick Start Guide

## 1-Minute Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Set Environment Variables
```bash
cp .env.example .env
# Edit .env with YOUR API keys:
# - OPENAI_API_KEY (from https://platform.openai.com)
# - GITHUB_TOKEN (from https://github.com/settings/tokens)
# - WEATHER_API_KEY (from https://openweathermap.org/api)
```

### Step 3: Run Examples

#### Via CLI (Quickest)
```bash
# Single task
python cli.py "Find top 5 Python AI framework repositories on GitHub"

# Interactive mode
python cli.py
```

#### Via API
```bash
# Start server
python main.py

# In another terminal
curl -X POST http://127.0.0.1:8000/process-task \
  -H "Content-Type: application/json" \
  -d '{"task": "What is the weather in London?"}'
```

## Task Examples

### Simple Tasks
- "What is the weather in San Francisco?"
- "Find popular Python repositories"
- "Get weather forecast for New York"

### Complex Tasks
- "Find the top 5 Python AI libraries on GitHub and tell me about the current weather in San Francisco"
- "Search for JavaScript web frameworks and get weather data for London, Tokyo, and Sydney"
- "What are the trending Python repositories and what's the weather like in Berlin?"

### Multi-Step Tasks
- "Find repositories about machine learning, tell me current weather in 3 major cities"
- "Get the top GitHub repositories for web development in Python, JavaScript, and Go"

## Understanding Agent Flow

```
Natural Language Input
    ↓
[PLANNER] Breaks down into steps + selects tools
    ↓
[EXECUTOR] Runs each step, calls APIs
    ↓
[VERIFIER] Validates and formats results
    ↓
Structured JSON Output
```

## API Response Structure

```json
{
  "status": "success",
  "user_task": "original task",
  "plan": {
    "objective": "what we're trying to achieve",
    "steps": [
      {"step_number": 1, "description": "...", "tool": "..."}
    ]
  },
  "execution": {
    "results": [
      {"step_number": 1, "status": "completed", "result": {...}}
    ]
  },
  "final_answer": {
    "summary": "human-readable summary"
  }
}
```

## Configuration Reference

Key settings in `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| OPENAI_MODEL | gpt-4-turbo-preview | LLM model to use |
| SERVER_HOST | 127.0.0.1 | API server host |
| SERVER_PORT | 8000 | API server port |
| DEBUG | false | Enable debug logging |
| LOG_LEVEL | INFO | Logging level |

## Troubleshooting

**Q: "OPENAI_API_KEY must be set"**
A: Make sure your .env file has `OPENAI_API_KEY=your_actual_key` (without quotes)

**Q: "JSON parse error"**
A: Check that your API keys are valid and your OpenAI account has credits

**Q: Tasks running slow**
A: This is normal - each task involves API calls which take time. Average: 5-15 seconds

**Q: "Unknown tool" error**
A: The planner selected a tool that doesn't exist. This is rare. Check logs.

## Next Steps

1. ✅ Install and run a quick test task
2. 📚 Read [README.md](README.md) for detailed documentation
3. 🔧 Explore the agents in `agents/` folder
4. 🛠️  Try adding custom tools in `tools/` folder
5. 🚀 Deploy the API server for production use

## Performance Tips

- Use shorter, more specific task descriptions
- Let the planner break down complex tasks
- Avoid very large max_results parameters
- Monitor API rate limits

## For Developers

### Adding a New Tool

1. Create `tools/my_tool.py`
2. Inherit from `BaseTool`
3. Implement `name`, `description`, `parameters`, `execute()`
4. Register in executor: `self.tools["my_tool"] = MyTool()`

### Running in Debug Mode

```bash
DEBUG=true LOG_LEVEL=DEBUG python cli.py "your task"
```

---

**Need help?** See README.md for detailed documentation
