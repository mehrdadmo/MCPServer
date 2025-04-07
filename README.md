# Claude MCP Revit Integration

An AI-powered Revit plugin that generates architectural designs based on natural language descriptions using Claude AI.

## Features

- Natural language processing for design requirements
- AI-powered architectural design generation
- Automatic Revit model creation
- Support for rooms, walls, doors, and windows
- Automatic dimensioning and annotations
- Modern UI with progress tracking

## Requirements

- Python 3.7 or higher
- Autodesk Revit 2024
- Anthropic API key for Claude AI

## Installation

1. Install the required Python packages:
```bash
pip install -r requirements.txt
```

2. Build the plugin:
```bash
python build_plugin.py
```

3. Copy the plugin to your Revit add-ins folder:
- Windows: `C:\Users\%USERNAME%\AppData\Roaming\Autodesk\Revit\Autodesk Revit 2024\Addins\ClaudeMCP`
- Mac: `~/Library/Application Support/Autodesk/Revit/Autodesk Revit 2024/Addins/`

4. Set up your Anthropic API key:
```bash
export ANTHROPIC_API_KEY="your-api-key"
```

## Usage

1. Start Revit and open a new project
2. Go to the Add-ins tab
3. Click the "AI Design" button
4. Enter your design requirements in natural language
5. Wait for the AI to generate and create the design
6. Review and modify the generated design as needed

## Testing

Run the test script to verify the AI design generation:
```bash
python test_ai_design.py
```

## Project Structure

- `revit_plugin/`: Main plugin package
  - `__init__.py`: Package initialization
  - `ai_design_command.py`: AI design command implementation
  - `claude_integration.py`: Claude AI integration
  - `requirements.txt`: Python dependencies
- `build_plugin.py`: Build script
- `test_ai_design.py`: Test script
- `README.md`: Project documentation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.