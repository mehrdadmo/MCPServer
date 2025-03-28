import uvicorn
from dotenv import load_dotenv
import os
import sys
import importlib.util

# Load environment variables
load_dotenv()

# Get host and port from environment variables
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))

if __name__ == "__main__":
    print(f"Starting server on {HOST}:{PORT}")
    
    try:
        # Attempt to import app directly
        spec = importlib.util.spec_from_file_location("app", "src/main.py")
        app_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app_module)
        
        # Run directly without module import
        uvicorn.run(app_module.app, host=HOST, port=PORT)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1) 