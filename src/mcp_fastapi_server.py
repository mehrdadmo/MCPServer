from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from anthropic import Anthropic
import os
from dotenv import load_dotenv
from typing import List, Optional, Dict

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Claude MCP Revit Server")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Anthropic client
anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

class RevitRequest(BaseModel):
    prompt: str
    model: str = "claude-3-sonnet"
    revit_elements: Optional[Dict] = None
    project_info: Optional[Dict] = None

class RevitResponse(BaseModel):
    response: str
    suggested_actions: List[str]
    error: Optional[str] = None

@app.post("/process_revit_query", response_model=RevitResponse)
async def process_revit_query(request: RevitRequest):
    try:
        # Construct the system prompt
        system_prompt = """You are an expert in Autodesk Revit and architectural design. 
        Analyze the provided information and suggest appropriate actions or modifications."""
        
        # Combine project info and elements with user prompt
        context = f"""
        Project Information: {request.project_info}
        Revit Elements: {request.revit_elements}
        User Query: {request.prompt}
        """

        # Call Claude API
        message = anthropic.messages.create(
            model=request.model,
            max_tokens=1000,
            system=system_prompt,
            messages=[
                {"role": "user", "content": context}
            ]
        )

        # Process the response
        suggested_actions = extract_suggested_actions(message.content)

        return RevitResponse(
            response=message.content,
            suggested_actions=suggested_actions
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def extract_suggested_actions(response: str) -> List[str]:
    # Implement logic to extract actionable items from Claude's response
    # This is a placeholder implementation
    return ["Action 1", "Action 2"]

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 