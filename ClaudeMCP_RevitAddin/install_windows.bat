@echo off
echo Installing ClaudeMCP Revit Add-in...

set REVIT_ADDINS=%APPDATA%\Autodesk\Revit\Addins\2025
if not exist "%REVIT_ADDINS%" mkdir "%REVIT_ADDINS%"

echo Copying files...
xcopy /Y "ClaudeMCP.addin" "%REVIT_ADDINS%\"
xcopy /Y "bin\Release\ClaudeMCP_RevitAddin.dll" "%REVIT_ADDINS%\"

echo Installation complete!
echo Please restart Revit to use the ClaudeMCP add-in.
pause 