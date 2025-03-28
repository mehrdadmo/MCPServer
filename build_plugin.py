import os
import shutil

def build_plugin():
    # Create output directory
    output_dir = "dist/ClaudeMCP"
    os.makedirs(output_dir, exist_ok=True)
    
    # Copy Revit plugin files
    plugin_dir = "revit_plugin"
    for item in os.listdir(plugin_dir):
        s = os.path.join(plugin_dir, item)
        d = os.path.join(output_dir, item)
        if os.path.isfile(s):
            shutil.copy2(s, d)
        elif os.path.isdir(s):
            shutil.copytree(s, d)
    
    # Copy the addin manifest
    shutil.copy2("ClaudeMCP.addin", output_dir)
    
    print(f"Build complete. Output directory: {output_dir}")

if __name__ == "__main__":
    build_plugin() 