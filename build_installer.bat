@echo off
echo Claude MCP Revit Plugin - Installer Builder
echo ==========================================
echo.

:: Check for Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check for Git (optional)
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo Git is not installed or not in PATH.
    echo It is recommended to install Git from https://git-scm.com/downloads
    echo.
    echo Press any key to continue anyway...
    pause >nul
)

:: Check for NSIS
set NSIS_FOUND=0
if exist "C:\Program Files (x86)\NSIS\makensis.exe" (
    set NSIS_FOUND=1
) else (
    where makensis >nul 2>&1
    if %errorlevel% equ 0 (
        set NSIS_FOUND=1
    )
)

if %NSIS_FOUND% equ 0 (
    echo NSIS is not installed or not in PATH.
    echo Please install NSIS from https://nsis.sourceforge.io/Download
    echo.
    echo Press any key to continue with build only...
    pause >nul
)

:: Install required Python packages
echo Installing required Python packages...
pip install requests

:: Download icons
echo Downloading icons and images...
python create_icons.py

:: Build the plugin files
echo Building plugin files...
python build_plugin.py

:: Check if build succeeded
if not exist "dist\ClaudeMCP" (
    echo Build failed!
    pause
    exit /b 1
)

:: Create installer if NSIS is available
if %NSIS_FOUND% equ 1 (
    echo Creating installer...
    python create_windows_installer.py
    
    if exist "ClaudeMCP_Installer.exe" (
        echo.
        echo Installation package created successfully: ClaudeMCP_Installer.exe
    ) else (
        echo.
        echo Failed to create installer. See errors above.
    )
) else (
    echo.
    echo Skipping installer creation because NSIS is not installed.
    echo.
    echo Files are ready in the dist\ClaudeMCP directory.
    echo You can install them manually by copying to:
    echo %%APPDATA%%\Autodesk\Revit\Addins\2025\ClaudeMCP
)

echo.
echo Build process completed.
echo.
pause 