# Claude MCP Revit Plugin - Windows Installer

This document explains how to build, distribute, and use the Windows installer for the Claude MCP Revit Plugin.

## Building the Installer

### Prerequisites

1. **Windows 10/11** - The installer can only be built on Windows
2. **Python 3.10 or later** - Download from [python.org](https://www.python.org/downloads/)
3. **NSIS (Nullsoft Scriptable Install System)** - Download from [nsis.sourceforge.io](https://nsis.sourceforge.io/Download)
4. **Git** (optional) - Download from [git-scm.com](https://git-scm.com/downloads)

### Build Steps

1. Clone the repository (or download the source code):
   ```
   git clone https://github.com/mehrdadmo/MCPServer.git
   cd MCPServer
   ```

2. Run the build installer script:
   ```
   build_installer.bat
   ```

   This script will:
   - Check for required dependencies
   - Download icons and images
   - Build the plugin
   - Create the installer (if NSIS is installed)

3. When completed, you'll have:
   - `dist/ClaudeMCP/` directory with all plugin files
   - `ClaudeMCP_Installer.exe` - the Windows installer

## Distributing the Installer

You can distribute the installer in several ways:

1. **GitHub Releases**:
   - Create a new release on GitHub
   - Upload the `ClaudeMCP_Installer.exe` file
   - Add release notes

2. **Direct Download**:
   - Host the `ClaudeMCP_Installer.exe` file on your website
   - Provide a download link

3. **Email**:
   - Send the `ClaudeMCP_Installer.exe` file as an attachment

## User Installation Instructions

Provide these instructions to your users:

1. **Download** the installer (`ClaudeMCP_Installer.exe`) from [your distribution source]

2. **Right-click** on the installer and select "Run as administrator"

3. **Follow** the on-screen installation instructions

4. The installer will:
   - Install the plugin to the Revit Addins folder
   - Create necessary registry entries
   - Install required Python packages
   - Create desktop and start menu shortcuts

5. **Start Revit 2025** to use the plugin

## Troubleshooting

If users encounter issues:

1. **Plugin Not Appearing**:
   - Verify Revit Python Shell is installed
   - Check that files were installed to:
     ```
     %APPDATA%\Autodesk\Revit\Addins\2025\ClaudeMCP
     %APPDATA%\Autodesk\Revit\Addins\2025\ClaudeMCP.addin
     ```

2. **Errors During Installation**:
   - Ensure user has administrator privileges
   - Check if Python is installed correctly
   - Verify the .NET Framework is installed

3. **Logs**:
   Check logs at:
   ```
   %APPDATA%\Autodesk\Revit\Addins\2025\ClaudeMCP\logs
   ```

## Uninstalling

Users can uninstall the plugin through:

1. **Windows Control Panel** > **Programs and Features** > **Claude MCP Revit Plugin** > **Uninstall**

2. **Start Menu** > **Claude MCP** > **Uninstall**

## Customizing the Installer

To customize the installer:

1. **Change Icon**: Replace the icon files in `revit_plugin/assets/`

2. **Modify Install Location**: Edit the `InstallDir` variable in `installer.nsi`

3. **Add Custom Actions**: Edit the install section in `installer.nsi` 