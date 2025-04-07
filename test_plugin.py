import requests
from mock_revit import mock_revit
import json

def test_revit_plugin():
    # Simulate Revit plugin functionality
    print("Testing Revit Plugin Integration...")
    
    # Get selected elements
    selected_elements = mock_revit.get_selected_elements()
    print(f"\nSelected Elements: {len(selected_elements)}")
    
    # Prepare data for API
    elements_data = []
    for element in selected_elements:
        element_info = mock_revit.get_element_info(element)
        elements_data.append(element_info)
    
    # Prepare project info
    project_info = {
        "name": "Test Project",
        "number": "TEST-001"
    }
    
    # Prepare the request payload
    payload = {
        "prompt": "Analyze these Revit elements and provide insights about their properties and potential improvements.",
        "revit_elements": elements_data,
        "project_info": project_info
    }
    
    try:
        # Send request to FastAPI server
        response = requests.post(
            "http://127.0.0.1:4000/process_revit_query",
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\nAnalysis Results:")
            print(json.dumps(result, indent=2))
        else:
            print(f"\nError: Server returned status code {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the FastAPI server. Make sure it's running on http://127.0.0.1:4000")
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    test_revit_plugin() 