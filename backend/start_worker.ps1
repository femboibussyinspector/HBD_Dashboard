# Start Celery Worker with Windows Compatibility
Write-Host "🚀 Starting Celery Worker for Windows..." -ForegroundColor Cyan

# Check for gevent
$geventInstalled = pip show gevent
if ($geventInstalled) {
    Write-Host "✅ Gevent detected. Starting with -P gevent (High Concurrency)..." -ForegroundColor Green
    celery -A celery_app worker --loglevel=info -P gevent
} else {
    Write-Host "⚠️ Gevent not found. Falling back to -P solo (Stable)..." -ForegroundColor Yellow
    celery -A celery_app worker --loglevel=info -P solo
}
