echo off

@REM Navigate to script directory
cd /d "%~dp0\.."

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

@REM Run the application
start cmd /c "python src/main.py"
