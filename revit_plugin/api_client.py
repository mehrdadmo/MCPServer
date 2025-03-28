import clr
import json
import requests
from System.Collections.Generic import Dictionary
import logging
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    filename=os.getenv("LOG_FILE", "revit_plugin.log"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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