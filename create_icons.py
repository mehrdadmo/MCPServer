import os
import sys
import requests
from pathlib import Path

def download_icons():
    """Download icons for the installer"""
    icons_dir = Path("revit_plugin/assets")
    icons_dir.mkdir(parents=True, exist_ok=True)
    
    # URLs for placeholder icons and images
    icon_urls = {
        "icon.ico": "https://github.com/architecture-building-systems/revitpythonshell/raw/master/RevitPythonShell/Resources/python-shell.ico",
        "server_icon.ico": "https://github.com/architecture-building-systems/revitpythonshell/raw/master/RevitPythonShell/Resources/python-shell.ico",
    }
    
    # URLs for placeholder bitmaps
    bitmap_urls = {
        "installer_welcome.bmp": "https://github.com/architecture-building-systems/revitpythonshell/raw/master/RevitPythonShell/Resources/python-shell.ico",
        "installer_header.bmp": "https://github.com/architecture-building-systems/revitpythonshell/raw/master/RevitPythonShell/Resources/python-shell.ico",
    }
    
    # Download icons
    for icon_name, url in icon_urls.items():
        icon_path = icons_dir / icon_name
        if not icon_path.exists():
            print(f"Downloading {icon_name} from {url}")
            try:
                response = requests.get(url)
                response.raise_for_status()
                with open(icon_path, "wb") as f:
                    f.write(response.content)
                print(f"Successfully downloaded {icon_name}")
            except Exception as e:
                print(f"Error downloading {icon_name}: {e}")
                # Create a placeholder file
                with open(icon_path, "w") as f:
                    f.write(f"Placeholder for {icon_name}")
    
    # Download bitmaps
    for bitmap_name, url in bitmap_urls.items():
        bitmap_path = icons_dir / bitmap_name
        if not bitmap_path.exists():
            print(f"Downloading {bitmap_name} from {url}")
            try:
                response = requests.get(url)
                response.raise_for_status()
                with open(bitmap_path, "wb") as f:
                    f.write(response.content)
                print(f"Successfully downloaded {bitmap_name}")
            except Exception as e:
                print(f"Error downloading {bitmap_name}: {e}")
                # Create a placeholder file
                with open(bitmap_path, "w") as f:
                    f.write(f"Placeholder for {bitmap_name}")
    
    print("Icons and images downloaded successfully")

if __name__ == "__main__":
    download_icons() 