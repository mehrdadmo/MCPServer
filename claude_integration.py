from anthropic import Anthropic
import os
from typing import Dict, Any, List
import json
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClaudeIntegration:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        self.client = Anthropic(api_key=api_key)
    
    async def generate_model(self, description: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Revit model data using Claude"""
        try:
            prompt = self._create_model_generation_prompt(description, requirements)
            response = await self._get_claude_response(prompt)
            return self._parse_model_response(response)
        except Exception as e:
            logger.error(f"Error generating model: {str(e)}")
            raise
    
    def _create_model_generation_prompt(self, description: str, requirements: Dict[str, Any]) -> str:
        """Create a detailed prompt for Claude"""
        return f"""
        You are an expert architectural designer working with Revit.
        Generate a detailed Revit model specification based on the following description and requirements.
        
        Description: {description}
        Requirements: {json.dumps(requirements, indent=2)}
        
        Generate a complete Revit model specification in the following JSON format:
        {{
            "rooms": [
                {{
                    "name": "string",
                    "area": number,
                    "dimensions": {{"length": number, "width": number}},
                    "location": {{"x": number, "y": number, "z": number}},
                    "elements": [
                        {{
                            "type": "string",
                            "parameters": {{
                                "Length": number,
                                "Height": number,
                                "Width": number,
                                "Material": "string",
                                "Location": {{"x": number, "y": number, "z": number}}
                            }}
                        }}
                    ],
                    "connections": [
                        {{
                            "from": "string",
                            "to": "string",
                            "type": "string"
                        }}
                    ]
                }}
            ],
            "walls": [
                {{
                    "start_point": {{"x": number, "y": number, "z": number}},
                    "end_point": {{"x": number, "y": number, "z": number}},
                    "height": number,
                    "type": "string",
                    "material": "string"
                }}
            ],
            "openings": [
                {{
                    "type": "string",
                    "location": {{"x": number, "y": number, "z": number}},
                    "width": number,
                    "height": number,
                    "wall_id": "string"
                }}
            ],
            "total_area": number,
            "layout": "string",
            "materials": [
                {{
                    "name": "string",
                    "type": "string",
                    "properties": {{...}}
                }}
            ],
            "metadata": {{
                "description": "string",
                "style": "string",
                "constraints": {{...}}
            }}
        }}
        
        Guidelines:
        1. Ensure all dimensions are in millimeters
        2. Use standard room sizes and proportions
        3. Include all necessary structural elements
        4. Specify appropriate materials for each element
        5. Ensure proper room connections and flow
        6. Maintain the total area requirement
        7. Follow modern architectural standards
        8. Include doors and windows in appropriate locations
        9. Consider furniture placement
        10. Ensure the design is practical and buildable
        """
    
    async def _get_claude_response(self, prompt: str) -> str:
        """Get response from Claude API"""
        try:
            response = await self.client.messages.create(
                model="claude-3-sonnet",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Error getting Claude response: {str(e)}")
            raise
    
    def _parse_model_response(self, response: str) -> Dict[str, Any]:
        """Parse Claude's response into structured data"""
        try:
            # Extract JSON from response
            json_str = response[response.find("{"):response.rfind("}")+1]
            model_data = json.loads(json_str)
            
            # Validate required fields
            self._validate_model_data(model_data)
            
            return model_data
        except Exception as e:
            logger.error(f"Error parsing model response: {str(e)}")
            raise
    
    def _validate_model_data(self, data: Dict[str, Any]):
        """Validate the generated model data"""
        required_fields = ["rooms", "walls", "openings", "total_area", "layout", "materials", "metadata"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate rooms
        for room in data["rooms"]:
            required_room_fields = ["name", "area", "dimensions", "location", "elements"]
            for field in required_room_fields:
                if field not in room:
                    raise ValueError(f"Missing required field in room: {field}")
            
            # Validate dimensions
            if not all(k in room["dimensions"] for k in ["length", "width"]):
                raise ValueError("Invalid room dimensions")
            
            # Validate elements
            for element in room["elements"]:
                if not all(k in element for k in ["type", "parameters"]):
                    raise ValueError("Invalid element specification")
        
        # Validate walls
        for wall in data["walls"]:
            required_wall_fields = ["start_point", "end_point", "height", "type"]
            for field in required_wall_fields:
                if field not in wall:
                    raise ValueError(f"Missing required field in wall: {field}")
        
        # Validate openings
        for opening in data["openings"]:
            required_opening_fields = ["type", "location", "width", "height"]
            for field in required_opening_fields:
                if field not in opening:
                    raise ValueError(f"Missing required field in opening: {field}")
    
    async def extract_requirements(self, description: str) -> Dict[str, Any]:
        """Extract requirements from natural language description"""
        try:
            prompt = f"""
            Extract architectural requirements from the following description:
            
            {description}
            
            Return a JSON object with the following structure:
            {{
                "total_area": number,
                "rooms": [
                    {{
                        "type": "string",
                        "count": number,
                        "min_area": number,
                        "max_area": number
                    }}
                ],
                "style": "string",
                "constraints": {{
                    "min_room_area": number,
                    "max_room_area": number,
                    "ceiling_height": number
                }}
            }}
            """
            
            response = await self._get_claude_response(prompt)
            
            # Extract JSON from response
            json_str = response[response.find("{"):response.rfind("}")+1]
            requirements = json.loads(json_str)
            
            return requirements
        except Exception as e:
            logger.error(f"Error extracting requirements: {str(e)}")
            raise 