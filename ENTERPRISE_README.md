# MikroTik Enterprise Management System

🚀 **Enterprise-level MikroTik Router Management Platform** with real-time monitoring, advanced analytics, multi-user support, and comprehensive automation capabilities.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Features

### Core Capabilities

- **Multi-Router Management** - Manage unlimited MikroTik routers from a single dashboard
- **Real-Time Monitoring** - Live metrics collection with WebSocket updates
- **Advanced Analytics** - Historical data visualization and trend analysis
- **Alert System** - Automated alerts with severity levels and notifications
- **User Management** - Role-based access control (Admin, Operator, Viewer)
- **Audit Logging** - Complete activity tracking for compliance

### Technical Features

- **RESTful API** - FastAPI backend with automatic OpenAPI documentation
- **Database Integration** - SQLAlchemy ORM with SQLite/PostgreSQL support
- **JWT Authentication** - Secure token-based authentication
- **WebSocket Support** - Real-time bidirectional communication
- **Background Tasks** - Automated metric collection and alert checking
- **Responsive UI** - Modern Next.js dashboard with Tailwind CSS

## 📋 System Requirements

### Backend

- Python 3.10 or higher
- 4GB RAM minimum (8GB recommended)
- PostgreSQL 13+ or SQLite
- Redis (optional, for caching)

### Frontend

- Node.js 18+ and npm/yarn
- Modern web browser

### MikroTik Routers

- RouterOS 6.x or 7.x
- SSH access enabled
- User account with appropriate permissions

## 🚀 Quick Start

### 1. Backend Setup

```bash
# Navigate to backend directory
cd enterprise-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env

# Run the server
python app/main.py
```

API: `http://localhost:8000` | Docs: `http://localhost:8000/docs`

### 2. Frontend Setup

```bash
# Navigate to dashboard directory
cd enterprise-dashboard

# Install dependencies
npm install

# Run development server
npm run dev
```

Dashboard: `http://localhost:3004`

### 3. Login & Add Router

Default credentials: `admin@mikrotik.local` / `Admin123!`

## 📁 Architecture

```
enterprise-backend/          # FastAPI Backend
├── app/
│   ├── main.py             # Entry point
│   ├── models.py           # Database models
│   ├── auth.py             # Authentication
│   ├── mikrotik_service.py # SSH client
│   ├── monitoring.py       # Background tasks
│   └── routers/            # API endpoints

enterprise-dashboard/        # Next.js Frontend
├── app/                    # Pages
├── components/             # UI components
└── lib/                    # API & state management
```

## 🔐 Security & Roles

- **JWT Authentication** with bcrypt encryption
- **Admin**: Full system access
- **Operator**: Router management & monitoring
- **Viewer**: Read-only access

## 📊 Key API Endpoints

- `POST /api/v1/auth/login` - Authentication
- `GET /api/v1/routers/` - List routers
- `GET /api/v1/routers/{id}/status` - Router status
- `POST /api/v1/routers/{id}/collect` - Collect metrics
- `GET /api/v1/analytics/dashboard` - Dashboard stats
- `WS /api/v1/alerts/ws` - Real-time alerts

## 🛠️ Production Deployment

```bash
# Backend
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker

# Frontend
npm run build && npm start
```

## 🐛 Troubleshooting

**Cannot connect to router?**

- Check SSH enabled on port 22
- Verify firewall allows SSH
- Test: `ssh admin@router-ip -p 22`

**Database errors?**

- Verify DATABASE_URL
- Run database initialization

## 📝 License

MIT License

---

**Made for Network Administrators** 🌐
