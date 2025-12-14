@echo off
REM Simple Windows batch file to build Digital Clock Application
echo Building Digital Clock Application...
echo.

REM Navigate to script directory
cd /d "%~dp0/.."

REM Check for virtual environment
if exist ".venv\Scripts\activate.bat" (
  echo Activating virtual environment...
  call .venv\Scripts\activate.bat
) else if exist "venv\Scripts\activate.bat" (
  echo Activating virtual environment...
  call venv\Scripts\activate.bat
) else (
  echo No virtual environment found, using system Python...
)

REM Install PyInstaller if needed
echo Checking PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
  echo Installing PyInstaller...
  python -m pip install PyInstaller
) else (
  echo PyInstaller already installed
)

REM Clean previous builds
if exist "dist" (
  echo Cleaning dist directory...
  rmdir /s /q dist
)
if exist "build" (
  echo Cleaning build directory...
  rmdir /s /q build
)
if exist "*.spec" (
  echo Cleaning spec files...
  del *.spec
)

REM Build executable
echo.
echo Building executable...
python -m PyInstaller --onefile --windowed --noconsole --add-data "assets;assets" --icon "assets/icon.ico" --name "DigitalClock" --distpath "dist" src/main.py

REM Check if build was successful
if exist "dist\DigitalClock.exe" (
  echo.
  echo Build completed successfully!
  echo Executable location: dist\DigitalClock.exe
  echo.
  
  set /p choice="Run the executable now? (y/N): "
  if /i "%choice%"=="y" (
    start "" "dist\DigitalClock.exe"
  )
) else (
  echo.
  echo Build failed! Check the output above for errors.
  pause
  exit /b 1
)

echo.
echo Build process completed.
pause
