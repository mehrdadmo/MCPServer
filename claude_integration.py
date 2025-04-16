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
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-3-opus-20240229"
    
    async def generate_model(self, description: str, requirements: dict) -> dict:
        """Generate a Revit model based on natural language description"""
        try:
            # Prepare the prompt for Claude
            prompt = f"""You are an expert architect and Revit specialist. 
            Please generate a detailed floor plan based on the following requirements:
            
            Description: {description}
            Requirements: {json.dumps(requirements, indent=2)}
            
            Generate a JSON response with the following structure:
            {{
                "levels": [
                    {{
                        "elevation": float,
                        "name": str
                    }}
                ],
                "walls": [
                    {{
                        "start": {{"x": float, "y": float}},
                        "end": {{"x": float, "y": float}},
                        "type_id": int,
                        "level_id": int
                    }}
                ],
                "rooms": [
                    {{
                        "name": str,
                        "boundary": [
                            {{"x": float, "y": float}},
                            ...
                        ]
                    }}
                ],
                "openings": [
                    {{
                        "type_id": int,
                        "location": {{"x": float, "y": float}},
                        "host_id": int
                    }}
                ]
            }}
            
            Ensure all measurements are in meters and the design follows architectural best practices."""

            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )

            # Parse the response
            try:
                design = json.loads(response.content[0].text)
                return design
            except json.JSONDecodeError:
                # If Claude returns a text description instead of JSON,
                # we'll use our fallback floor plan generator
                return self._generate_fallback_floor_plan(requirements)

        except Exception as e:
            print(f"Error generating model with Claude: {str(e)}")
            # Fallback to our basic floor plan generator
            return self._generate_fallback_floor_plan(requirements)

    def _generate_fallback_floor_plan(self, requirements: dict) -> dict:
        """Fallback floor plan generator if Claude fails"""
        # This is a simplified version of the floor plan generator
        # that was previously in test_server.py
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