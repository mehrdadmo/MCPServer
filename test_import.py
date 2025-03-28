try:
    from src.main import app
    print("Successfully imported app from src.main")
except Exception as e:
    print(f"Error importing: {str(e)}") 