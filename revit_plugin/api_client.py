import clr
import json
import requests
from System.Collections.Generic import Dictionary

class ClaudeMCPClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url

    def process_query(self, prompt: str, doc) -> Dict:
        """
        Process a query with the current Revit document context
        """
        # Extract relevant Revit information
        project_info = self.extract_project_info(doc)
        elements = self.extract_relevant_elements(doc)

        # Prepare the request
        payload = {
            "prompt": prompt,
            "revit_elements": elements,
            "project_info": project_info
        }

        # Make the API call
        response = requests.post(
            f"{self.base_url}/process_revit_query",
            json=payload
        )

        return response.json()

    def extract_project_info(self, doc) -> Dict:
        """
        Extract relevant project information from the Revit document
        """
        project_info = doc.ProjectInformation
        return {
            "project_name": project_info.Name,
            "project_number": project_info.Number,
            "project_status": project_info.Status
        }

    def extract_relevant_elements(self, doc) -> Dict:
        """
        Extract relevant elements from the Revit document
        """
        # Implement your logic to extract relevant elements
        # This is just a placeholder
        return {} 