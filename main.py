"""Main FastAPI application"""
import logging
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from config import Config
from orchestrator import AIOperationsOrchestrator

# Setup logging
logging.basicConfig(level=Config.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="AI Operations Assistant",
    description="Multi-agent system for executing complex tasks",
    version="1.0.0"
)

# Initialize orchestrator
orchestrator = None


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    global orchestrator
    try:
        Config.validate()
        orchestrator = AIOperationsOrchestrator()
        logger.info("AI Operations Assistant initialized successfully")
    except ValueError as e:
        logger.error(f"Failed to initialize: {str(e)}")
        raise


# Request/Response models
class TaskRequest(BaseModel):
    """Task request model"""
    task: str


class TaskResponse(BaseModel):
    """Task response model"""
    status: str
    task: str
    plan: Dict[str, Any]
    execution: Dict[str, Any]
    final_answer: Dict[str, Any]


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Operations Assistant"
    }


@app.post("/process-task", response_model=dict)
async def process_task(request: TaskRequest):
    """
    Process a user task
    
    Args:
        request: Task request with natural language task
        
    Returns:
        Processed result with plan, execution, and final answer
    """
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        logger.info(f"Received task: {request.task}")
        result = orchestrator.process_task(request.task)
        
        return result
    except Exception as e:
        logger.error(f"Error processing task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "AI Operations Assistant",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "process_task": "/process-task (POST)"
        },
        "example_task": "Find the top 5 Python repositories on GitHub with the most stars and get the current weather in San Francisco"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host=Config.SERVER_HOST,
        port=Config.SERVER_PORT,
        log_level=Config.LOG_LEVEL.lower()
    )
