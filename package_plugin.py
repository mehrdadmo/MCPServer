import os
import shutil
import zipfile
import datetime
import platform
import subprocess
import sys
from build_plugin import build_plugin

def create_install_scripts(dist_dir):
    # Create Windows installation script
    win_install = '''@echo off
echo Installing ClaudeMCP Revit Plugin...
set "REVIT_ADDINS=%APPDATA%\\Autodesk\\Revit\\Autodesk Revit 2024\\Addins\\ClaudeMCP"
if not exist "%REVIT_ADDINS%" mkdir "%REVIT_ADDINS%"
xcopy /E /I /Y "ClaudeMCP\\*" "%REVIT_ADDINS%"
echo Installation complete!
pause
'''
    
    # Create Mac installation script
    mac_install = '''#!/bin/bash
echo "Installing ClaudeMCP Revit Plugin..."
REVIT_ADDINS="$HOME/Library/Application Support/Autodesk/Revit/Autodesk Revit 2024/Addins/ClaudeMCP"
mkdir -p "$REVIT_ADDINS"
cp -R ClaudeMCP/* "$REVIT_ADDINS/"
echo "Installation complete!"
'''
    
    # Write installation scripts
    with open(os.path.join(dist_dir, 'install_windows.bat'), 'w') as f:
        f.write(win_install)
    
    with open(os.path.join(dist_dir, 'install_mac.sh'), 'w') as f:
        f.write(mac_install)
    
    # Make Mac script executable
    os.chmod(os.path.join(dist_dir, 'install_mac.sh'), 0o755)

def create_package():
    # Build the plugin
    build_plugin()
    
    # Create versioned package directory
    version = "1.0"
    date = datetime.datetime.now().strftime("%Y%m%d")
    package_name = f"ClaudeMCP_Plugin_v{version}_{date}"
    package_dir = f"dist/{package_name}"
    
    # Create package directory
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir)
    
    # Copy built plugin to package directory
    shutil.copytree("dist/ClaudeMCP", os.path.join(package_dir, "ClaudeMCP"))
    
    # Create installation scripts
    create_install_scripts(package_dir)
    
    # Copy README and LICENSE
    shutil.copy2("README.md", os.path.join(package_dir, "README.md"))
    shutil.copy2("LICENSE", os.path.join(package_dir, "LICENSE"))
    
    # Create zip archive
    shutil.make_archive(package_name, 'zip', 'dist', package_name)
    
    print(f"\nPackage created successfully: {package_name}.zip")
    print(f"Package location: {os.path.abspath(package_name + '.zip')}")
    print("\nPackage contents:")
    for root, dirs, files in os.walk(package_dir):
        level = root.replace(package_dir, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{subindent}{f}")

if __name__ == '__main__':
    create_package() 