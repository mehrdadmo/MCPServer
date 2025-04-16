# Claude MCP Revit Plugin

A Python-based Revit plugin that integrates Claude AI for architectural design assistance and analysis.

## Features

- Natural language processing of Revit elements
- AI-powered design suggestions
- Real-time analysis of selected elements
- Easy-to-use interface in Revit's Add-ins tab

## Requirements

- Revit 2024 or 2025
- Python 3.10 or later
- Required Python packages:
  ```
  pip install requests python-dotenv
  ```

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/mehrdadmo/MCPServer.git
   cd MCPServer
   ```

2. Build the plugin:
   ```bash
   python build_plugin.py
   ```

3. Install the plugin:
   ```bash
   # Windows
   xcopy /E /I dist\ClaudeMCP "%APPDATA%\Autodesk\Revit\Addins\2025\ClaudeMCP"
   ```

4. Configure Python in Revit:
   - Open Revit
   - Go to Manage → Python
   - Add the plugin directory to Python path:
     ```
     %APPDATA%\Autodesk\Revit\Addins\2025\ClaudeMCP
     ```

5. Restart Revit

## Usage

1. Open a Revit project
2. Select elements you want to analyze
3. Click the "Ask Claude" button in the Add-ins tab
4. View Claude's analysis and suggestions

## Configuration

Create a `.env` file in the plugin directory with:
```
MCP_SERVER_URL=http://localhost:8000
```

## Development

- `revit_plugin/` - Main plugin code
- `build_plugin.py` - Build script
- `ClaudeMCP.addin` - Revit add-in manifest

## License

MIT License

## Support

For issues and feature requests, please visit:
https://github.com/mehrdadmo/MCPServer/issues