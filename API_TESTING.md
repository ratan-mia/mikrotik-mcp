# API Testing Guide

## Quick API Tests

### Using Browser

1. **Check Backend Health**

```
http://localhost:8000/health
```

2. **View API Documentation**

```
http://localhost:8000/docs
```

3. **Interactive API Testing**

```
http://localhost:8000/redoc
```

### Using PowerShell

#### 1. Health Check

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health"
```

Expected Response:

```json
{ "status": "healthy" }
```

#### 2. Login

```powershell
$body = @{
    username = "admin@mikrotik.local"
    password = "Admin123!"
}
$response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/login" -Method POST -Body $body -ContentType "application/x-www-form-urlencoded"
$token = $response.access_token
```

#### 3. Get Current User

```powershell
$headers = @{
    "Authorization" = "Bearer $token"
}
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/me" -Headers $headers
```

#### 4. List Routers

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/routers/" -Headers $headers
```

#### 5. Get Dashboard Stats

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/analytics/dashboard" -Headers $headers
```

#### 6. List Alerts

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/alerts/" -Headers $headers
```

### Full Test Script

```powershell
# Complete API Test Script

Write-Host "Testing MikroTik Enterprise API..." -ForegroundColor Cyan
Write-Host ""

# 1. Health Check
Write-Host "[1/6] Health Check..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health"
    Write-Host "✓ Status: $($health.status)" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed: $_" -ForegroundColor Red
    exit
}

# 2. Login
Write-Host "[2/6] Authentication..." -ForegroundColor Yellow
try {
    $body = @{
        username = "admin@mikrotik.local"
        password = "Admin123!"
    }
    $auth = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/login" -Method POST -Body $body -ContentType "application/x-www-form-urlencoded"
    $token = $auth.access_token
    Write-Host "✓ Logged in successfully" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed: $_" -ForegroundColor Red
    exit
}

# 3. Get User Info
Write-Host "[3/6] Get Current User..." -ForegroundColor Yellow
try {
    $headers = @{
        "Authorization" = "Bearer $token"
    }
    $user = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/me" -Headers $headers
    Write-Host "✓ User: $($user.username) ($($user.role))" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed: $_" -ForegroundColor Red
}

# 4. Dashboard Stats
Write-Host "[4/6] Dashboard Statistics..." -ForegroundColor Yellow
try {
    $stats = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/analytics/dashboard" -Headers $headers
    Write-Host "✓ Total Routers: $($stats.total_routers)" -ForegroundColor Green
    Write-Host "✓ Active Alerts: $($stats.active_alerts)" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed: $_" -ForegroundColor Red
}

# 5. List Routers
Write-Host "[5/6] List Routers..." -ForegroundColor Yellow
try {
    $routers = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/routers/" -Headers $headers
    Write-Host "✓ Found $($routers.Count) router(s)" -ForegroundColor Green
    foreach ($router in $routers) {
        Write-Host "  - $($router.name) ($($router.hostname):$($router.port))" -ForegroundColor Gray
    }
} catch {
    Write-Host "✗ Failed: $_" -ForegroundColor Red
}

# 6. List Alerts
Write-Host "[6/6] List Alerts..." -ForegroundColor Yellow
try {
    $alerts = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/alerts/" -Headers $headers
    Write-Host "✓ Found $($alerts.Count) alert(s)" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "API Testing Complete!" -ForegroundColor Cyan
```

Save as `test-api.ps1` and run:

```powershell
.\test-api.ps1
```

## Using Swagger UI

1. Open: http://localhost:8000/docs

2. Click "Authorize" button (top right)

3. Login:

   - Username: admin@mikrotik.local
   - Password: Admin123!

4. Copy the access_token

5. Click "Authorize" again and paste token with format:

   ```
   Bearer YOUR_ACCESS_TOKEN
   ```

6. Now you can test all endpoints interactively!

## Common API Workflows

### Workflow 1: Add Router and Collect Metrics

```powershell
# Login
$body = @{
    username = "admin@mikrotik.local"
    password = "Admin123!"
}
$auth = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/login" -Method POST -Body $body -ContentType "application/x-www-form-urlencoded"
$headers = @{
    "Authorization" = "Bearer $($auth.access_token)"
    "Content-Type" = "application/json"
}

# Add Router
$routerData = @{
    name = "Main Router"
    hostname = "202.84.44.49"
    port = 22
    username = "Admin115"
    password = "@dminAhL#"
    description = "Production router"
    location = "Head Office"
    is_active = $true
} | ConvertTo-Json

$router = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/routers/" -Method POST -Headers $headers -Body $routerData

# Collect Metrics
$metrics = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/routers/$($router.id)/collect" -Method POST -Headers $headers

Write-Host "Router added and metrics collected!"
Write-Host "CPU Load: $($metrics.cpu_load)%"
Write-Host "Memory: $($metrics.memory_used)/$($metrics.memory_total) MB"
```

### Workflow 2: Monitor Router Status

```powershell
# Get Router Status
$status = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/routers/1/status" -Headers $headers

Write-Host "Router: $($status.router.name)"
Write-Host "Last Seen: $($status.router.last_seen)"
Write-Host "Active Alerts: $($status.alert_count)"
Write-Host "Connected Devices: $($status.device_count)"

if ($status.latest_metric) {
    Write-Host "Latest CPU: $($status.latest_metric.cpu_load)%"
}
```

### Workflow 3: Get Historical Analytics

```powershell
# Get 24-hour analytics
$analytics = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/analytics/routers/1/history?hours=24" -Headers $headers

Write-Host "Router: $($analytics.router_name)"
Write-Host "Data Points: $($analytics.cpu_usage.Count)"

# Average CPU
$avgCpu = ($analytics.cpu_usage | Measure-Object -Property value -Average).Average
Write-Host "Average CPU: $([math]::Round($avgCpu, 2))%"
```

## Error Responses

### 401 Unauthorized

```json
{ "detail": "Could not validate credentials" }
```

**Solution**: Login again and get a new token

### 403 Forbidden

```json
{ "detail": "Operation not permitted" }
```

**Solution**: User role doesn't have permission

### 404 Not Found

```json
{ "detail": "Router not found" }
```

**Solution**: Check router ID exists

### 500 Internal Server Error

```json
{ "detail": "Failed to collect metrics: Connection timeout" }
```

**Solution**: Check router connectivity

## Performance Testing

### Test Metric Collection Speed

```powershell
$stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
$metrics = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/routers/1/collect" -Method POST -Headers $headers
$stopwatch.Stop()

Write-Host "Metric collection took: $($stopwatch.ElapsedMilliseconds)ms"
```

### Concurrent Requests

```powershell
# Test 10 concurrent dashboard stats requests
$jobs = 1..10 | ForEach-Object {
    Start-Job -ScriptBlock {
        param($token)
        $headers = @{ "Authorization" = "Bearer $token" }
        Invoke-RestMethod -Uri "http://localhost:8000/api/v1/analytics/dashboard" -Headers $headers
    } -ArgumentList $auth.access_token
}

Wait-Job $jobs
$jobs | Receive-Job
$jobs | Remove-Job
```

## WebSocket Testing

### Using JavaScript Console

Open browser console on dashboard and run:

```javascript
const ws = new WebSocket("ws://localhost:8000/api/v1/alerts/ws");

ws.onopen = () => {
  console.log("Connected to alerts WebSocket");
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log("New alert:", data);
};

ws.onerror = (error) => {
  console.error("WebSocket error:", error);
};
```

## Automated Testing

Create `test-automation.ps1`:

```powershell
# Continuous monitoring test
while ($true) {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health"
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    if ($health.status -eq "healthy") {
        Write-Host "[$timestamp] ✓ Backend healthy" -ForegroundColor Green
    } else {
        Write-Host "[$timestamp] ✗ Backend unhealthy" -ForegroundColor Red
    }

    Start-Sleep -Seconds 10
}
```

## Troubleshooting

### Can't connect to API

```powershell
# Check if backend is running
Get-NetTCPConnection -LocalPort 8000
```

### Token expired

```powershell
# Get new token (tokens expire in 30 minutes)
$auth = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/login" -Method POST -Body $body -ContentType "application/x-www-form-urlencoded"
```

### CORS errors

Check that frontend URL is in CORS_ORIGINS in `.env`

---

**For more API details, visit: http://localhost:8000/docs**
