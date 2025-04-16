from anthropic import Anthropic, AnthropicBedrock
import os
from typing import Dict, Any, List
import json
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename=os.path.join(os.path.dirname(__file__), 'claude_mcp.log'),
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ClaudeIntegration:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
            
        self.client = Anthropic(api_key=api_key)
        self.model = os.getenv("CLAUDE_MODEL", "claude-3-opus-20240229")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "4000"))
        logger.info(f"Claude Integration initialized with model: {self.model}")
    
    async def generate_model(self, description: str, requirements: dict) -> dict:
        """Generate a Revit model based on natural language description using Claude MCP"""
        try:
            # Prepare the MCP context for Claude
            tools = [{
                "name": "revit_model_generator",
                "description": "Tool for generating Revit models from natural language",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "levels": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "elevation": {"type": "number"},
                                    "name": {"type": "string"}
                                },
                                "required": ["elevation", "name"]
                            }
                        },
                        "walls": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "start": {
                                        "type": "object",
                                        "properties": {
                                            "x": {"type": "number"},
                                            "y": {"type": "number"}
                                        },
                                        "required": ["x", "y"]
                                    },
                                    "end": {
                                        "type": "object",
                                        "properties": {
                                            "x": {"type": "number"},
                                            "y": {"type": "number"}
                                        },
                                        "required": ["x", "y"]
                                    },
                                    "type_id": {"type": "integer"},
                                    "level_id": {"type": "integer"}
                                },
                                "required": ["start", "end", "type_id", "level_id"]
                            }
                        },
                        "rooms": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "boundary": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "x": {"type": "number"},
                                                "y": {"type": "number"}
                                            },
                                            "required": ["x", "y"]
                                        }
                                    }
                                },
                                "required": ["name", "boundary"]
                            }
                        },
                        "openings": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "type_id": {"type": "integer"},
                                    "location": {
                                        "type": "object",
                                        "properties": {
                                            "x": {"type": "number"},
                                            "y": {"type": "number"}
                                        },
                                        "required": ["x", "y"]
                                    },
                                    "host_id": {"type": "integer"}
                                },
                                "required": ["type_id", "location", "host_id"]
                            }
                        }
                    },
                    "required": ["levels", "walls"]
                }
            }]

            # Prepare the prompt for Claude
            prompt = f"""You are an expert architect and Revit specialist. 
            Please generate a detailed floor plan based on the following requirements:
            
            Description: {description}
            Requirements: {json.dumps(requirements, indent=2)}
            
            Use the revit_model_generator tool to generate a structured model that can be imported into Revit.
            The model should include levels, walls, rooms, and openings.
            
            Ensure all measurements are in meters and the design follows architectural best practices.
            """

            # Call Claude API with tool use
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                tools=tools,
                messages=[{"role": "user", "content": prompt}]
            )

            # Parse the tool use response
            tool_outputs = []
            for content in response.content:
                if content.type == "tool_use":
                    tool_outputs.append(content.input)

            # If we got tool output, return it
            if tool_outputs:
                return tool_outputs[0]
            
            # Otherwise, parse text response as JSON (fallback)
            try:
                for content in response.content:
                    if content.type == "text":
                        # Find JSON in the text
                        text = content.text
                        start = text.find('{')
                        end = text.rfind('}') + 1
                        if start != -1 and end != 0:
                            json_str = text[start:end]
                            return json.loads(json_str)
                
                # If no JSON found, use fallback
                return self._generate_fallback_floor_plan(requirements)
            except json.JSONDecodeError:
                return self._generate_fallback_floor_plan(requirements)

        except Exception as e:
            logger.error(f"Error generating model with Claude: {str(e)}")
            # Fallback to our basic floor plan generator
            return self._generate_fallback_floor_plan(requirements)

    def _generate_fallback_floor_plan(self, requirements: dict) -> dict:
        """Fallback floor plan generator if Claude fails"""
        # This is a simplified version of the floor plan generator
        total_area = requirements.get("area", 120)
        bedrooms = requirements.get("bedrooms", 2)
        bathrooms = requirements.get("bathrooms", 1)

        # Calculate dimensions
        length = (total_area ** 0.5) * 1.2
        width = total_area / length

        # Create basic floor plan
        return {
            "levels": [{"elevation": 0, "name": "Level 1"}],
            "walls": [
                {"start": {"x": 0, "y": 0}, "end": {"x": length, "y": 0}, "type_id": 1, "level_id": 1},
                {"start": {"x": length, "y": 0}, "end": {"x": length, "y": width}, "type_id": 1, "level_id": 1},
                {"start": {"x": length, "y": width}, "end": {"x": 0, "y": width}, "type_id": 1, "level_id": 1},
                {"start": {"x": 0, "y": width}, "end": {"x": 0, "y": 0}, "type_id": 1, "level_id": 1}
            ],
            "rooms": [],
            "openings": []
        }
    
    async def extract_requirements(self, description: str) -> Dict[str, Any]:
        """Extract requirements from natural language description using Claude"""
        try:
            # Define schema for requirements extraction
            tools = [{
                "name": "extract_requirements",
                "description": "Extract architectural requirements from natural language description",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "total_area": {"type": "number"},
                        "rooms": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "type": {"type": "string"},
                                    "count": {"type": "integer"},
                                    "min_area": {"type": "number"},
                                    "max_area": {"type": "number"}
                                },
                                "required": ["type", "count"]
                            }
                        },
                        "style": {"type": "string"},
                        "constraints": {
                            "type": "object",
                            "properties": {
                                "min_room_area": {"type": "number"},
                                "max_room_area": {"type": "number"},
                                "ceiling_height": {"type": "number"}
                            }
                        }
                    },
                    "required": ["total_area", "rooms"]
                }
            }]
            
            prompt = f"""
            Extract architectural requirements from the following description:
            
            {description}
            
            Use the extract_requirements tool to provide a structured representation of the requirements.
            """
            
            # Call Claude API with tool use
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                tools=tools,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse the tool use response
            tool_outputs = []
            for content in response.content:
                if content.type == "tool_use":
                    tool_outputs.append(content.input)
            
            # If we got tool output, return it
            if tool_outputs:
                return tool_outputs[0]
            
            # Fallback to parsing text
            default_requirements = {
                "total_area": 120,
                "rooms": [
                    {"type": "bedroom", "count": 2, "min_area": 15},
                    {"type": "bathroom", "count": 1, "min_area": 8},
                    {"type": "living_room", "count": 1, "min_area": 30}
                ],
                "style": "modern",
                "constraints": {
                    "min_room_area": 8,
                    "ceiling_height": 2.4
                }
            }
            
            return default_requirements
            
        except Exception as e:
            logger.error(f"Error extracting requirements: {str(e)}")
            # Return default requirements
            return {
                "total_area": 120,
                "rooms": [
                    {"type": "bedroom", "count": 2, "min_area": 15},
                    {"type": "bathroom", "count": 1, "min_area": 8},
                    {"type": "living_room", "count": 1, "min_area": 30}
                ],
                "style": "modern",
                "constraints": {
                    "min_room_area": 8,
                    "ceiling_height": 2.4
                }
            } 