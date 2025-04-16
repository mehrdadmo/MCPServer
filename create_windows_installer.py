import os
import sys
import shutil
import subprocess
from pathlib import Path

# Configuration
PLUGIN_NAME = "ClaudeMCP"
PLUGIN_VERSION = "1.0.0"
PLUGIN_PUBLISHER = "MehrdadMo"
PLUGIN_URL = "https://github.com/mehrdadmo/MCPServer"
INSTALLER_OUTPUT = "ClaudeMCP_Installer.exe"

def create_installer():
    # Check if NSIS is installed
    nsis_path = ""
    try:
        # First try the standard installation path
        default_path = r"C:\Program Files (x86)\NSIS\makensis.exe"
        if os.path.exists(default_path):
            nsis_path = default_path
        else:
            # Try to find it using 'where' command
            result = subprocess.run(["where", "makensis"], capture_output=True, text=True)
            if result.returncode == 0:
                nsis_path = result.stdout.strip()
    except Exception:
        pass
        
    if not nsis_path:
        print("NSIS not found. Please install NSIS from https://nsis.sourceforge.io/Download")
        print("Installing NSIS Manually:")
        print("1. Download NSIS from https://nsis.sourceforge.io/Download")
        print("2. Install NSIS")
        print("3. Run this script again")
        return False
    
    # Make sure build directory exists
    build_dir = Path("dist") / PLUGIN_NAME
    if not build_dir.exists():
        print("Please run build_plugin.py first to create the distribution files.")
        return False
    
    # Create installer directory
    installer_dir = Path("installer")
    if installer_dir.exists():
        shutil.rmtree(installer_dir)
    installer_dir.mkdir()
    
    # Create NSIS script
    nsis_script = installer_dir / "installer.nsi"
    with open(nsis_script, "w") as f:
        f.write(f"""
!include "MUI2.nsh"
!include "LogicLib.nsh"

; General
Name "{PLUGIN_NAME} Revit Plugin"
OutFile "../{INSTALLER_OUTPUT}"
Unicode True
InstallDir "$APPDATA\\Autodesk\\Revit\\Addins\\2025\\{PLUGIN_NAME}"
InstallDirRegKey HKCU "Software\\{PLUGIN_NAME}" "Install_Dir"
RequestExecutionLevel admin

; Interface Settings
!define MUI_ABORTWARNING
!define MUI_ICON "..\\revit_plugin\\assets\\icon.ico"
!define MUI_UNICON "..\\revit_plugin\\assets\\icon.ico"
!define MUI_WELCOMEFINISHPAGE_BITMAP "..\\revit_plugin\\assets\\installer_welcome.bmp"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "..\\revit_plugin\\assets\\installer_header.bmp"
!define MUI_HEADERIMAGE_RIGHT

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "..\\LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; Languages
!insertmacro MUI_LANGUAGE "English"

; Install Section
Section "Install"
  SetOutPath "$INSTDIR"
  
  ; Create plugin directory
  CreateDirectory "$INSTDIR"
  
  ; Copy plugin files
  File /r "..\\dist\\{PLUGIN_NAME}\\*.*"
  
  ; Create addin manifest in the Revit Addins directory
  CreateDirectory "$APPDATA\\Autodesk\\Revit\\Addins\\2025"
  File /oname=$APPDATA\\Autodesk\\Revit\\Addins\\2025\\{PLUGIN_NAME}.addin "..\\{PLUGIN_NAME}.addin"
  
  ; Create uninstaller
  WriteUninstaller "$INSTDIR\\uninstall.exe"
  
  ; Create registry keys for uninstaller
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{PLUGIN_NAME}" "DisplayName" "{PLUGIN_NAME} Revit Plugin"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{PLUGIN_NAME}" "UninstallString" "$INSTDIR\\uninstall.exe"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{PLUGIN_NAME}" "DisplayVersion" "{PLUGIN_VERSION}"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{PLUGIN_NAME}" "Publisher" "{PLUGIN_PUBLISHER}"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{PLUGIN_NAME}" "URLInfoAbout" "{PLUGIN_URL}"
  
  ; Install Python if not already installed
  Call CheckPython
  
  ; Install Python dependencies
  nsExec::ExecToLog 'cmd.exe /c "python -m pip install -r $INSTDIR\\requirements.txt"'
  
  ; Create start menu shortcut
  CreateDirectory "$SMPROGRAMS\\{PLUGIN_NAME}"
  CreateShortCut "$SMPROGRAMS\\{PLUGIN_NAME}\\Uninstall.lnk" "$INSTDIR\\uninstall.exe"
  CreateShortCut "$SMPROGRAMS\\{PLUGIN_NAME}\\Documentation.lnk" "$INSTDIR\\README.md"
  
  ; Create desktop shortcut to launch MCP Server
  CreateShortCut "$DESKTOP\\Launch MCP Server.lnk" "cmd.exe" '/k "cd /d $INSTDIR && python test_server.py"' "$INSTDIR\\assets\\server_icon.ico"
SectionEnd

; Uninstall Section
Section "Uninstall"
  ; Remove plugin files
  RMDir /r "$INSTDIR"
  
  ; Remove addin manifest
  Delete "$APPDATA\\Autodesk\\Revit\\Addins\\2025\\{PLUGIN_NAME}.addin"
  
  ; Remove start menu shortcuts
  RMDir /r "$SMPROGRAMS\\{PLUGIN_NAME}"
  
  ; Remove desktop shortcut
  Delete "$DESKTOP\\Launch MCP Server.lnk"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{PLUGIN_NAME}"
  DeleteRegKey HKCU "Software\\{PLUGIN_NAME}"
SectionEnd

; Check if Python is installed
Function CheckPython
  nsExec::ExecToStack 'python --version'
  Pop $0
  Pop $1
  ${If} $0 != 0
    MessageBox MB_YESNO "Python is required but not found. Would you like to download and install Python now?" IDYES download IDNO done
    download:
      ExecShell "open" "https://www.python.org/downloads/"
    done:
  ${EndIf}
FunctionEnd

; Check if Revit Python Shell is installed
Function CheckRPS
  IfFileExists "C:\\Program Files\\RevitPythonShell\\RpsAddin.dll" done notfound
  notfound:
    MessageBox MB_YESNO "Revit Python Shell is required but not found. Would you like to download it now?" IDYES download IDNO done
    download:
      ExecShell "open" "https://github.com/architecture-building-systems/revitpythonshell/releases"
    done:
FunctionEnd
""")
    
    # Create icon and assets directory if it doesn't exist
    assets_dir = Path("revit_plugin") / "assets"
    if not assets_dir.exists():
        assets_dir.mkdir(parents=True)
    
    # Create default icons if they don't exist (placeholder - would need real icons)
    if not (assets_dir / "icon.ico").exists():
        # Create a simple text file as a placeholder
        with open(assets_dir / "icon.ico", "w") as f:
            f.write("Placeholder for icon")
    
    if not (assets_dir / "server_icon.ico").exists():
        # Create a simple text file as a placeholder
        with open(assets_dir / "server_icon.ico", "w") as f:
            f.write("Placeholder for server icon")
    
    if not (assets_dir / "installer_welcome.bmp").exists():
        # Create a simple text file as a placeholder
        with open(assets_dir / "installer_welcome.bmp", "w") as f:
            f.write("Placeholder for welcome image")
    
    if not (assets_dir / "installer_header.bmp").exists():
        # Create a simple text file as a placeholder
        with open(assets_dir / "installer_header.bmp", "w") as f:
            f.write("Placeholder for header image")
    
    # Make sure LICENSE file exists
    if not os.path.exists("LICENSE"):
        with open("LICENSE", "w") as f:
            f.write("""MIT License

Copyright (c) 2024 MehrdadMo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.""")
    
    # Run NSIS to create installer
    print(f"Creating installer with NSIS at {nsis_path}...")
    try:
        subprocess.run([nsis_path, str(nsis_script)], check=True)
        print(f"Installer created successfully: {INSTALLER_OUTPUT}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating installer: {e}")
        return False

if __name__ == "__main__":
    create_installer() 