import os
import shutil
import zipfile
from datetime import datetime

def build_windows_installer():
    # Create output directory
    output_dir = "dist/ClaudeMCP_Windows"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    # Copy plugin files
    plugin_files = [
        "revit_plugin/__init__.py",
        "revit_plugin/revit_commands.py",
        "revit_plugin/api_client.py",
        "revit_plugin/ai_design_command.py",
        "ClaudeMCP.addin",
        "requirements.txt"
    ]

    for file in plugin_files:
        if os.path.exists(file):
            if os.path.isdir(file):
                shutil.copytree(file, os.path.join(output_dir, os.path.basename(file)))
            else:
                shutil.copy2(file, output_dir)

    # Create Windows-specific addin manifest
    with open(os.path.join(output_dir, "ClaudeMCP.addin"), "w") as f:
        f.write(f"""<?xml version="1.0" encoding="utf-8"?>
<RevitAddIns>
  <AddIn Type="Command">
    <Text>Claude MCP Integration</Text>
    <Description>Integrates Claude AI with Revit for intelligent design assistance</Description>
    <Assembly>{os.path.join("%APPDATA%", "Autodesk", "Revit", "Autodesk Revit 2025", "Addins", "ClaudeMCP", "revit_plugin", "revit_commands.py")}</Assembly>
    <FullClassName>revit_plugin.revit_commands.ClaudeRevitCommand</FullClassName>
    <ClientId>8D83C886-B739-4ACD-A9DB-1BC78F315B2A</ClientId>
    <VendorId>ClaudeMCP</VendorId>
    <VendorDescription>Claude MCP Revit Integration</VendorDescription>
  </AddIn>
  <AddIn Type="Command">
    <Text>AI Design</Text>
    <Description>Generate Revit models using natural language</Description>
    <Assembly>{os.path.join("%APPDATA%", "Autodesk", "Revit", "Autodesk Revit 2025", "Addins", "ClaudeMCP", "revit_plugin", "ai_design_command.py")}</Assembly>
    <FullClassName>revit_plugin.ai_design_command.AIDesignCommand</FullClassName>
    <ClientId>9E94C887-C840-4BDE-A9EC-2CD78F416B3B</ClientId>
    <VendorId>ClaudeMCP</VendorId>
    <VendorDescription>Claude MCP AI Design</VendorDescription>
  </AddIn>
</RevitAddIns>""")

    # Create installation instructions
    with open(os.path.join(output_dir, "INSTALL.txt"), "w") as f:
        f.write("""Claude MCP Revit Plugin Installation Instructions

1. Extract all files from this package to:
   %APPDATA%\\Autodesk\\Revit\\Autodesk Revit 2025\\Addins\\ClaudeMCP

2. Install Python dependencies:
   - Open Command Prompt as Administrator
   - Navigate to the installation directory
   - Run: pip install -r requirements.txt

3. Start Revit 2025
   - The plugin will appear in the Add-ins tab
   - Look for "Ask Claude" and "AI Design" buttons

4. Configure the plugin:
   - Make sure the FastAPI server is running
   - The server should be accessible at http://localhost:8000

For support, visit: https://github.com/mehrdadmo/MCPServer
""")

    # Create a zip file for distribution
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"ClaudeMCP_Revit2025_{timestamp}.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, output_dir)
                zipf.write(file_path, arcname)

    print(f"Windows installer created successfully: {zip_filename}")
    print(f"Installation directory: {output_dir}")

if __name__ == "__main__":
    build_windows_installer() 