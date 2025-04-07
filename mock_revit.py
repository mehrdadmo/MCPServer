from dataclasses import dataclass
from typing import List, Dict, Any
import json

@dataclass
class MockElement:
    id: str
    type: str
    parameters: Dict[str, Any]

class MockRevitEnvironment:
    def __init__(self):
        self.elements = []
        self.selected_elements = []
        
    def add_element(self, element_type: str, parameters: Dict[str, Any]) -> MockElement:
        element = MockElement(
            id=f"mock_{len(self.elements)}",
            type=element_type,
            parameters=parameters
        )
        self.elements.append(element)
        return element
    
    def select_element(self, element: MockElement):
        self.selected_elements.append(element)
    
    def get_selected_elements(self) -> List[MockElement]:
        return self.selected_elements
    
    def clear_selection(self):
        self.selected_elements = []
    
    def get_element_info(self, element: MockElement) -> Dict[str, Any]:
        return {
            "id": element.id,
            "type": element.type,
            "parameters": element.parameters
        }

# Create a test environment
mock_revit = MockRevitEnvironment()

# Add some sample elements
sample_wall = mock_revit.add_element(
    "Wall",
    {
        "Length": 5000,
        "Height": 3000,
        "Width": 200,
        "Material": "Concrete"
    }
)

sample_door = mock_revit.add_element(
    "Door",
    {
        "Width": 1000,
        "Height": 2100,
        "Material": "Wood"
    }
)

# Select some elements
mock_revit.select_element(sample_wall)
mock_revit.select_element(sample_door) 