from fastapi import FastAPI, HTTPException, WebSocket
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import logging
from dotenv import load_dotenv
import os
from claude_integration import ClaudeIntegration

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
    title="Claude MCP Test Server",
    description="Server for integrating Claude AI with Autodesk Revit",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize Claude integration
claude = ClaudeIntegration()

# Data models
class RevitElement(BaseModel):
    id: str
    type: str
    parameters: Dict[str, Any]

class ProjectInfo(BaseModel):
    name: str
    number: str

class RevitQuery(BaseModel):
    prompt: str
    revit_elements: List[RevitElement]
    project_info: ProjectInfo

class RevitResponse(BaseModel):
    response: str
    suggested_actions: List[str]
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str

class ModelGenerationRequest(BaseModel):
    description: str
    requirements: Dict[str, Any]
    constraints: Optional[Dict[str, Any]] = None

class ModelGenerationResponse(BaseModel):
    success: bool
    model_data: Dict[str, Any]
    message: str
    error: Optional[str] = None

# WebSocket connections
active_connections: List[WebSocket] = []

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint returning welcome message"""
    return {"message": "Welcome to Claude MCP Test Server"}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        environment=os.getenv("ENVIRONMENT", "development")
    )

@app.post("/process_revit_query", response_model=RevitResponse)
async def process_revit_query(query: RevitQuery):
    """Process Revit-related queries using Claude AI"""
    try:
        logger.info(f"Processing Revit query: {query.prompt}")
        
        # Simulate Claude's analysis
        analysis = {
            "summary": f"Analysis of {len(query.revit_elements)} Revit elements",
            "elements_analysis": [],
            "recommendations": []
        }
        
        # Analyze each element
        for element in query.revit_elements:
            element_analysis = {
                "id": element.id,
                "type": element.type,
                "analysis": f"Analyzing {element.type} with parameters: {element.parameters}"
            }
            analysis["elements_analysis"].append(element_analysis)
            
            # Add some mock recommendations
            if element.type == "Wall":
                analysis["recommendations"].append(
                    f"Consider optimizing wall thickness for {element.parameters.get('Material', 'unknown material')}"
                )
            elif element.type == "Door":
                analysis["recommendations"].append(
                    f"Check if door dimensions meet accessibility standards"
                )
        
        return RevitResponse(
            response=analysis["summary"],
            suggested_actions=analysis["recommendations"],
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

@app.post("/generate_revit_model", response_model=ModelGenerationResponse)
async def generate_revit_model(request: ModelGenerationRequest):
    """Generate Revit model based on natural language description"""
    try:
        logger.info(f"Generating Revit model for: {request.description}")
        
        # Generate model using Claude
        model_data = await claude.generate_model(
            description=request.description,
            requirements=request.requirements
        )
        
        return ModelGenerationResponse(
            success=True,
            model_data=model_data,
            message="Model generated successfully",
            error=None
        )
        
    except Exception as e:
        logger.error(f"Error generating model: {str(e)}")
        return ModelGenerationResponse(
            success=False,
            model_data={},
            message="Failed to generate model",
            error=str(e)
        )

if __name__ == "__main__":
    print("Starting server on http://127.0.0.1:4000")
    print("API documentation available at http://127.0.0.1:4000/docs")
    uvicorn.run(
        "test_server:app",
        host="127.0.0.1",
        port=4000,
        reload=True
    ) 