#!/bin/bash
# Setup script for AI Operations Assistant

echo "🚀 AI Operations Assistant - Setup Script"
echo "=========================================="
echo ""

# Check Python
echo "1. Checking Python installation..."
python_version=$(python --version 2>&1)
if [[ $? -eq 0 ]]; then
    echo "✓ Python found: $python_version"
else
    echo "✗ Python not found. Please install Python 3.8+"
    exit 1
fi

# Create virtual environment
echo ""
echo "2. Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "3. Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi
echo "✓ Virtual environment activated"

# Install dependencies
echo ""
echo "4. Installing dependencies..."
pip install -q -r requirements.txt
if [[ $? -eq 0 ]]; then
    echo "✓ Dependencies installed successfully"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi

# Setup environment file
echo ""
echo "5. Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ .env file created from template"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your API keys:"
    echo "   - OPENAI_API_KEY (from https://platform.openai.com)"
    echo "   - GITHUB_TOKEN (from https://github.com/settings/tokens)"
    echo "   - WEATHER_API_KEY (from https://openweathermap.org)"
else
    echo "✓ .env file already exists"
fi

# Validate configuration
echo ""
echo "6. Validating configuration..."
python -c "
try:
    from config import Config
    print('✓ Configuration valid')
except ValueError as e:
    print(f'⚠️  Configuration warning: {e}')
    print('   This is expected if you haven\\'t set API keys yet')
except Exception as e:
    print(f'✗ Configuration error: {e}')
    exit(1)
" || true

# Test import
echo ""
echo "7. Testing imports..."
python -c "
from orchestrator import AIOperationsOrchestrator
from agents import PlannerAgent, ExecutorAgent, VerifierAgent
from tools import GitHubTool, WeatherTool
print('✓ All imports successful')
" 2>/dev/null

if [[ $? -eq 0 ]]; then
    echo "✓ Imports validated"
else
    echo "⚠️  Import test skipped (API keys may be needed)"
fi

# Summary
echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "📋 Next Steps:"
echo "1. Edit .env with your API keys"
echo "2. Read QUICK_START.md for usage"
echo "3. Try a simple command:"
echo ""
echo "   python cli.py \"Get weather in London\""
echo ""
echo "Documentation:"
echo "  - QUICK_START.md    - Fast setup guide"
echo "  - README.md         - Complete reference"
echo "  - ARCHITECTURE.md   - Design overview"
echo "  - EXAMPLES.md       - Working examples"
echo ""
