import requests
import json
from typing import Dict, Any

def test_design_generation() -> None:
    url = "http://localhost:8000/generate"
    
    # Test data
    data = {
        "action": "generate_design",
        "requirements": {
            "area": 120,
            "bedrooms": 2,
            "bathrooms": 1,
            "style": "Modern",
            "additional_requirements": "Open plan living area with large windows"
        }
    }
    
    try:
        print("Sending design request to server...")
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            print("\nDesign generated successfully!")
            print(f"Message: {result['message']}")
            
            # Print design details
            design = result['design']
            print("\nDesign Details:")
            print(f"Levels: {len(design['levels'])}")
            print(f"Walls: {len(design['walls'])}")
            print(f"Rooms: {len(design['rooms'])}")
            print(f"Openings: {len(design['openings'])}")
            
            # Save design to file
            with open('generated_design.json', 'w') as f:
                json.dump(design, f, indent=2)
            print("\nDesign saved to 'generated_design.json'")
            
        else:
            print(f"\nError: Server returned status code {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to server")
        print("Please make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    print("Claude MCP Test Client")
    print("======================")
    test_design_generation() 