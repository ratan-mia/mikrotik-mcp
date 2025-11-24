#!/usr/bin/env python3
"""Check active devices using RouterOS API"""

import routeros_api

def check_devices_api():
    host = "202.84.44.49"
    port = 7782
    username = "Admin115"
    password = "@dminAhL#"
    
    print(f"Connecting to {host}:{port} via RouterOS API...")
    
    try:
        # Connect to RouterOS
        connection = routeros_api.RouterOsApiPool(
            host,
            username=username,
            password=password,
            port=port,
            plaintext_login=True
        )
        
        api = connection.get_api()
        print("✓ Connected successfully!\n")
        
        # Get DHCP leases
        print("=" * 80)
        print("DHCP LEASES (Active devices)")
        print("=" * 80)
        dhcp_leases = api.get_resource('/ip/dhcp-server/lease')
        leases = dhcp_leases.get()
        
        if leases:
            for i, lease in enumerate(leases, 1):
                print(f"\n{i}. Device:")
                print(f"   MAC Address: {lease.get('mac-address', 'N/A')}")
                print(f"   IP Address:  {lease.get('address', 'N/A')}")
                print(f"   Hostname:    {lease.get('host-name', 'N/A')}")
                print(f"   Status:      {lease.get('status', 'N/A')}")
                print(f"   Server:      {lease.get('server', 'N/A')}")
        else:
            print("No DHCP leases found")
        
        # Get ARP table
        print("\n" + "=" * 80)
        print("ARP TABLE (Devices seen on network)")
        print("=" * 80)
        arp_resource = api.get_resource('/ip/arp')
        arp_entries = arp_resource.get()
        
        if arp_entries:
            for i, entry in enumerate(arp_entries, 1):
                print(f"\n{i}. Device:")
                print(f"   MAC Address: {entry.get('mac-address', 'N/A')}")
                print(f"   IP Address:  {entry.get('address', 'N/A')}")
                print(f"   Interface:   {entry.get('interface', 'N/A')}")
                print(f"   Status:      {entry.get('complete', 'N/A')}")
        else:
            print("No ARP entries found")
        
        # Get interface statistics
        print("\n" + "=" * 80)
        print("INTERFACE STATUS")
        print("=" * 80)
        interface_resource = api.get_resource('/interface')
        interfaces = interface_resource.get()
        
        if interfaces:
            for interface in interfaces:
                if interface.get('running') == 'true':
                    print(f"\n✓ {interface.get('name', 'N/A')}")
                    print(f"   Type:    {interface.get('type', 'N/A')}")
                    print(f"   Running: {interface.get('running', 'N/A')}")
                    print(f"   RX:      {interface.get('rx-byte', '0')} bytes")
                    print(f"   TX:      {interface.get('tx-byte', '0')} bytes")
        else:
            print("No interfaces found")
        
        connection.disconnect()
        print("\n✓ Connection closed")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_devices_api()
