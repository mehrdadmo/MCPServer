import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from System.Collections.Generic import List
import json
import requests
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

class ClaudeRevitCommand(IExternalCommand):
    def Execute(self, commandData, message, elements):
        try:
            # Get the current Revit application and document
            app = commandData.Application
            doc = app.ActiveUIDocument.Document

            # Initialize the API client
            api_url = "http://127.0.0.1:4000"

            # Get selected elements
            selection = app.ActiveUIDocument.Selection.GetElementIds()
            selected_elements = [doc.GetElement(id) for id in selection]

            # Extract element information
            elements_info = self.extract_elements_info(selected_elements, doc)

            # Prepare the request
            payload = {
                "prompt": "Analyze these Revit elements",
                "revit_elements": elements_info,
                "project_info": self.get_project_info(doc)
            }

            # Send request to API
            response = requests.post(
                f"{api_url}/process_revit_query",
                json=payload
            )

            if response.status_code == 200:
                result = response.json()
                
                # Show results in Revit UI
                TaskDialog.Show(
                    "Claude Analysis",
                    f"Response: {result['response']}\n\nSuggested Actions:\n" + 
                    "\n".join(f"- {action}" for action in result['suggested_actions'])
                )
            else:
                TaskDialog.Show("Error", f"API request failed: {response.text}")

            return Result.Succeeded

        except Exception as e:
            logger.error(f"Error in ClaudeRevitCommand: {str(e)}")
            TaskDialog.Show("Error", str(e))
            return Result.Failed

    def extract_elements_info(self, elements, doc):
        """Extract information from Revit elements"""
        elements_info = {
            "walls": [],
            "floors": [],
            "roofs": []
        }

        for element in elements:
            try:
                if isinstance(element, Wall):
                    elements_info["walls"].append({
                        "id": element.Id.IntegerValue,
                        "type": element.WallType.Name,
                        "length": element.Width,
                        "height": element.Height
                    })
                elif isinstance(element, Floor):
                    elements_info["floors"].append({
                        "id": element.Id.IntegerValue,
                        "type": element.FloorType.Name,
                        "area": element.Area
                    })
                elif isinstance(element, RoofBase):
                    elements_info["roofs"].append({
                        "id": element.Id.IntegerValue,
                        "type": element.RoofType.Name,
                        "area": element.Area
                    })
            except Exception as e:
                logger.error(f"Error extracting element info: {str(e)}")

        return elements_info

    def get_project_info(self, doc):
        """Get project information"""
        try:
            project_info = doc.ProjectInformation
            return {
                "project_name": project_info.Name,
                "project_number": project_info.Number,
                "client_name": project_info.ClientName,
                "building_name": project_info.BuildingName
            }
        except Exception as e:
            logger.error(f"Error getting project info: {str(e)}")
            return {} 