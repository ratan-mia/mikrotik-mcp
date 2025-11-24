# Quick Start Guide

## Fastest Way to Get Started

### Option 1: Using Startup Script (Recommended)

**Windows CMD:**

```cmd
cd d:\Projects\Mikrtotik
start.bat
```

**Windows PowerShell:**

```powershell
cd d:\Projects\Mikrtotik
.\start.ps1
```

This will open two windows:

- Backend API Server (port 8000)
- Frontend Dashboard (port 3004)

### Option 2: Manual Start

**Terminal 1 - Backend:**

```powershell
cd d:\Projects\Mikrtotik\enterprise-backend
.\venv\Scripts\Activate.ps1
python app/main.py
```

**Terminal 2 - Frontend:**

```powershell
cd d:\Projects\Mikrtotik\enterprise-dashboard
npm run dev
```

### Option 3: First Time Setup

If this is your first time:

```powershell
# 1. Install backend dependencies
cd d:\Projects\Mikrtotik\enterprise-backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. Install frontend dependencies
cd ..\enterprise-dashboard
npm install

# 3. Run startup script
cd ..
.\start.ps1
```

## Access the System

1. Open browser: **http://localhost:3004**

2. Login with:

   - Email: `admin@mikrotik.local`
   - Password: `Admin123!`

3. Add your MikroTik router:
   - Click "Routers" → "Add Router"
   - Enter router details
   - Click "Collect Metrics"

## Default Router Configuration

For the existing router (202.84.44.49):

- Name: Production Router
- Hostname: 202.84.44.49
- Port: 22
- Username: Admin115
- Password: @dminAhL#

## URLs

- **Dashboard**: http://localhost:3004
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Interactive API**: http://localhost:8000/redoc

## Common Tasks

### View API Documentation

```
http://localhost:8000/docs
```

### Check Backend Health

```
http://localhost:8000/health
```

### Stop Services

Close the terminal windows or press `Ctrl+C`

### Change Admin Password

1. Login to dashboard
2. Go to Settings → Profile
3. Update password

## Troubleshooting

### Backend won't start

```powershell
# Check if port 8000 is in use
Get-NetTCPConnection -LocalPort 8000

# Kill the process
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process
```

### Frontend won't start

```powershell
# Check if port 3004 is in use
Get-NetTCPConnection -LocalPort 3004

# Kill the process
Get-Process -Id (Get-NetTCPConnection -LocalPort 3004).OwningProcess | Stop-Process
```

### Database errors

```powershell
cd enterprise-backend
.\venv\Scripts\Activate.ps1
python -c "from app.database import init_db; init_db()"
```

## Next Steps

1. ✅ Login to dashboard
2. ✅ Add your routers
3. ✅ Collect metrics
4. ✅ Set up monitoring
5. ✅ Configure alerts
6. ✅ Create additional users

## Support

- Full Documentation: See `ENTERPRISE_README.md`
- Installation Guide: See `INSTALLATION.md`
- API Reference: http://localhost:8000/docs
