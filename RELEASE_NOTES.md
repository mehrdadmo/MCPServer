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
- `install_windows.bat`: Windows installation script

### Features
- Integration with Claude AI for intelligent design assistance
- Natural language processing for design requirements
- Automatic model generation based on user input
- Support for Revit 2025
- Windows installer with automatic dependency management

### Installation (Windows)
1. Download the installer: [ClaudeMCP_Revit2025_20250416_091430.zip](ClaudeMCP_Revit2025_20250416_091430.zip)
2. Extract the ZIP file to a temporary location
3. Right-click on `install_windows.bat` and select "Run as administrator"
4. The installer will:
   - Create the necessary directories
   - Copy all required files
   - Install Python dependencies
   - Configure the plugin for Revit 2025
5. Start Revit 2025
6. The plugin will appear in the Add-ins tab

### Manual Installation (Alternative)
If the automatic installer doesn't work, you can install manually:
1. Create directory: `%APPDATA%\Autodesk\Revit\Autodesk Revit 2025\Addins\ClaudeMCP`
2. Copy all files from the ZIP to this directory
3. Open Command Prompt as Administrator
4. Navigate to the installation directory
5. Run: `pip install -r requirements.txt`

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
- `install_windows.bat`: Windows installation script

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