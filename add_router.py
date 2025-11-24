"""Script to add MikroTik router to the enterprise dashboard"""
import requests
import sys

# Backend URL
BASE_URL = "http://localhost:8001/api/v1"

# Login credentials
LOGIN_DATA = {
    "username": "admin@mikrotik.local",
    "password": "Admin123!"
}

# Router data from .env
ROUTER_DATA = {
    "name": "Main MikroTik Router",
    "hostname": "202.84.44.49",
    "port": 7782,
    "username": "Admin115",
    "password": "@dminAhL#",
    "description": "Primary network router",
    "location": "Main Office",
    "is_active": True
}

def main():
    # Login
    print("🔐 Logging in...")
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        data=LOGIN_DATA,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.text}")
        sys.exit(1)
    
    token = login_response.json()["access_token"]
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    print("✅ Login successful")
    
    # Check if router already exists
    print("\n📡 Checking existing routers...")
    routers_response = requests.get(f"{BASE_URL}/routers", headers=headers)
    existing_routers = routers_response.json()
    
    # Check if router with same hostname exists
    existing = next((r for r in existing_routers if r["hostname"] == ROUTER_DATA["hostname"]), None)
    
    if existing:
        print(f"⚠️  Router already exists: {existing['name']} (ID: {existing['id']})")
        router_id = existing["id"]
    else:
        # Add router
        print("\n➕ Adding new router...")
        add_response = requests.post(
            f"{BASE_URL}/routers",
            json=ROUTER_DATA,
            headers=headers
        )
        
        if add_response.status_code == 201:
            router = add_response.json()
            router_id = router["id"]
            print(f"✅ Router added successfully!")
            print(f"   ID: {router['id']}")
            print(f"   Name: {router['name']}")
            print(f"   Host: {router['hostname']}:{router['port']}")
        else:
            print(f"❌ Failed to add router: {add_response.text}")
            sys.exit(1)
    
    # Test connection to router
    print(f"\n🔌 Testing connection to router (ID: {router_id})...")
    try:
        status_response = requests.get(
            f"{BASE_URL}/routers/{router_id}/status",
            headers=headers,
            timeout=10
        )
        
        if status_response.status_code == 200:
            status = status_response.json()
            print("✅ Connection successful!")
            print(f"   Router OS: {status.get('routeros_version', 'Unknown')}")
            print(f"   Board: {status.get('board_name', 'Unknown')}")
            print(f"   Uptime: {status.get('uptime', 'Unknown')}")
        else:
            print(f"⚠️  Could not get router status: {status_response.text}")
    except Exception as e:
        print(f"⚠️  Connection test failed: {e}")
    
    # Collect initial metrics
    print(f"\n📊 Collecting initial metrics...")
    try:
        collect_response = requests.post(
            f"{BASE_URL}/routers/{router_id}/collect",
            headers=headers,
            timeout=10
        )
        
        if collect_response.status_code == 200:
            print("✅ Metrics collected successfully!")
        else:
            print(f"⚠️  Could not collect metrics: {collect_response.text}")
    except Exception as e:
        print(f"⚠️  Metric collection failed: {e}")
    
    # Show dashboard stats
    print("\n📈 Dashboard Statistics:")
    stats_response = requests.get(f"{BASE_URL}/analytics/dashboard", headers=headers)
    if stats_response.status_code == 200:
        stats = stats_response.json()
        print(f"   Total Routers: {stats['total_routers']}")
        print(f"   Active Routers: {stats['active_routers']}")
        print(f"   Connected Devices: {stats['total_devices']}")
        print(f"   Active Alerts: {stats['active_alerts']}")
        print(f"   Critical Alerts: {stats['critical_alerts']}")
    
    print("\n✨ Setup complete! Visit http://localhost:3004 to view the dashboard")

if __name__ == "__main__":
    main()
