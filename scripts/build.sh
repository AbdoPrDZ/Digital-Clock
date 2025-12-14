#!/bin/bash
# Bash script to build Python clock application to executable (Linux/macOS)
echo -e "\033[32mBuilding Clock Application...\033[0m"

# Navigate to script directory
cd "$(dirname "$0")\.."

# Check if virtual environment exists and activate it
if [ -f ".venv/bin/activate" ]; then
  echo -e "\033[33mActivating virtual environment...\033[0m"
  source .venv/bin/activate
elif [ -f "venv/bin/activate" ]; then
  echo -e "\033[33mActivating virtual environment...\033[0m"
  source venv/bin/activate
else
  echo -e "\033[33mVirtual environment not found. Using system Python...\033[0m"
fi

# Check Python version
python_version=$(python3 --version 2>/dev/null || python --version 2>/dev/null)
echo -e "\033[36mUsing: $python_version\033[0m"

# Install PyInstaller if not already installed
echo -e "\033[33mChecking for PyInstaller...\033[0m"
if ! python -c "import PyInstaller" 2>/dev/null; then
  echo -e "\033[33mInstalling PyInstaller...\033[0m"
  python -m pip install PyInstaller
fi

# Clean previous build
if [ -d "dist" ]; then
  echo -e "\033[33mCleaning previous build...\033[0m"
  rm -rf dist
fi

if [ -d "build" ]; then
  echo -e "\033[33mCleaning build cache...\033[0m"
  rm -rf build
fi

if [ -f "clock.spec" ]; then
  echo -e "\033[33mRemoving old spec file...\033[0m"
  rm clock.spec
fi

# Build the executable
echo -e "\033[32mBuilding executable...\033[0m"
python -m PyInstaller \
  --onefile \
  --windowed \
  --add-data "assets:assets" \
  --icon "assets/icon.ico" \
  --name "DigitalClock" \
  --distpath "dist" \
  src/main.py

# Check if build was successful
if [ -f "dist/DigitalClock" ]; then
  echo -e "\033[32m\nBuild completed successfully!\033[0m"
  echo -e "\033[36mExecutable location: dist/DigitalClock\033[0m"
  
  # Make executable
  chmod +x dist/DigitalClock

  # Create desktop entry for Linux
  if command -v desktop-file-install >/dev/null 2>&1; then
    read -p $'\nCreate desktop entry? (y/N): ' choice
    if [[ "$choice" =~ ^[Yy]$ ]]; then
      desktop_file="$HOME/.local/share/applications/digital-clock.desktop"
      cat > "$desktop_file" << EOF
[Desktop Entry]
Name=Digital Clock
Comment=Digital Clock Application
Exec=$(pwd)/dist/DigitalClock
Icon=$(pwd)/assets/icon.png
Type=Application
Categories=Utility;Clock;
Terminal=false
EOF
      echo -e "\033[32mDesktop entry created!\033[0m"
    fi
  fi

  # Ask if user wants to run the executable
  read -p $'\nRun the executable now? (y/N): ' run_choice
  if [[ "$run_choice" =~ ^[Yy]$ ]]; then
    ./dist/DigitalClock &
  fi

else
  echo -e "\033[31m\nBuild failed! Check the output above for errors.\033[0m"
  exit 1
fi

echo -e "\033[32m\nBuild process completed.\033[0m"
