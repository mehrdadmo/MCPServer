import requests
import json

def test_model_generation():
    print("Testing Revit Model Generation...")
    
    # Prepare the request payload
    payload = {
        "description": "I want a 3 bedroom house with kitchen and living room in 180 square meter",
        "requirements": {
            "total_area": 180,
            "rooms": [
                {"type": "bedroom", "count": 3},
                {"type": "kitchen", "count": 1},
                {"type": "living_room", "count": 1}
            ],
            "style": "modern"
        },
        "constraints": {
            "min_room_area": 15,
            "max_room_area": 40,
            "ceiling_height": 3.0
        }
    }
    
    try:
        # Send request to FastAPI server
        response = requests.post(
            "http://127.0.0.1:4000/generate_revit_model",
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\nModel Generation Results:")
            print(json.dumps(result, indent=2))
            
            if result["success"]:
                print("\nModel Data:")
                print(json.dumps(result["model_data"], indent=2))
            else:
                print(f"\nError: {result.get('error', 'Unknown error')}")
        else:
            print(f"\nError: Server returned status code {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the FastAPI server. Make sure it's running on http://127.0.0.1:4000")
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    test_model_generation() 