# Claude MCP Revit Plugin - Windows Installation Guide

This guide provides detailed instructions for installing and using the Claude MCP Revit Plugin on Windows systems.

## Prerequisites

1. **Revit 2025** - Make sure you have Revit 2025 installed
2. **Python 3.10 or later** - Download from [python.org](https://www.python.org/downloads/)
3. **Revit Python Shell** - Download and install from [GitHub](https://github.com/architecture-building-systems/revitpythonshell/releases)
4. **Administrator privileges** - Required for installation

## Installation Steps

### Automatic Installation (Recommended)

1. Build the plugin:
   ```
   python build_plugin.py
   ```

2. Run the installer as administrator:
   - Right-click on `install_windows.bat`
   - Select "Run as administrator"
   - Follow the on-screen instructions

3. Restart Revit 2025

### Manual Installation

If the automatic installation doesn't work, follow these steps:

1. Build the plugin:
   ```
   python build_plugin.py
   ```

2. Copy the plugin files:
   ```
   xcopy /E /I /Y dist\ClaudeMCP %APPDATA%\Autodesk\Revit\Addins\2025\ClaudeMCP
   copy ClaudeMCP.addin %APPDATA%\Autodesk\Revit\Addins\2025\
   ```

3. Install required Python packages:
   ```
   cd %APPDATA%\Autodesk\Revit\Addins\2025\ClaudeMCP
   pip install -r requirements.txt
   ```

4. Restart Revit 2025

## Configuration

1. Edit the `.env` file in the plugin directory to set your MCP server URL:
   ```
   %APPDATA%\Autodesk\Revit\Addins\2025\ClaudeMCP\.env
   ```

2. Set your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## Usage

1. Start Revit 2025
2. Go to the Add-ins tab
3. Click on "Ask Claude" to analyze selected Revit elements
4. To use the AI design generation:
   - Make sure the MCP server is running
   - Run `python test_server.py` from the command line
   - Use the plugin from Revit

## Troubleshooting

### Plugin Not Appearing

1. Check if Revit Python Shell is properly installed
2. Verify the plugin files are in the correct location:
   ```
   %APPDATA%\Autodesk\Revit\Addins\2025\ClaudeMCP
   %APPDATA%\Autodesk\Revit\Addins\2025\ClaudeMCP.addin
   ```
3. Check the Revit journal files for errors:
   ```
   %APPDATA%\Autodesk\Revit\Autodesk Revit 2025\Journals
   ```

### Connection Issues

1. Make sure the MCP server is running
2. Check the .env file for the correct MCP_SERVER_URL setting
3. Verify your Anthropic API key is valid

### Logs

Check the logs for errors:
```
%APPDATA%\Autodesk\Revit\Addins\2025\ClaudeMCP\logs\claude_mcp.log
```

## Support

For issues and feature requests, please submit them to:
https://github.com/mehrdadmo/MCPServer/issues 