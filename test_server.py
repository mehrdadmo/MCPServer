from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
import uvicorn
import logging
from dotenv import load_dotenv
import os
from claude_integration import ClaudeIntegration
import json
import asyncio

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    filename=os.getenv("LOG_FILE", "mcp_server.log"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app with docs
app = FastAPI(
    title="Claude MCP Server",
    description="MCP Server for integrating Claude AI with Autodesk Revit",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Claude integration
claude = ClaudeIntegration()

# Data models
class Point2D(BaseModel):
    x: float
    y: float

class ElementParameter(BaseModel):
    name: str
    value: Union[str, float, int, bool]
    
class RevitElement(BaseModel):
    id: str
    name: Optional[str] = None
    category: Optional[str] = None
    type: str
    parameters: Optional[Dict[str, Any]] = {}

class ProjectInfo(BaseModel):
    name: Optional[str] = None
    number: Optional[str] = None
    client: Optional[str] = None
    address: Optional[str] = None

class RevitQueryRequest(BaseModel):
    elements: List[RevitElement]
    project_info: Optional[ProjectInfo] = None
    prompt: Optional[str] = "Analyze these Revit elements"

class RevitQueryResponse(BaseModel):
    response: str
    suggested_actions: Optional[List[str]] = None
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    version: str
    claude_model: str

class Wall(BaseModel):
    start: Point2D
    end: Point2D
    type_id: int
    level_id: int
    
class Level(BaseModel):
    elevation: float
    name: str
    
class Room(BaseModel):
    name: str
    boundary: List[Point2D]
    
class Opening(BaseModel):
    type_id: int
    location: Point2D
    host_id: int
    
class RevitModel(BaseModel):
    levels: List[Level]
    walls: List[Wall]
    rooms: Optional[List[Room]] = Field(default_factory=list)
    openings: Optional[List[Opening]] = Field(default_factory=list)

class ModelGenerationRequest(BaseModel):
    description: str
    requirements: Dict[str, Any]
    version: Optional[str] = "1.0"

class ModelGenerationResponse(BaseModel):
    success: bool
    model_data: RevitModel
    message: str
    error: Optional[str] = None

# WebSocket connections
active_connections: List[WebSocket] = []

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint returning welcome message"""
    return {"message": "Welcome to Claude MCP Server"}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        claude_model=claude.model
    )

@app.post("/process_revit_query", response_model=RevitQueryResponse)
async def process_revit_query(query: RevitQueryRequest):
    """Process Revit-related queries using Claude AI MCP"""
    try:
        logger.info(f"Processing Revit query with {len(query.elements)} elements")
        
        # Prepare prompt for Claude
        elements_description = []
        for element in query.elements:
            element_desc = f"- {element.category} ({element.type}): {element.name} (ID: {element.id})"
            if element.parameters:
                param_list = [f"{k}: {v}" for k, v in element.parameters.items()]
                element_desc += f"\n  Parameters: {', '.join(param_list)}"
            elements_description.append(element_desc)
            
        elements_text = "\n".join(elements_description)
        
        project_info_text = ""
        if query.project_info:
            project_info_text = f"""
Project Information:
- Name: {query.project_info.name}
- Number: {query.project_info.number}
- Client: {query.project_info.client}
- Address: {query.project_info.address}
"""

        # Call Claude with prompt
        prompt = f"""
{query.prompt}

Elements in the Revit model:
{elements_text}

{project_info_text}

Provide a detailed analysis of these elements including any potential issues, improvements, 
or opportunities. Include specific suggestions for actions.
"""

        # For demo purposes, simulate Claude's analysis
        # In production, you would call Claude API here
        analysis = f"Analysis of {len(query.elements)} Revit elements"
        suggestions = []
        
        for element in query.elements:
            if element.category == "Walls":
                suggestions.append(f"Optimize wall thickness for better energy efficiency")
            elif element.category == "Doors":
                suggestions.append(f"Check if door dimensions meet accessibility standards")
            elif element.category == "Windows":
                suggestions.append(f"Consider adding solar shading to south-facing windows")
                
        if not suggestions:
            suggestions = ["Improve documentation", "Check for design consistency", "Verify materials specifications"]
        
        return RevitQueryResponse(
            response=analysis,
            suggested_actions=suggestions,
            error=None
        )
        
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

@app.post("/generate_revit_model", response_model=ModelGenerationResponse)
async def generate_revit_model(request: ModelGenerationRequest):
    """Generate Revit model based on natural language description using Claude MCP"""
    try:
        logger.info(f"Generating Revit model for: {request.description}")
        
        # Generate model using Claude MCP
        model_data = await claude.generate_model(
            description=request.description,
            requirements=request.requirements
        )
        
        # Convert model data to Pydantic model for validation
        revit_model = RevitModel(**model_data)
        
        return ModelGenerationResponse(
            success=True,
            model_data=revit_model,
            message="Model generated successfully",
            error=None
        )
        
    except Exception as e:
        logger.error(f"Error generating model: {str(e)}")
        return ModelGenerationResponse(
            success=False,
            model_data=RevitModel(levels=[], walls=[]),
            message="Failed to generate model",
            error=str(e)
        )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run("test_server:app", host=host, port=port, reload=True) 