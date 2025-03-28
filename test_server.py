from fastapi import FastAPI, HTTPException, WebSocket
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn
import logging
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    filename=os.getenv("LOG_FILE", "app.log"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app with docs
app = FastAPI(
    title="Claude MCP Revit Server",
    description="Server for integrating Claude AI with Autodesk Revit",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Data models
class RevitRequest(BaseModel):
    prompt: str
    model: str = "claude-3-sonnet"
    revit_elements: Optional[Dict] = None
    project_info: Optional[Dict] = None

class RevitResponse(BaseModel):
    response: str
    suggested_actions: List[str]
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str

# WebSocket connections
active_connections: List[WebSocket] = []

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint returning welcome message"""
    return {"message": "Welcome to Claude MCP Revit Server"}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        environment=os.getenv("ENVIRONMENT", "development")
    )

@app.post("/process_revit_query", response_model=RevitResponse)
async def process_revit_query(request: RevitRequest):
    """Process Revit-related queries using Claude AI"""
    try:
        logger.info(f"Processing Revit query: {request.prompt}")
        
        # TODO: Replace with actual Claude API integration
        # For now, return mock response
        response = {
            "response": "This is a mock response. Claude API integration pending.",
            "suggested_actions": ["Action 1", "Action 2"]
        }
        
        return RevitResponse(**response)
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication"""
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Process the received data
            response = f"Received: {data}"
            await websocket.send_text(response)
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
    finally:
        active_connections.remove(websocket)

@app.get("/api/revit/elements", response_model=Dict)
async def get_revit_elements():
    """Get available Revit elements"""
    return {
        "walls": ["Basic Wall", "Curtain Wall", "Stacked Wall"],
        "floors": ["Basic Floor", "Slab", "Foundation"],
        "roofs": ["Basic Roof", "Extrusion Roof"]
    }

@app.get("/api/revit/properties", response_model=Dict)
async def get_revit_properties():
    """Get available Revit properties"""
    return {
        "dimensions": ["Length", "Width", "Height", "Area"],
        "materials": ["Concrete", "Steel", "Wood", "Glass"],
        "parameters": ["Mark", "Comments", "Phase"]
    }

if __name__ == "__main__":
    print("Starting server on http://127.0.0.1:4000")
    print("API documentation available at http://127.0.0.1:4000/docs")
    uvicorn.run(
        "test_server:app",
        host="127.0.0.1",
        port=4000,
        reload=True
    ) 