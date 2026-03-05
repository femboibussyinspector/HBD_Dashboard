# Start Script for GDrive Automation AND Backend Server
# This script opens everything in separate, titled, clean windows

Write-Host "🚀 Starting Everything..." -ForegroundColor Cyan

# 1. Start Celery Worker (Downloads & Processes CSVs)
Write-Host "1. Starting Celery Worker..." -ForegroundColor Green
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", "title Celery Worker; .\venv\Scripts\Activate.ps1; .\start_worker.ps1"

# 2. Start Python Scanner (Scans Google Drive for new files to send to Celery)
Write-Host "2. Starting GDrive Scanner..." -ForegroundColor Green
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", "title GDrive Scanner; .\venv\Scripts\Activate.ps1; python worker_etl.py"

# 3. Start Flask Web API (Runs the Dashboard Backend)
Write-Host "3. Starting Flask API Server..." -ForegroundColor Green
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", "title Flask Server; .\venv\Scripts\Activate.ps1; python app.py --runserver"

Write-Host "✅ All services started in separate windows." -ForegroundColor Yellow
Write-Host "💡 To check status at any time, run: python gdrive_status.py" -ForegroundColor Magenta
