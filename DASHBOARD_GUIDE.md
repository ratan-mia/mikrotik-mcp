# MikroTik Enterprise Dashboard - Quick Reference

## 🌐 Access URLs

- **Dashboard**: http://localhost:3004
- **Routers Page**: http://localhost:3004/routers
- **Backend API**: http://localhost:8001

## 🔐 Login Credentials

```
Email: admin@mikrotik.local
Password: Admin123!
```

## 📡 Your MikroTik Router

```
Name: Main MikroTik Router
Host: 202.84.44.49
Port: 7782
Username: Admin115
Password: @dminAhL#
Status: ✅ Added to system
```

## 📊 Dashboard Features

### Overview Page (/)

- Total routers count
- Active routers status
- Connected devices
- Active alerts
- System health metrics

### Routers Page (/routers)

- ✅ View all registered routers
- ✅ Add new routers via modal
- ✅ Check router status (RouterOS version, board, uptime, CPU)
- ✅ Collect real-time metrics
- ✅ Monitor router health
- ✅ Access router Web UI
- ✅ Active/inactive status indicators

### Navigation

- Overview - Main dashboard
- Routers - Router management (NEW!)
- Monitoring - Real-time metrics (Coming soon)
- Alerts - Alert management (Coming soon)
- Settings - System settings (Coming soon)

## 🚀 Running the System

### Start Backend

```powershell
# In separate PowerShell window
cd d:\Projects\Mikrtotik\enterprise-backend
d:\Projects\Mikrtotik\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8001
```

### Start Frontend

```powershell
cd d:\Projects\Mikrtotik\enterprise-dashboard
npm run dev
```

### Add Router (Script)

```powershell
cd d:\Projects\Mikrtotik
d:\Projects\Mikrtotik\.venv\Scripts\python.exe add_router.py
```

## 🎯 Router Management Actions

1. **Check Status** - Test SSH connection and get RouterOS info
2. **Collect Metrics** - Gather CPU, memory, bandwidth data
3. **Web UI** - Open router's web interface in new tab

## 📱 Mobile Responsive

The dashboard is fully responsive and works on:

- Desktop (1920px+)
- Laptop (1280px+)
- Tablet (768px+)
- Mobile (375px+)

## 🔧 API Endpoints

- POST `/api/v1/auth/login` - User login
- GET `/api/v1/auth/me` - Current user info
- GET `/api/v1/routers` - List all routers
- POST `/api/v1/routers` - Add new router
- GET `/api/v1/routers/{id}/status` - Get router status
- POST `/api/v1/routers/{id}/collect` - Collect metrics
- GET `/api/v1/analytics/dashboard` - Dashboard stats

## 🎨 UI Components

- **Modern gradient background** (slate-900 → blue-900)
- **Glass-morphism cards** (backdrop-blur-sm)
- **Animated transitions**
- **Icon-based navigation** (Lucide React)
- **Color-coded status** (green=active, slate=inactive)
- **Modal forms** for adding routers

## ✅ Completed Features

- [x] User authentication with JWT
- [x] Email validation (supports .local domains)
- [x] Dashboard overview with stats
- [x] Router management page
- [x] Add router functionality
- [x] Real-time status checking
- [x] Metrics collection
- [x] Responsive navigation
- [x] Auto-refresh capabilities
- [x] Error handling

## 🔜 Next Steps

1. Monitor collected metrics over time
2. Create analytics charts
3. Set up alert rules
4. Add backup scheduling
5. Implement bulk operations
6. Add router configuration templates

---

Last Updated: November 24, 2025
Version: 1.0.0
