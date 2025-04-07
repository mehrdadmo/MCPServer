import asyncio
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Mock Claude integration for testing
class MockClaudeIntegration:
    async def extract_requirements(self, description: str):
        """Mock implementation of requirements extraction"""
        print(f"Extracting requirements from: {description}")
        return {
            "total_area": 80,
            "rooms": [
                {
                    "type": "bedroom",
                    "count": 2,
                    "min_area": 12,
                    "max_area": 15
                },
                {
                    "type": "bathroom",
                    "count": 1,
                    "min_area": 5,
                    "max_area": 8
                },
                {
                    "type": "kitchen",
                    "count": 1,
                    "min_area": 8,
                    "max_area": 12
                },
                {
                    "type": "living_room",
                    "count": 1,
                    "min_area": 20,
                    "max_area": 25
                }
            ],
            "style": "modern minimalist",
            "constraints": {
                "min_room_area": 5,
                "max_room_area": 25,
                "ceiling_height": 2.8
            }
        }
    
    async def generate_model(self, description: str, requirements: dict):
        """Mock implementation of model generation"""
        print(f"Generating model for: {description}")
        print(f"With requirements: {json.dumps(requirements, indent=2)}")
        
        return {
            "rooms": [
                {
                    "name": "Bedroom 1",
                    "area": 14,
                    "dimensions": {"length": 4, "width": 3.5},
                    "location": {"x": 0, "y": 0, "z": 0},
                    "elements": [
                        {
                            "type": "wall",
                            "parameters": {
                                "Length": 4,
                                "Height": 2.8,
                                "Width": 0.2,
                                "Material": "Drywall",
                                "Location": {"x": 0, "y": 0, "z": 0}
                            }
                        }
                    ],
                    "connections": [
                        {
                            "from": "Bedroom 1",
                            "to": "Living Room",
                            "type": "door"
                        }
                    ]
                },
                {
                    "name": "Bedroom 2",
                    "area": 13,
                    "dimensions": {"length": 3.8, "width": 3.4},
                    "location": {"x": 5, "y": 0, "z": 0},
                    "elements": [
                        {
                            "type": "wall",
                            "parameters": {
                                "Length": 3.8,
                                "Height": 2.8,
                                "Width": 0.2,
                                "Material": "Drywall",
                                "Location": {"x": 5, "y": 0, "z": 0}
                            }
                        }
                    ],
                    "connections": [
                        {
                            "from": "Bedroom 2",
                            "to": "Living Room",
                            "type": "door"
                        }
                    ]
                },
                {
                    "name": "Bathroom",
                    "area": 6,
                    "dimensions": {"length": 3, "width": 2},
                    "location": {"x": 0, "y": 5, "z": 0},
                    "elements": [
                        {
                            "type": "wall",
                            "parameters": {
                                "Length": 3,
                                "Height": 2.8,
                                "Width": 0.2,
                                "Material": "Tile",
                                "Location": {"x": 0, "y": 5, "z": 0}
                            }
                        }
                    ],
                    "connections": [
                        {
                            "from": "Bathroom",
                            "to": "Living Room",
                            "type": "door"
                        }
                    ]
                },
                {
                    "name": "Kitchen",
                    "area": 10,
                    "dimensions": {"length": 4, "width": 2.5},
                    "location": {"x": 5, "y": 5, "z": 0},
                    "elements": [
                        {
                            "type": "wall",
                            "parameters": {
                                "Length": 4,
                                "Height": 2.8,
                                "Width": 0.2,
                                "Material": "Drywall",
                                "Location": {"x": 5, "y": 5, "z": 0}
                            }
                        }
                    ],
                    "connections": [
                        {
                            "from": "Kitchen",
                            "to": "Living Room",
                            "type": "open"
                        }
                    ]
                },
                {
                    "name": "Living Room",
                    "area": 22,
                    "dimensions": {"length": 5.5, "width": 4},
                    "location": {"x": 2.5, "y": 2.5, "z": 0},
                    "elements": [
                        {
                            "type": "wall",
                            "parameters": {
                                "Length": 5.5,
                                "Height": 2.8,
                                "Width": 0.2,
                                "Material": "Drywall",
                                "Location": {"x": 2.5, "y": 2.5, "z": 0}
                            }
                        }
                    ],
                    "connections": []
                }
            ],
            "walls": [
                {
                    "start_point": {"x": 0, "y": 0, "z": 0},
                    "end_point": {"x": 4, "y": 0, "z": 0},
                    "height": 2.8,
                    "type": "Interior",
                    "material": "Drywall"
                },
                {
                    "start_point": {"x": 4, "y": 0, "z": 0},
                    "end_point": {"x": 4, "y": 3.5, "z": 0},
                    "height": 2.8,
                    "type": "Interior",
                    "material": "Drywall"
                },
                {
                    "start_point": {"x": 4, "y": 3.5, "z": 0},
                    "end_point": {"x": 0, "y": 3.5, "z": 0},
                    "height": 2.8,
                    "type": "Interior",
                    "material": "Drywall"
                },
                {
                    "start_point": {"x": 0, "y": 3.5, "z": 0},
                    "end_point": {"x": 0, "y": 0, "z": 0},
                    "height": 2.8,
                    "type": "Interior",
                    "material": "Drywall"
                }
            ],
            "openings": [
                {
                    "type": "door",
                    "location": {"x": 1.5, "y": 0, "z": 0},
                    "width": 0.9,
                    "height": 2.1,
                    "wall_id": "wall1"
                },
                {
                    "type": "door",
                    "location": {"x": 0, "y": 1.5, "z": 0},
                    "width": 0.9,
                    "height": 2.1,
                    "wall_id": "wall4"
                },
                {
                    "type": "window",
                    "location": {"x": 2, "y": 3.5, "z": 1.2},
                    "width": 1.5,
                    "height": 1.2,
                    "wall_id": "wall3"
                }
            ],
            "total_area": 80,
            "layout": "open plan with bedrooms on one side",
            "materials": [
                {
                    "name": "Drywall",
                    "type": "wall",
                    "properties": {
                        "thickness": 0.2,
                        "color": "white"
                    }
                },
                {
                    "name": "Tile",
                    "type": "floor",
                    "properties": {
                        "thickness": 0.02,
                        "color": "gray"
                    }
                }
            ],
            "metadata": {
                "description": "Modern apartment with 2 bedrooms and open living space",
                "style": "modern minimalist",
                "constraints": {
                    "min_room_area": 5,
                    "max_room_area": 25,
                    "ceiling_height": 2.8
                }
            }
        }

async def test_ai_design():
    """Test the AI design generation functionality"""
    try:
        # Initialize Claude integration
        claude = MockClaudeIntegration()
        
        # Test description
        description = """
        Design a modern apartment with:
        - 2 bedrooms
        - 1 bathroom
        - Open kitchen and living room
        - Total area of 80 square meters
        - Large windows for natural light
        - Modern minimalist style
        """
        
        print("Extracting requirements...")
        requirements = await claude.extract_requirements(description)
        print("\nExtracted Requirements:")
        print(json.dumps(requirements, indent=2))
        
        print("\nGenerating design...")
        model_data = await claude.generate_model(description, requirements)
        print("\nGenerated Model Data:")
        print(json.dumps(model_data, indent=2))
        
        print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"Error during test: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_ai_design()) 