# Installation Guide

## Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL or SQLite
- Git

## Step-by-Step Installation

### 1. Clone or Setup Project

Already in: `d:\Projects\Mikrtotik`

### 2. Backend Installation

```powershell
# Navigate to backend
cd d:\Projects\Mikrtotik\enterprise-backend

# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Edit .env - Update if needed
# DATABASE_URL, SECRET_KEY, ADMIN credentials

# Initialize database (creates tables & admin user)
python -c "from app.database import init_db; init_db(); from app.models import User, UserRole; from app.auth import get_password_hash; from sqlalchemy.orm import Session; from app.database import SessionLocal; db = SessionLocal(); admin = db.query(User).filter(User.email == 'admin@mikrotik.local').first(); print('Admin exists' if admin else 'Creating admin...'); db.close()"

# Start backend server
python app/main.py
```

Backend running on: **http://localhost:8000**

### 3. Frontend Installation

```powershell
# New terminal - Navigate to dashboard
cd d:\Projects\Mikrtotik\enterprise-dashboard

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend running on: **http://localhost:3004**

### 4. Access System

1. Open browser: `http://localhost:3004`
2. Login credentials:
   - Email: `admin@mikrotik.local`
   - Password: `Admin123!`

### 5. Add Your MikroTik Router

1. Click "Routers" in sidebar
2. Click "Add Router"
3. Fill in details:

   - **Name**: Main Router (or any name)
   - **Hostname**: `202.84.44.49`
   - **Port**: `22`
   - **Username**: `Admin115`
   - **Password**: `@dminAhL#`
   - **Description**: Production router
   - **Location**: Head Office

4. Click "Save"
5. Router will appear in list

### 6. Collect Metrics

1. Go to router details
2. Click "Collect Metrics"
3. View real-time data

### 7. Enable Auto-Monitoring (Optional)

Run monitoring service in background:

```powershell
cd d:\Projects\Mikrtotik\enterprise-backend
python -m app.monitoring
```

This will:

- Collect metrics every 30 seconds
- Check for alerts every 60 seconds
- Update all active routers

## Configuration

### Environment Variables

Edit `enterprise-backend\.env`:

```env
DATABASE_URL=sqlite:///./mikrotik_enterprise.db
SECRET_KEY=your-secret-key-here
ADMIN_EMAIL=admin@mikrotik.local
ADMIN_PASSWORD=Admin123!
MONITORING_INTERVAL=30
```

### CORS Settings

If frontend runs on different port, update `enterprise-backend\app\config.py`:

```python
CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3004"
```

## Troubleshooting

### Port Already in Use

Backend (8000):

```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process
```

Frontend (3004):

```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 3004).OwningProcess | Stop-Process
```

### Database Errors

Reset database:

```powershell
cd enterprise-backend
del mikrotik_enterprise.db
python -c "from app.database import init_db; init_db()"
```

### Module Not Found

Reinstall dependencies:

```powershell
pip install --upgrade -r requirements.txt
```

## Production Setup

### Using PostgreSQL

1. Install PostgreSQL
2. Create database:

```sql
CREATE DATABASE mikrotik_enterprise;
CREATE USER mikrotik WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE mikrotik_enterprise TO mikrotik;
```

3. Update .env:

```env
DATABASE_URL=postgresql://mikrotik:secure_password@localhost/mikrotik_enterprise
```

### Run as Service (Windows)

Use NSSM or create scheduled tasks:

```powershell
# Install NSSM
# Download from nssm.cc

# Create service
nssm install MikroTikBackend "C:\Path\To\venv\Scripts\python.exe" "C:\Path\To\app\main.py"
nssm start MikroTikBackend
```

## Next Steps

1. Change admin password
2. Create additional users
3. Add all routers
4. Configure alert thresholds
5. Set up email notifications
6. Schedule automated backups

## Support

- API Documentation: http://localhost:8000/docs
- Check logs in terminal for errors
- Ensure routers have SSH enabled on port 22
