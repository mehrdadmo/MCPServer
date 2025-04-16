import os
import sys
import clr
from System.IO import Path
import logging

# Configure logging
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    filename=os.path.join(log_dir, "launcher.log"),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Get add-in directory
try:
    addin_dir = Path.GetDirectoryName(__FILE__)
    logging.info(f"Add-in directory: {addin_dir}")
except Exception as e:
    logging.error(f"Error getting add-in directory: {e}")
    addin_dir = os.path.dirname(os.path.abspath(__file__))

# Add addin directory to path
sys.path.append(addin_dir)
logging.info(f"Added to sys.path: {addin_dir}")

# Import required Revit libraries
try:
    clr.AddReference('RevitAPI')
    clr.AddReference('RevitAPIUI')
    from Autodesk.Revit.DB import *
    from Autodesk.Revit.UI import *
    logging.info("Successfully imported Revit API")
except Exception as e:
    logging.error(f"Error importing Revit API: {e}")

# Import command implementations
try:
    from revit_plugin.revit_commands import ClaudeRevitCommand
    from revit_plugin.ai_design_command import AIDesignCommand
    logging.info("Successfully imported command implementations")
except Exception as e:
    logging.error(f"Error importing command implementations: {e}")

# This function will be called by Revit Python Shell
def ExecuteCommand(commandData):
    try:
        # Get the command name from the button text
        command_name = commandData.Application.ActiveAddInId.GetHashCode()
        logging.info(f"Command hash: {command_name}")
        
        # Check if it's the "Ask Claude" button
        button_text = Path.GetFileName(commandData.Application.ActiveAddInId.GetPath())
        logging.info(f"Button text: {button_text}")
        
        if "AI Design" in button_text:
            logging.info("Executing AIDesignCommand")
            cmd = AIDesignCommand()
            return cmd.Execute(commandData, None, None)
        else:
            # Default to ClaudeRevitCommand
            logging.info("Executing ClaudeRevitCommand")
            cmd = ClaudeRevitCommand()
            return cmd.Execute(commandData, None, None)
    except Exception as e:
        logging.error(f"Error in ExecuteCommand: {e}")
        TaskDialog.Show("Error", f"An error occurred: {str(e)}")
        return Result.Failed 