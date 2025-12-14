#!/usr/bin/env python3
"""
macOS-specific build script for Digital Clock Application
Creates an .app bundle with proper macOS integration

Usage: python build-macos.py
"""

import os
import sys
import subprocess
import shutil
import plistlib
from pathlib import Path

def print_status(message, color="white"):
  """Print colored status message"""
  colors = {
    "red": "\033[91m",
    "green": "\033[92m", 
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "cyan": "\033[96m",
    "white": "\033[97m"
  }
  print(f"{colors.get(color, colors['white'])}{message}\033[0m")

def run_command(cmd):
  """Run command and return success status"""
  try:
    result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
    return True, result.stdout
  except subprocess.CalledProcessError as e:
    return False, e.stderr

def main():
  """Main build function for macOS"""
  print_status("Building Digital Clock for macOS...", "cyan")

  # Check if running on macOS
  if sys.platform != "darwin":
    print_status("This script is designed for macOS only!", "red")
    sys.exit(1)

  # Navigate to script directory
  script_dir = Path(__file__).parent + "/.."
  os.chdir(script_dir)

  # Check for virtual environment
  venv_python = None
  for venv_path in [".venv", "venv", "env"]:
    python_path = Path(venv_path) / "bin" / "python"
    if python_path.exists():
      venv_python = str(python_path)
      print_status(f"Using virtual environment: {venv_path}", "yellow")
      break

  if not venv_python:
    venv_python = "python3"
    print_status("Using system Python", "yellow")

  # Install PyInstaller
  print_status("Installing PyInstaller...", "yellow")
  success, output = run_command(f"{venv_python} -m pip install PyInstaller")
  if not success:
    print_status(f"Failed to install PyInstaller: {output}", "red")
    sys.exit(1)

  # Clean previous builds
  for path in ["dist", "build", "main.spec"]:
    if os.path.exists(path):
      if os.path.isdir(path):
        shutil.rmtree(path)
      else:
        os.remove(path)
      print_status(f"Cleaned {path}", "yellow")

  # Create .icns file if it doesn't exist
  icon_icns = Path("assets/icon.icns")
  if not icon_icns.exists():
    icon_png = Path("assets/icon.png")
    if icon_png.exists():
      print_status("Converting PNG to ICNS...", "yellow")
      success, _ = run_command(f"sips -s format icns '{icon_png}' --out '{icon_icns}'")
      if not success:
        print_status("Failed to create ICNS, using PNG", "yellow")
        icon_file = "assets/icon.png"
      else:
        icon_file = str(icon_icns)
    else:
      icon_file = None
  else:
    icon_file = str(icon_icns)

  # Build command
  build_cmd = [
    f"{venv_python} -m PyInstaller",
    "--onefile",
    "--windowed",
    "--add-data 'assets:assets'",
    "--name 'Digital Clock'",
    "--osx-bundle-identifier 'com.digitalclock.app'"
  ]

  if icon_file:
    build_cmd.append(f"--icon '{icon_file}'")

  build_cmd.append("src/main.py")

  # Execute build
  print_status("Building macOS app bundle...", "green")
  success, output = run_command(" ".join(build_cmd))

  if not success:
    print_status(f"Build failed: {output}", "red")
    sys.exit(1)

  # Check if app was created
  app_path = Path("dist/Digital Clock.app")
  if app_path.exists():
    print_status("Build completed successfully!", "green")
    print_status(f"App bundle created: {app_path}", "cyan")

    # Create additional Info.plist entries
    plist_path = app_path / "Contents" / "Info.plist"
    if plist_path.exists():
      with open(plist_path, 'rb') as f:
        plist = plistlib.load(f)

      # Add additional metadata
      plist.update({
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'CFBundleDocumentTypes': [],
        'LSUIElement': True,  # Makes it not appear in dock
        'LSBackgroundOnly': False,
        'NSHighResolutionCapable': True
      })

      with open(plist_path, 'wb') as f:
        plistlib.dump(plist, f)

      print_status("Updated app metadata", "green")

    # Ask to run
    try:
      run_app = input("\nRun the app now? (y/N): ").strip().lower()
      if run_app in ['y', 'yes']:
        subprocess.Popen(['open', str(app_path)])
    except KeyboardInterrupt:
      pass

    # Ask to create Applications symlink
    try:
      create_link = input("Create link in Applications folder? (y/N): ").strip().lower()
      if create_link in ['y', 'yes']:
        apps_link = Path("/Applications/Digital Clock.app")
        if apps_link.exists():
          os.remove(apps_link)
        os.symlink(app_path.absolute(), apps_link)
        print_status("Created Applications folder link", "green")
    except (KeyboardInterrupt, OSError) as e:
      if isinstance(e, OSError):
        print_status(f"Failed to create Applications link: {e}", "red")

  else:
    print_status("App bundle not found after build!", "red")
    sys.exit(1)

  print_status("macOS build process completed!", "green")

if __name__ == "__main__":
  main()
