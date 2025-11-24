# MikroTik Enterprise Management System - Startup Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " MikroTik Enterprise Management System" -ForegroundColor Cyan
Write-Host " Starting Backend and Frontend" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start Backend
Write-Host "[1/2] Starting FastAPI Backend..." -ForegroundColor Yellow
Set-Location -Path "enterprise-backend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& {.\venv\Scripts\Activate.ps1; python app/main.py}"
Start-Sleep -Seconds 5

# Start Frontend
Write-Host "[2/2] Starting Next.js Dashboard..." -ForegroundColor Yellow
Set-Location -Path "..\enterprise-dashboard"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& {npm run dev}"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host " Services Starting..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Backend:    http://localhost:8000" -ForegroundColor White
Write-Host "  API Docs:   http://localhost:8000/docs" -ForegroundColor White
Write-Host "  Dashboard:  http://localhost:3004" -ForegroundColor White
Write-Host ""
Write-Host "  Login: admin@mikrotik.local / Admin123!" -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Services running in separate windows." -ForegroundColor Gray
Write-Host "Close those windows to stop services." -ForegroundColor Gray

Set-Location -Path ".."
