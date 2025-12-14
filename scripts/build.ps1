# PowerShell script to build Python clock application to executable
Write-Host 'Building Clock Application...' -ForegroundColor Green

# Navigate to script directory
Set-Location $PSScriptRoot\..

# Activate virtual environment if it exists
if (Test-Path '.venv\Scripts\Activate.ps1') {
    Write-Host 'Activating virtual environment...' -ForegroundColor Yellow
    & .\.venv\Scripts\Activate.ps1
} else {
    Write-Host 'Virtual environment not found. Using system Python...' -ForegroundColor Yellow
}

# Install PyInstaller if not already installed
Write-Host 'Checking for PyInstaller...' -ForegroundColor Yellow
try {
    python -c 'import PyInstaller' 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host 'Installing PyInstaller...' -ForegroundColor Yellow
        python -m pip install PyInstaller
    }
} catch {
    Write-Host 'Installing PyInstaller...' -ForegroundColor Yellow
    python -m pip install PyInstaller
}

# Clean previous build
if (Test-Path 'dist') {
    Write-Host 'Cleaning previous build...' -ForegroundColor Yellow
    Remove-Item -Recurse -Force 'dist'
}

if (Test-Path 'build') {
    Write-Host 'Cleaning build cache...' -ForegroundColor Yellow
    Remove-Item -Recurse -Force 'build'
}

if (Test-Path 'clock.spec') {
    Write-Host 'Removing old spec file...' -ForegroundColor Yellow
    Remove-Item 'clock.spec'
}

# Build the executable
Write-Host 'Building executable...' -ForegroundColor Green
python -m PyInstaller `
    --onefile `
    --windowed `
    --noconsole `
    --add-data 'assets;assets' `
    --icon 'assets/icon.ico' `
    --name 'DigitalClock' `
    --distpath 'dist' `
    src/main.py

# Check if build was successful
if (Test-Path 'dist\DigitalClock.exe') {
    Write-Host '
Build completed successfully!' -ForegroundColor Green
    Write-Host 'Executable location: dist\DigitalClock.exe' -ForegroundColor Cyan
    
    # Create a shortcut on desktop (optional)
    $choice = Read-Host '
Create desktop shortcut? (y/N)'
    if ($choice -eq 'y' -or $choice -eq 'Y') {
        $WshShell = New-Object -comObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut("$([Environment]::GetFolderPath('Desktop'))\Digital Clock.lnk")
        $Shortcut.TargetPath = "$PSScriptRoot\dist\DigitalClock.exe"
        $Shortcut.WorkingDirectory = "$PSScriptRoot\dist"
        $Shortcut.IconLocation = "$PSScriptRoot\assets\icon.ico"
        $Shortcut.Description = 'Digital Clock Application'
        $Shortcut.Save()
        Write-Host 'Desktop shortcut created!' -ForegroundColor Green
    }
    
    # Ask if user wants to run the executable
    $run = Read-Host '
Run the executable now? (y/N)'
    if ($run -eq 'y' -or $run -eq 'Y') {
        Start-Process 'dist\DigitalClock.exe'
    }
    
} else {
    Write-Host '
Build failed! Check the output above for errors.' -ForegroundColor Red
    exit 1
}

Write-Host '
Build process completed.' -ForegroundColor Green
