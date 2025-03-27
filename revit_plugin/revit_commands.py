import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from System.Collections.Generic import List
from api_client import ClaudeMCPClient

class ClaudeRevitCommand(IExternalCommand):
    def Execute(self, commandData, message, elements):
        try:
            # Get the current Revit application and document
            app = commandData.Application
            doc = app.ActiveUIDocument.Document

            # Initialize the Claude MCP client
            claude_client = ClaudeMCPClient(base_url="http://localhost:5000")

            # Example prompt
            prompt = "Analyze the current project and suggest improvements for energy efficiency"

            # Process the query
            response = claude_client.process_query(prompt, doc)

            # Show results in Revit UI
            TaskDialog.Show("Claude Analysis", response['response'])

            return Result.Succeeded

        except Exception as e:
            TaskDialog.Show("Error", str(e))
            return Result.Failed 