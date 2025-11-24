# MikroTik Dashboard

A modern, responsive web dashboard for managing MikroTik routers built with Next.js 15 and Tailwind CSS.

## Features

- 📊 Real-time system monitoring (CPU, Memory, Uptime, Connections)
- 🖥️ Connected devices overview
- 🔌 Network interface statistics
- 🔥 Firewall status
- 🔄 Auto-refresh capability
- 📱 Fully responsive design
- 🎨 Modern dark theme with glassmorphism effects

## Installation

```bash
cd mikrotik-dashboard
npm install
```

## Configuration

Edit the router configuration in `app/api/router/status/route.ts`:

```typescript
const ROUTER_CONFIG = {
  host: "202.84.44.49",
  port: 22,
  username: "Admin115",
  password: "@dminAhL#",
};
```

## Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Production

```bash
npm run build
npm run start
```

## Features Overview

### Dashboard

- System uptime and version
- CPU and memory usage
- Active connections count
- Interface traffic statistics

### Devices

- List all connected DHCP clients
- IP and MAC addresses
- Device hostnames
- Connection status

### Interfaces

- Network interface status
- Upload/download statistics
- Active/inactive state

### Firewall

- Firewall rules overview
- Security status

## Technologies

- **Next.js 15** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide React** - Beautiful icon library
- **SSH2** - SSH connection to MikroTik router

## License

MIT
