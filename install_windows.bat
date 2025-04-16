@echo off
echo Claude MCP Revit Plugin Installer
echo ===============================

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running as administrator
) else (
    echo Please run this installer as administrator
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

REM Set installation directory
set INSTALL_DIR=%APPDATA%\Autodesk\Revit\Autodesk Revit 2025\Addins\ClaudeMCP
echo Creating installation directory: %INSTALL_DIR%

REM Create directory if it doesn't exist
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy files
echo Copying plugin files...
xcopy /E /I /Y "revit_plugin" "%INSTALL_DIR%\revit_plugin"
copy /Y "ClaudeMCP.addin" "%INSTALL_DIR%"
copy /Y "requirements.txt" "%INSTALL_DIR%"
copy /Y "INSTALL.txt" "%INSTALL_DIR%"

REM Install Python dependencies
echo Installing Python dependencies...
cd "%INSTALL_DIR%"
pip install -r requirements.txt

echo.
echo Installation complete!
echo.
echo Please start Revit 2025 to use the plugin.
echo The plugin will appear in the Add-ins tab.
echo.
pause 