import os
import shutil

def build_plugin():
    # Clean up existing build directory
    dist_dir = 'dist/ClaudeMCP'
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    
    # Create fresh build directory
    os.makedirs(dist_dir, exist_ok=True)
    
    # Copy Python files
    source_dir = 'revit_plugin'
    for item in os.listdir(source_dir):
        s = os.path.join(source_dir, item)
        d = os.path.join(dist_dir, item)
        if os.path.isfile(s):
            shutil.copy2(s, d)
        elif os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
    
    # Copy addin manifest
    shutil.copy2('ClaudeMCP.addin', os.path.join(dist_dir, 'ClaudeMCP.addin'))
    
    print(f"Build completed successfully. Output directory: {dist_dir}")
    print("\nNext steps:")
    print("1. Copy the contents of dist/ClaudeMCP to:")
    print("   Windows: %APPDATA%\\Autodesk\\Revit\\Addins\\2025\\ClaudeMCP")
    print("2. Make sure Python 3.10+ is installed")
    print("3. Install required packages: pip install requests python-dotenv")
    print("4. Restart Revit")
    return True

if __name__ == '__main__':
    build_plugin() 