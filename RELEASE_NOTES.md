# Claude MCP Revit 2025 Plugin - Release Notes

## Version 1.0.0 (2024-04-16)

### Package Contents
The installer package contains the following files:
- `__init__.py`: Package initialization file
- `ai_design_command.py`: AI-powered design generation module
- `api_client.py`: API client for Claude AI integration
- `ClaudeMCP.addin`: Revit add-in manifest file
- `INSTALL.txt`: Installation instructions
- `requirements.txt`: Python dependencies
- `revit_commands.py`: Core Revit command implementations

### Features
- Integration with Claude AI for intelligent design assistance
- Natural language processing for design requirements
- Automatic model generation based on user input
- Support for Revit 2025
- Windows installer with automatic dependency management

### Installation
1. Download the installer: [ClaudeMCP_Revit2025_20250416_091430.zip](ClaudeMCP_Revit2025_20250416_091430.zip)
2. Extract the ZIP file to a temporary location
3. Copy all files to: `%APPDATA%\Autodesk\Revit\Autodesk Revit 2025\Addins\ClaudeMCP`
4. Install Python dependencies:
   ```bash
   cd "%APPDATA%\Autodesk\Revit\Autodesk Revit 2025\Addins\ClaudeMCP"
   pip install -r requirements.txt
   ```
5. Start Revit 2025
6. The plugin will appear in the Add-ins tab

### System Requirements
- Windows 10 or later
- Autodesk Revit 2025
- Python 3.10 or later
- Internet connection for Claude AI integration

### File Descriptions
- `__init__.py`: Initializes the plugin package and exports command classes
- `ai_design_command.py`: Implements AI-powered design generation using Claude
- `api_client.py`: Handles communication with the Claude AI API
- `ClaudeMCP.addin`: Configures the plugin for Revit 2025
- `INSTALL.txt`: Detailed installation instructions
- `requirements.txt`: Lists required Python packages
- `revit_commands.py`: Core functionality for Revit integration

### Changes
- Initial release
- Windows installer support
- Automatic dependency installation
- Improved error handling
- Enhanced user interface

### Known Issues
- None reported

### Support
For support and bug reports, please visit:
https://github.com/mehrdadmo/MCPServer/issues 