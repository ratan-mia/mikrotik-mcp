@echo off
echo ========================================
echo  MikroTik Enterprise Management System
echo  Starting Backend and Frontend
echo ========================================
echo.

REM Start Backend
echo [1/2] Starting FastAPI Backend...
cd enterprise-backend
start "MikroTik Backend" cmd /k "venv\Scripts\activate && python app/main.py"
timeout /t 5 /nobreak >nul

REM Start Frontend
echo [2/2] Starting Next.js Dashboard...
cd ..\enterprise-dashboard
start "MikroTik Dashboard" cmd /k "npm run dev"

echo.
echo ========================================
echo  Services Starting...
echo ========================================
echo.
echo  Backend:    http://localhost:8000
echo  API Docs:   http://localhost:8000/docs
echo  Dashboard:  http://localhost:3004
echo.
echo  Login: admin@mikrotik.local / Admin123!
echo.
echo  Press any key to close this window
echo  (Services will continue running)
echo ========================================
pause >nul
