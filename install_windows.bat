@echo off
echo Installing Claude MCP Revit Plugin for Windows...

:: Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Error: This installation requires administrator privileges.
    echo Please right-click on install_windows.bat and select "Run as administrator".
    pause
    exit /b 1
)

:: Create target directories
set REVIT_ADDINS=%APPDATA%\Autodesk\Revit\Addins
set TARGET_DIR=%REVIT_ADDINS%\2025\ClaudeMCP

if not exist "%REVIT_ADDINS%\2025" mkdir "%REVIT_ADDINS%\2025"
if not exist "%TARGET_DIR%" mkdir "%TARGET_DIR%"

:: Copy files to target directory
echo Copying files to %TARGET_DIR%...
xcopy /E /I /Y dist\ClaudeMCP\* "%TARGET_DIR%"
copy ClaudeMCP.addin "%REVIT_ADDINS%\2025\"

:: Install required Python packages
echo Installing required Python packages...
pip install -r requirements.txt

echo.
echo Installation completed successfully.
echo.
echo Next steps:
echo 1. Make sure the Revit Python Shell is installed
echo 2. Start or restart Revit 2025
echo 3. The plugin should appear in the Add-ins tab
echo.

pause 