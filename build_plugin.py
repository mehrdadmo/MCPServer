import os
import shutil
import platform
import sys
from pathlib import Path

def build_plugin():
    print("Building Claude MCP Revit Plugin...")
    
    # Clean up existing build directory
    dist_dir = 'dist/ClaudeMCP'
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    
    # Create fresh build directory
    os.makedirs(dist_dir, exist_ok=True)
    
    # Create assets directory if it doesn't exist
    assets_dir = Path("revit_plugin/assets")
    if not assets_dir.exists():
        assets_dir.mkdir(parents=True)
    
    # Make sure we have placeholder icons
    for icon_file in ["icon.ico", "server_icon.ico"]:
        icon_path = assets_dir / icon_file
        if not icon_path.exists():
            with open(icon_path, "w") as f:
                f.write(f"Placeholder for {icon_file}")
    
    # Copy Python files
    source_dir = 'revit_plugin'
    for item in os.listdir(source_dir):
        s = os.path.join(source_dir, item)
        d = os.path.join(dist_dir, item)
        if os.path.isfile(s):
            shutil.copy2(s, d)
        elif os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
    
    # Copy launcher script
    if os.path.exists('launcher.py'):
        shutil.copy2('launcher.py', os.path.join(dist_dir, 'launcher.py'))
    
    # Copy README files
    if os.path.exists('README.md'):
        shutil.copy2('README.md', os.path.join(dist_dir, 'README.md'))
    if os.path.exists('README_WINDOWS.md'):
        shutil.copy2('README_WINDOWS.md', os.path.join(dist_dir, 'README_WINDOWS.md'))
    
    # Copy test_server.py if it exists
    if os.path.exists('test_server.py'):
        shutil.copy2('test_server.py', os.path.join(dist_dir, 'test_server.py'))
    
    # Copy server files if they exist
    if os.path.exists('claude_integration.py'):
        shutil.copy2('claude_integration.py', os.path.join(dist_dir, 'claude_integration.py'))
    
    # Create a sample .env file
    with open(os.path.join(dist_dir, '.env'), 'w') as f:
        f.write("# Configuration for Claude MCP Revit Plugin\n")
        f.write("MCP_SERVER_URL=http://localhost:8000\n")
        f.write("ANTHROPIC_API_KEY=your_api_key_here\n")
    
    # Copy requirements.txt
    if os.path.exists('requirements.txt'):
        shutil.copy2('requirements.txt', os.path.join(dist_dir, 'requirements.txt'))
    else:
        # Create default requirements.txt
        with open(os.path.join(dist_dir, 'requirements.txt'), 'w') as f:
            f.write("fastapi>=0.110.0\n")
            f.write("uvicorn>=0.29.0\n")
            f.write("python-dotenv>=1.0.0\n")
            f.write("anthropic>=0.30.0\n")
            f.write("requests>=2.31.0\n")
            f.write("pydantic>=2.6.0\n")
            f.write("websockets>=12.0\n")
    
    # Copy addin manifest
    shutil.copy2('ClaudeMCP.addin', os.path.join(dist_dir, 'ClaudeMCP.addin'))
    
    # Platform-specific build
    if platform.system() == 'Windows':
        print("Building for Windows...")
        # Check for Revit Python Shell DLL
        rps_dll = r"C:\Program Files\RevitPythonShell\RpsAddin.dll"
        if os.path.exists(rps_dll):
            shutil.copy2(rps_dll, os.path.join(dist_dir, "RpsAddin.dll"))
            print("Copied Revit Python Shell DLL")
        else:
            print("WARNING: Revit Python Shell DLL not found at", rps_dll)
            print("Plugin may not work without Revit Python Shell installed.")
    
    print(f"Build completed successfully. Output directory: {dist_dir}")
    print("\nNext steps:")
    
    if platform.system() == 'Windows':
        print("To create an installer (requires NSIS):")
        print("  python create_windows_installer.py")
        print("\nOr to install manually:")
        print("  xcopy /E /I /Y dist\\ClaudeMCP %APPDATA%\\Autodesk\\Revit\\Addins\\2025\\ClaudeMCP")
        print("  copy ClaudeMCP.addin %APPDATA%\\Autodesk\\Revit\\Addins\\2025\\")
    else:
        print("To install manually:")
        print("  cp -R dist/ClaudeMCP ~/Library/Application\\ Support/Autodesk/Revit/Addins/2025/")
    
    return True

if __name__ == '__main__':
    build_plugin() 