import os
import sys
import shutil
from setuptools import setup
from setuptools.command.build_py import build_py

class BuildRevitPlugin(build_py):
    def run(self):
        # First, run the normal build
        build_py.run(self)
        
        # Create the output directory if it doesn't exist
        output_dir = "dist/ClaudeMCP"
        os.makedirs(output_dir, exist_ok=True)
        
        # Copy the Revit plugin files
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
    setup(
        name="ClaudeMCP",
        version="1.0.0",
        packages=["revit_plugin"],
        cmdclass={"build_py": BuildRevitPlugin},
    ) 