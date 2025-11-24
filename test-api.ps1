# MikroTik Enterprise API Test Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " MikroTik Enterprise API Testing" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$baseUrl = "http://localhost:8000"

# 1. Health Check
Write-Host "[1/6] Testing Health Check..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "$baseUrl/health"
    Write-Host "✓ Status: $($health.status)" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed: Backend not running?" -ForegroundColor Red
    Write-Host "   Start backend first: cd enterprise-backend; python app/main.py" -ForegroundColor Gray
    exit
}

# 2. Login
Write-Host "[2/6] Testing Authentication..." -ForegroundColor Yellow
try {
    $body = @{
        username = "admin@mikrotik.local"
        password = "Admin123!"
    }
    $auth = Invoke-RestMethod -Uri "$baseUrl/api/v1/auth/login" -Method POST -Body $body -ContentType "application/x-www-form-urlencoded"
    $token = $auth.access_token
    Write-Host "✓ Login successful" -ForegroundColor Green
    Write-Host "  Token: $($token.Substring(0, 20))..." -ForegroundColor Gray
} catch {
    Write-Host "✗ Failed: $_" -ForegroundColor Red
    exit
}

# 3. Get User Info
Write-Host "[3/6] Testing User Info..." -ForegroundColor Yellow
try {
    $headers = @{
        "Authorization" = "Bearer $token"
    }
    $user = Invoke-RestMethod -Uri "$baseUrl/api/v1/auth/me" -Headers $headers
    Write-Host "✓ User: $($user.username)" -ForegroundColor Green
    Write-Host "  Role: $($user.role)" -ForegroundColor Gray
    Write-Host "  Email: $($user.email)" -ForegroundColor Gray
} catch {
    Write-Host "✗ Failed: $_" -ForegroundColor Red
}

# 4. Dashboard Stats
Write-Host "[4/6] Testing Dashboard..." -ForegroundColor Yellow
try {
    $stats = Invoke-RestMethod -Uri "$baseUrl/api/v1/analytics/dashboard" -Headers $headers
    Write-Host "✓ Dashboard loaded" -ForegroundColor Green
    Write-Host "  Total Routers: $($stats.total_routers)" -ForegroundColor Gray
    Write-Host "  Active Routers: $($stats.active_routers)" -ForegroundColor Gray
    Write-Host "  Total Devices: $($stats.total_devices)" -ForegroundColor Gray
    Write-Host "  Active Alerts: $($stats.active_alerts)" -ForegroundColor Gray
} catch {
    Write-Host "✗ Failed: $_" -ForegroundColor Red
}

# 5. List Routers
Write-Host "[5/6] Testing Router List..." -ForegroundColor Yellow
try {
    $routers = Invoke-RestMethod -Uri "$baseUrl/api/v1/routers/" -Headers $headers
    Write-Host "✓ Found $($routers.Count) router(s)" -ForegroundColor Green
    if ($routers.Count -gt 0) {
        foreach ($router in $routers) {
            Write-Host "  - $($router.name)" -ForegroundColor Gray
            Write-Host "    $($router.hostname):$($router.port)" -ForegroundColor DarkGray
            Write-Host "    Active: $($router.is_active)" -ForegroundColor DarkGray
        }
    } else {
        Write-Host "  No routers configured yet" -ForegroundColor DarkGray
    }
} catch {
    Write-Host "✗ Failed: $_" -ForegroundColor Red
}

# 6. List Alerts
Write-Host "[6/6] Testing Alerts..." -ForegroundColor Yellow
try {
    $alerts = Invoke-RestMethod -Uri "$baseUrl/api/v1/alerts/" -Headers $headers
    Write-Host "✓ Found $($alerts.Count) alert(s)" -ForegroundColor Green
    if ($alerts.Count -gt 0) {
        foreach ($alert in $alerts[0..2]) {
            $severityColor = switch ($alert.severity) {
                "critical" { "Red" }
                "warning" { "Yellow" }
                default { "Cyan" }
            }
            Write-Host "  - $($alert.title)" -ForegroundColor $severityColor
            Write-Host "    $($alert.message)" -ForegroundColor DarkGray
        }
    } else {
        Write-Host "  No alerts" -ForegroundColor DarkGray
    }
} catch {
    Write-Host "✗ Failed: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Test Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend URL:  $baseUrl" -ForegroundColor White
Write-Host "API Docs:     $baseUrl/docs" -ForegroundColor White
Write-Host "Dashboard:    http://localhost:3004" -ForegroundColor White
Write-Host ""
Write-Host "All tests completed!" -ForegroundColor Green
Write-Host ""
