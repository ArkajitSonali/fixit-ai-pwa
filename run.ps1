# AI Debugging Support Tool - Startup Script

$ErrorActionPreference = "Stop"

Write-Host "Setting up AI Debugging Support Tool..." -ForegroundColor Cyan

# Ensure we are in the script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Check if Python is installed
if (-not (Get-Command 'python' -ErrorAction SilentlyContinue)) {
    Write-Host "Python is not installed. Please install Python 3.10+ and run this script again." -ForegroundColor Red
    exit 1
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path "backend\venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv backend\venv
}

# Activate virtual environment
$activateScript = "backend\venv\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    . $activateScript
} else {
    Write-Host "Could not find virtual environment activation script." -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r backend\requirements.txt | Out-Null

Write-Host "Setup complete! Starting the server..." -ForegroundColor Green

# Start the uvicorn server serving both backend API and frontend static files
Set-Location backend

Write-Host "
--------------------------------------------------
🚀 Server running at: http://127.0.0.1:8000
Press Ctrl+C to stop the server
--------------------------------------------------
" -ForegroundColor Green

# Use relative imports, host on 127.0.0.1
uvicorn main:app --reload --host 127.0.0.1 --port 8000
