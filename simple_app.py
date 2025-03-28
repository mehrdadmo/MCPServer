from fastapi import FastAPI, HTTPException, WebSocket
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn

# Create FastAPI app with explicit docs URLs
app = FastAPI(
    title="Claude MCP Revit Server",
    docs_url="/",  # Swagger UI at root
    redoc_url="/redoc"  # ReDoc at /redoc
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

@app.get("/hello")
async def hello():
    return {"message": "Hello World!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/process_revit_query", response_model=RevitResponse)
async def process_revit_query(request: RevitRequest):
    try:
        # For now, return mock response
        response = {
            "response": "This is a mock response. Claude API integration pending.",
            "suggested_actions": ["Action 1", "Action 2"]
        }
        
        return RevitResponse(**response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("Starting server on http://127.0.0.1:8888")
    uvicorn.run(app, host="127.0.0.1", port=8888) 