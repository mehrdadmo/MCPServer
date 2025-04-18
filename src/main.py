from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
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

# Initialize FastAPI app
app = FastAPI(
    title="Claude MCP Revit Server",
    description="Server for integrating Claude AI with Autodesk Revit",
    version=os.getenv("REVIT_PLUGIN_VERSION", "1.0.0")
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

# WebSocket connections
active_connections: List[WebSocket] = []

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the Claude MCP Revit Server")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the Claude MCP Revit Server")

@app.get("/")
async def root():
    return {"message": "Welcome to Claude MCP Revit Server"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/process_revit_query", response_model=RevitResponse)
async def process_revit_query(request: RevitRequest):
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