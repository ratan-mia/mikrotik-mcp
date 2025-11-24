# 🌐 MikroTik Enterprise Management System

**Professional-grade router management platform for MikroTik RouterOS devices**

---

## 📚 Documentation Index

### Quick Access

- 🚀 **[Quick Start Guide](QUICKSTART.md)** - Get up and running in 5 minutes
- 📦 **[Installation Guide](INSTALLATION.md)** - Detailed installation instructions
- 📖 **[Complete Documentation](ENTERPRISE_README.md)** - Full system documentation
- 🧪 **[API Testing Guide](API_TESTING.md)** - Test and explore the API
- 📝 **[Project Summary](PROJECT_SUMMARY.md)** - What's included in this system

### 🎯 Getting Started

#### Option 1: Quick Start (Recommended)

```powershell
# Run this command to start everything
cd d:\Projects\Mikrtotik
.\start.ps1
```

Then open: **http://localhost:3004**  
Login: `admin@mikrotik.local` / `Admin123!`

#### Option 2: Manual Setup

See [INSTALLATION.md](INSTALLATION.md) for detailed steps

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────┐
│                  User Browser                        │
│            http://localhost:3004                     │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│          Next.js Frontend Dashboard                  │
│  - Login/Authentication                              │
│  - Router Management UI                              │
│  - Real-time Monitoring                              │
│  - Analytics & Charts                                │
│  - Alert Management                                  │
└────────────────┬────────────────────────────────────┘
                 │ API Calls (REST + WebSocket)
                 ▼
┌─────────────────────────────────────────────────────┐
│           FastAPI Backend Server                     │
│            http://localhost:8000                     │
│  - JWT Authentication                                │
│  - RESTful API Endpoints                             │
│  - WebSocket Alerts                                  │
│  - Background Monitoring                             │
└────────┬──────────────────────────┬─────────────────┘
         │                          │
         │                          ▼
         │              ┌──────────────────────┐
         │              │   SQLite Database    │
         │              │  - Users             │
         │              │  - Routers           │
         │              │  - Metrics           │
         │              │  - Alerts            │
         │              │  - Devices           │
         │              └──────────────────────┘
         │
         ▼ SSH Connection
┌─────────────────────────────────────────────────────┐
│            MikroTik Router(s)                        │
│  - RouterOS 6.x / 7.x                                │
│  - SSH Port 22                                       │
│  - System Resources                                  │
│  - Network Interfaces                                │
│  - Connected Devices                                 │
└─────────────────────────────────────────────────────┘
```

---

## 📦 What's Included

### Backend (`enterprise-backend/`)

- ✅ FastAPI REST API
- ✅ JWT Authentication
- ✅ SQLAlchemy Database
- ✅ MikroTik SSH Client
- ✅ Background Monitoring
- ✅ WebSocket Support
- ✅ Role-based Access Control

### Frontend (`enterprise-dashboard/`)

- ✅ Next.js 15 + React 19
- ✅ Tailwind CSS Styling
- ✅ TypeScript
- ✅ State Management (Zustand)
- ✅ Responsive Design
- ✅ Real-time Updates

### Features

- ✅ Multi-router management
- ✅ Live monitoring (30s intervals)
- ✅ Historical analytics
- ✅ Automated alerts
- ✅ Device tracking
- ✅ Interface statistics
- ✅ User management
- ✅ Audit logging support

---

## 🔑 Default Credentials

**Admin User:**

- Email: `admin@mikrotik.local`
- Password: `Admin123!`

**Your MikroTik Router:**

- Hostname: `202.84.44.49`
- Port: `22`
- Username: `Admin115`
- Password: `@dminAhL#`

---

## 🚀 Quick Commands

### Start Everything

```powershell
.\start.ps1                    # Windows PowerShell
start.bat                      # Windows CMD
```

### Test API

```powershell
.\test-api.ps1                 # Run API tests
```

### Access Points

```
Backend API:    http://localhost:8000
API Docs:       http://localhost:8000/docs
Frontend:       http://localhost:3004
```

### Manual Start

**Backend:**

```powershell
cd enterprise-backend
.\venv\Scripts\Activate.ps1
python app/main.py
```

**Frontend:**

```powershell
cd enterprise-dashboard
npm run dev
```

---

## 📊 Key Features

### 1. Dashboard Overview

- System statistics
- Active routers count
- Connected devices
- Active alerts
- Performance metrics

### 2. Router Management

- Add/edit/delete routers
- Real-time status
- Metric collection
- Device listing
- Interface monitoring

### 3. Monitoring & Analytics

- CPU usage tracking
- Memory utilization
- Network bandwidth
- Connection counts
- Historical data (customizable timeframe)

### 4. Alert System

- Automated alert generation
- Severity levels (Info, Warning, Critical)
- Real-time notifications via WebSocket
- Alert acknowledgment
- Alert history

### 5. User Management

- Role-based access (Admin, Operator, Viewer)
- Secure authentication
- User profiles
- Activity tracking

---

## 🛠️ Technology Stack

| Component          | Technology          |
| ------------------ | ------------------- |
| Backend Framework  | FastAPI             |
| Frontend Framework | Next.js 15          |
| Database           | SQLite / PostgreSQL |
| Authentication     | JWT Tokens          |
| SSH Client         | Paramiko            |
| State Management   | Zustand             |
| Styling            | Tailwind CSS        |
| API Documentation  | OpenAPI (Swagger)   |
| WebSocket          | FastAPI WebSocket   |

---

## 📁 Project Structure

```
d:\Projects\Mikrtotik\
├── enterprise-backend/          # Python FastAPI Backend
│   ├── app/
│   │   ├── main.py             # Application entry
│   │   ├── auth.py             # Authentication
│   │   ├── models.py           # Database models
│   │   ├── mikrotik_service.py # Router client
│   │   ├── monitoring.py       # Background tasks
│   │   └── routers/            # API endpoints
│   ├── requirements.txt
│   └── .env
│
├── enterprise-dashboard/        # Next.js Frontend
│   ├── app/                    # Pages
│   ├── components/             # React components
│   ├── lib/                    # Utilities
│   └── package.json
│
├── QUICKSTART.md               # Quick start guide
├── INSTALLATION.md             # Installation guide
├── ENTERPRISE_README.md        # Full documentation
├── API_TESTING.md              # API testing guide
├── PROJECT_SUMMARY.md          # Project summary
├── start.ps1                   # Startup script
└── test-api.ps1                # API test script
```

---

## 🎯 Common Tasks

### Add a New Router

1. Login to dashboard
2. Navigate to "Routers"
3. Click "Add Router"
4. Enter router details
5. Click "Save"

### Collect Metrics

1. Go to router details
2. Click "Collect Metrics" button
3. View real-time data

### View Analytics

1. Navigate to "Monitoring"
2. Select router
3. Choose time range
4. View charts and graphs

### Manage Alerts

1. Navigate to "Alerts"
2. View active alerts
3. Acknowledge or dismiss
4. Configure thresholds (Settings)

### Create Users

1. Login as Admin
2. Go to "Settings" → "Users"
3. Click "Add User"
4. Assign role
5. Click "Create"

---

## 🔧 Configuration

### Backend Configuration

Edit `enterprise-backend/.env`:

```env
DATABASE_URL=sqlite:///./mikrotik_enterprise.db
SECRET_KEY=your-secret-key
MONITORING_INTERVAL=30
ALERT_CHECK_INTERVAL=60
```

### Frontend Configuration

Edit `enterprise-dashboard/next.config.ts` for API proxy settings

---

## 🐛 Troubleshooting

### Backend won't start

```powershell
# Check if port 8000 is in use
Get-NetTCPConnection -LocalPort 8000

# Stop the process
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force
```

### Frontend won't start

```powershell
# Check if port 3004 is in use
Get-NetTCPConnection -LocalPort 3004

# Clear cache and reinstall
cd enterprise-dashboard
Remove-Item -Recurse -Force node_modules, .next
npm install
```

### Can't connect to router

- Verify SSH is enabled on router
- Check firewall allows SSH (port 22)
- Test: `ssh Admin115@202.84.44.49 -p 22`

### Database errors

```powershell
cd enterprise-backend
.\venv\Scripts\Activate.ps1
python -c "from app.database import init_db; init_db()"
```

---

## 📖 Learning Resources

### API Documentation

- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Code Examples

See [API_TESTING.md](API_TESTING.md) for PowerShell examples

### MikroTik Resources

- RouterOS Manual: https://help.mikrotik.com/
- RouterOS API: https://wiki.mikrotik.com/wiki/Manual:API

---

## 🎉 Next Steps

1. ✅ Start the system (`.\start.ps1`)
2. ✅ Login to dashboard
3. ✅ Add your routers
4. ✅ Collect metrics
5. ✅ Configure monitoring
6. ✅ Set up alerts
7. ✅ Create additional users
8. ✅ Explore features

---

## 📞 Support

- **Documentation**: See files in this directory
- **API Reference**: http://localhost:8000/docs
- **Test API**: Run `.\test-api.ps1`

---

## 📝 License

MIT License - Use freely for personal or commercial projects

---

## 🙏 Credits

Built with:

- FastAPI
- Next.js
- Tailwind CSS
- MikroTik RouterOS
- And many other open-source technologies

---

**Made with ❤️ for Network Administrators**

_Professional router management made simple_
