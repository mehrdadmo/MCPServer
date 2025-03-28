# Claude MCP Revit Integration

A server implementation that integrates Claude AI with Autodesk Revit architectural software, enabling AI-powered analysis of Revit elements.

## Features

- FastAPI server for handling Claude AI requests
- Revit plugin integration with custom UI
- Real-time communication between Revit and Claude
- Environment-based configuration
- Comprehensive logging system
- Element analysis and insights

## Project Structure

```
MCPServer/
├── revit_plugin/         # Revit plugin code
│   ├── __init__.py
│   ├── revit_commands.py
│   ├── api_client.py
│   └── requirements.txt
├── tests/                # Test files
├── scripts/              # Utility scripts
├── app.py               # Main FastAPI application
├── test_server.py       # Test server implementation
├── setup.py             # Package configuration
├── build.py             # Build script
└── requirements.txt     # Project dependencies
```

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
- Copy `.env.example` to `.env`
- Update the configuration values, including your Claude API key

4. Build the Revit plugin:
```bash
python build_plugin.py
```

5. Install the Revit plugin:
- Windows: Copy `dist/ClaudeMCP` to `C:\Users\[USERNAME]\AppData\Roaming\Autodesk\Revit\Autodesk Revit 2024\Addins\`
- Mac: Copy `dist/ClaudeMCP` to `~/Library/Application Support/Autodesk/Revit/Autodesk Revit 2024/Addins/`

6. Run the FastAPI server:
```bash
python test_server.py
```

## Usage

1. Start Autodesk Revit
2. Open a Revit project
3. Select elements you want to analyze
4. Click the "Ask Claude" button in the Add-ins tab
5. View Claude's analysis in the task dialog

## Development

- FastAPI server runs on http://127.0.0.1:4000
- API documentation available at http://127.0.0.1:4000/docs
- Health check endpoint at http://127.0.0.1:4000/health

## Testing

Run tests with:
```bash
pytest
```

## License

MIT License

## Author

Mehrdad Mohamadali