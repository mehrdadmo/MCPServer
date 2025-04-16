from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import logging
from dotenv import load_dotenv
import os
from claude_integration import ClaudeIntegration
import json
import random

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

class DesignRequirements(BaseModel):
    area: float
    bedrooms: int
    bathrooms: int
    style: str
    additional_requirements: str

class DesignRequest(BaseModel):
    action: str
    requirements: DesignRequirements

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

def generate_floor_plan(requirements: DesignRequirements) -> Dict[str, Any]:
    # Calculate room sizes based on total area
    total_area = requirements.area
    bedroom_area = total_area * 0.3 / requirements.bedrooms
    bathroom_area = total_area * 0.2 / requirements.bathrooms
    living_area = total_area * 0.5

    # Generate walls
    walls = []
    wall_types = {
        "exterior": 1,
        "interior": 2
    }

    # Create exterior walls
    length = (total_area ** 0.5) * 1.2  # Approximate length of the house
    width = total_area / length

    # Exterior walls
    walls.extend([
        {"start": {"x": 0, "y": 0}, "end": {"x": length, "y": 0}, "type_id": wall_types["exterior"], "level_id": 1},
        {"start": {"x": length, "y": 0}, "end": {"x": length, "y": width}, "type_id": wall_types["exterior"], "level_id": 1},
        {"start": {"x": length, "y": width}, "end": {"x": 0, "y": width}, "type_id": wall_types["exterior"], "level_id": 1},
        {"start": {"x": 0, "y": width}, "end": {"x": 0, "y": 0}, "type_id": wall_types["exterior"], "level_id": 1}
    ])

    # Create interior walls for bedrooms
    bedroom_width = (bedroom_area ** 0.5) * 0.8
    bedroom_length = bedroom_area / bedroom_width

    for i in range(requirements.bedrooms):
        x_offset = length * 0.2 + i * (bedroom_length + 2)
        walls.extend([
            {"start": {"x": x_offset, "y": 0}, "end": {"x": x_offset, "y": bedroom_width}, "type_id": wall_types["interior"], "level_id": 1},
            {"start": {"x": x_offset, "y": bedroom_width}, "end": {"x": x_offset + bedroom_length, "y": bedroom_width}, "type_id": wall_types["interior"], "level_id": 1},
            {"start": {"x": x_offset + bedroom_length, "y": bedroom_width}, "end": {"x": x_offset + bedroom_length, "y": 0}, "type_id": wall_types["interior"], "level_id": 1}
        ])

    # Create rooms
    rooms = []
    for i in range(requirements.bedrooms):
        x_offset = length * 0.2 + i * (bedroom_length + 2)
        rooms.append({
            "name": f"Bedroom {i+1}",
            "boundary": [
                {"x": x_offset, "y": 0},
                {"x": x_offset + bedroom_length, "y": 0},
                {"x": x_offset + bedroom_length, "y": bedroom_width},
                {"x": x_offset, "y": bedroom_width}
            ]
        })

    # Create bathroom
    bathroom_width = (bathroom_area ** 0.5) * 0.8
    bathroom_length = bathroom_area / bathroom_width
    x_offset = length * 0.8
    rooms.append({
        "name": "Bathroom",
        "boundary": [
            {"x": x_offset, "y": width - bathroom_width},
            {"x": x_offset + bathroom_length, "y": width - bathroom_width},
            {"x": x_offset + bathroom_length, "y": width},
            {"x": x_offset, "y": width}
        ]
    })

    # Create openings (doors and windows)
    openings = []
    door_type = 3  # Assuming this is the door type ID
    window_type = 4  # Assuming this is the window type ID

    # Add doors to bedrooms
    for i in range(requirements.bedrooms):
        x_offset = length * 0.2 + i * (bedroom_length + 2)
        openings.append({
            "type_id": door_type,
            "location": {"x": x_offset + bedroom_length/2, "y": 0},
            "host_id": walls[i*3]["type_id"]  # Reference to the wall
        })

    # Add windows
    window_spacing = length / 4
    for i in range(3):  # Add 3 windows to exterior walls
        openings.append({
            "type_id": window_type,
            "location": {"x": window_spacing * (i+1), "y": 0},
            "host_id": walls[0]["type_id"]
        })

    return {
        "levels": [{"elevation": 0}],
        "walls": walls,
        "rooms": rooms,
        "openings": openings
    }

@app.post("/generate")
async def generate_design(request: DesignRequest):
    if request.action != "generate_design":
        raise HTTPException(status_code=400, detail="Invalid action")

    try:
        design = generate_floor_plan(request.requirements)
        return {
            "status": "success",
            "design": design,
            "message": f"Generated {request.requirements.style} style design with {request.requirements.bedrooms} bedrooms and {request.requirements.bathrooms} bathrooms"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("Starting Claude MCP Test Server...")
    print("Server will be available at: http://localhost:8000")
    print("API documentation available at: http://localhost:8000/docs")
    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        print(f"Error starting server: {str(e)}")
        print("Please check if port 8000 is available and try again.") 