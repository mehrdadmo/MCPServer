from openai import OpenAI
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ValidationError
from typing import List, Optional

# Configuration
NVIDIA_API_KEY = "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"
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"

# Debug: Print to verify API Key
print("Using NVIDIA_API_KEY:", NVIDIA_API_KEY)

# Initialize Nvidia OpenAI-compatible client
try:
    client = OpenAI(
        base_url=NVIDIA_BASE_URL,
        api_key=NVIDIA_API_KEY
    )
except Exception as e:
    raise RuntimeError(f"Failed to initialize OpenAI client: {e}")

# FastAPI Application
app = FastAPI(
    title="NeuroPedagogy AI",
    description="Transformative AI-Powered Learning Ecosystem",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Data Models
class Message(BaseModel):
    role: str
    content: str

class LearningContext(BaseModel):
    subject: Optional[str] = "General Education"
    difficulty_level: Optional[str] = "intermediate"
    learning_style: Optional[str] = "adaptive"

class AIAssistantRequest(BaseModel):
    messages: List[Message]
    context: Optional[LearningContext] = LearningContext()

# Educational AI Assistant Endpoint
@app.post("/ai-tutor/chat")
async def educational_chat(request: AIAssistantRequest):
    """
    Intelligent conversational learning endpoint
    Dynamically adapts responses based on educational context.
    """
    try:
        # Construct enriched prompt with contextual learning parameters
        enriched_messages = [
            {"role": "system", "content": f"""
            You are an advanced AI educational assistant specialized in {request.context.subject}. 
            Adapt explanations for {request.context.difficulty_level} learners.
            Learning Style: {request.context.learning_style}

            Core Teaching Principles:
            - Break complex concepts into digestible insights
            - Provide real-world, contextual examples
            - Encourage critical thinking
            - Generate follow-up exploratory questions
            """}
        ] + [msg.dict() for msg in request.messages]

        # Call Nemotron API
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=enriched_messages,
            temperature=0.7,
            top_p=0.9,
            max_tokens=1024,
            stream=True
        )

        # Stream-based response generation
        generated_content = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                generated_content += chunk.choices[0].delta.content

        return {
            "response": generated_content,
            "context": request.context.dict(),
            "tokens_used": len(generated_content.split())
        }

    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=f"Validation Error: {ve}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating educational chat: {e}")

# WebSocket Streaming Endpoint for Real-time Learning
@app.websocket("/ai-tutor/stream")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time educational AI interactions.
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            request = AIAssistantRequest(**data)
            
            # Similar streaming logic as HTTP endpoint
            completion = client.chat.completions.create(
                model="nvidia/llama-3.1-nemotron-70b-instruct",
                messages=[msg.dict() for msg in request.messages],
                temperature=0.7,
                stream=True
            )

            for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    await websocket.send_text(chunk.choices[0].delta.content)

    except WebSocketDisconnect:
        print("WebSocket connection closed.")
    except ValidationError as ve:
        await websocket.send_text(f"Validation Error: {ve}")
    except Exception as e:
        await websocket.send_text(f"Error during WebSocket communication: {e}")

# Telemetry and Health Check Endpoint
@app.get("/health")
def health_check():
    """
    Check the operational status of the AI system.
    """
    return {
        "status": "Cognitive Ecosystem Operational",
        "model": "Nvidia Nemotron 70B",
        "capabilities": [
            "Adaptive Learning",
            "Contextual Understanding", 
            "Real-time Knowledge Transmission"
        ]
    }
