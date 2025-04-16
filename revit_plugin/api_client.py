import clr
import json
import requests
from System.Collections.Generic import Dictionary
import logging
from dotenv import load_dotenv
import os
from typing import Dict, Any, List

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    filename=os.path.join(os.path.dirname(__file__), 'claude_mcp.log'),
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self):
        # Get server URL from environment variable, default to localhost
        self.server_url = os.getenv("MCP_SERVER_URL", "http://localhost:8000")
        logger.info(f"Initializing API client with server URL: {self.server_url}")
    
    def process_revit_query(self, elements_data):
        """Send Revit elements to the server for processing"""
        try:
            # Extract project information from Revit document if available
            project_info = {}
            
            # Prepare the request
            payload = {
                "elements": elements_data,
                "project_info": project_info
            }
            
            # Log the request
            logger.info(f"Sending query to server with {len(elements_data)} elements")
            
            # Make API call
            response = requests.post(
                f"{self.server_url}/process_revit_query",
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            
            return result.get('response', 'No response from server')
        except Exception as e:
            logger.error(f"Error processing Revit query: {str(e)}")
            return f"Error communicating with server: {str(e)}"
    
    def generate_model(self, description: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Request model generation from the server"""
        try:
            logger.info(f"Requesting model generation for: {description}")
            
            response = requests.post(
                f"{self.server_url}/generate_revit_model",
                json={
                    "description": description,
                    "requirements": requirements,
                    "version": "1.0"
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error generating model: {str(e)}")
            raise
    
    def check_server_health(self) -> bool:
        """Check if the server is running and healthy"""
        try:
            response = requests.get(f"{self.server_url}/health")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return False

class ClaudeMCPClient:
    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url
        self.session = requests.Session()
        logger.info(f"Initialized ClaudeMCPClient with base URL: {base_url}")

    def process_query(self, prompt: str, doc) -> dict:
        """
        Process a query with the current Revit document context
        """
        try:
            # Extract relevant Revit information
            project_info = self.extract_project_info(doc)
            elements = self.extract_relevant_elements(doc)

            # Prepare the request
            payload = {
                "prompt": prompt,
                "revit_elements": elements,
                "project_info": project_info
            }

            logger.info(f"Sending query to server: {prompt}")

            # Make the API call
            response = self.session.post(
                f"{self.base_url}/process_revit_query",
                json=payload
            )

            response.raise_for_status()
            return response.json()

        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            raise

    def extract_project_info(self, doc) -> dict:
        """
        Extract relevant project information from the Revit document
        """
        try:
            project_info = doc.ProjectInformation
            return {
                "project_name": project_info.Name,
                "project_number": project_info.Number,
                "project_status": project_info.Status,
                "client_name": project_info.ClientName,
                "building_name": project_info.BuildingName
            }
        except Exception as e:
            logger.error(f"Error extracting project info: {str(e)}")
            return {}

    def extract_relevant_elements(self, doc) -> dict:
        """
        Extract relevant elements from the Revit document
        """
        try:
            elements = {}
            
            # Collect walls
            walls = FilteredElementCollector(doc).OfClass(Wall).ToElements()
            elements["walls"] = [
                {
                    "id": wall.Id.IntegerValue,
                    "type": wall.WallType.Name,
                    "length": wall.Width,
                    "height": wall.Height
                }
                for wall in walls
            ]

            # Collect rooms
            rooms = FilteredElementCollector(doc).OfClass(Room).ToElements()
            elements["rooms"] = [
                {
                    "id": room.Id.IntegerValue,
                    "name": room.Name,
                    "number": room.Number,
                    "area": room.Area
                }
                for room in rooms
            ]

            return elements

        except Exception as e:
            logger.error(f"Error extracting elements: {str(e)}")
            return {}

    def health_check(self) -> bool:
        """
        Check if the server is healthy
        """
        try:
            response = self.session.get(f"{self.base_url}/health")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return False 