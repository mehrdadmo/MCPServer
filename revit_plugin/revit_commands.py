import clr
import os
import json
import logging
from System import Guid
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.Attributes import *

# Configure logging
logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), 'claude_mcp.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ClaudeRevitCommand(IExternalCommand):
    def Execute(self, commandData, message, elements):
        try:
            # Get the active document
            doc = commandData.Application.ActiveUIDocument.Document
            
            # Get selected elements
            selection = commandData.Application.ActiveUIDocument.Selection
            selected_ids = selection.GetElementIds()
            
            if not selected_ids:
                TaskDialog.Show("Claude MCP", "Please select elements in Revit first.")
                return Result.Succeeded
            
            # Extract element information
            elements_data = []
            for element_id in selected_ids:
                element = doc.GetElement(element_id)
                if element:
                    elements_data.append({
                        "id": element.Id.IntegerValue,
                        "name": element.Name,
                        "category": element.Category.Name if element.Category else "Unknown",
                        "type": element.GetType().Name
                    })
            
            # Send to API
            from api_client import APIClient
            client = APIClient()
            response = client.process_revit_query(elements_data)
            
            # Show response
            TaskDialog.Show("Claude Analysis", response)
            
            return Result.Succeeded
            
        except Exception as e:
            logging.error(f"Error in ClaudeRevitCommand: {str(e)}")
            TaskDialog.Show("Error", f"An error occurred: {str(e)}")
            return Result.Failed

# Register the command
__revit_application__ = None

def OnStartup(application):
    global __revit_application__
    __revit_application__ = application
    logging.info("Claude MCP plugin started")

def OnShutdown(application):
    global __revit_application__
    __revit_application__ = None
    logging.info("Claude MCP plugin shutdown") 