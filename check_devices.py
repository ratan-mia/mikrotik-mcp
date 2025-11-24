#!/usr/bin/env python3
"""Quick script to check active devices on MikroTik router"""

import paramiko
import time

def check_active_devices():
    host = "202.84.44.49"
    port = 7782
    username = "Admin115"
    password = "@dminAhL#"
    
    print(f"Connecting to {host}:{port}...")
    
    try:
        # Create SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect with banner timeout
        ssh.connect(
            hostname=host,
            port=port,
            username=username,
            password=password,
            timeout=30,
            banner_timeout=60,
            auth_timeout=30,
            look_for_keys=False,
            allow_agent=False
        )
        
        print("✓ Connected successfully!\n")
        
        # Get DHCP leases
        print("=" * 80)
        print("DHCP LEASES (Active IP assignments)")
        print("=" * 80)
        stdin, stdout, stderr = ssh.exec_command('/ip dhcp-server lease print detail where status=bound')
        dhcp_output = stdout.read().decode('utf-8', errors='ignore')
        print(dhcp_output)
        
        # Get ARP table
        print("\n" + "=" * 80)
        print("ARP TABLE (Devices on network)")
        print("=" * 80)
        stdin, stdout, stderr = ssh.exec_command('/ip arp print detail')
        arp_output = stdout.read().decode('utf-8', errors='ignore')
        print(arp_output)
        
        # Get interface list
        print("\n" + "=" * 80)
        print("INTERFACE STATUS")
        print("=" * 80)
        stdin, stdout, stderr = ssh.exec_command('/interface print stats')
        interface_output = stdout.read().decode('utf-8', errors='ignore')
        print(interface_output)
        
        # Get wireless registration if available
        print("\n" + "=" * 80)
        print("WIRELESS CLIENTS (if any)")
        print("=" * 80)
        stdin, stdout, stderr = ssh.exec_command('/interface wireless registration-table print detail')
        wireless_output = stdout.read().decode('utf-8', errors='ignore')
        if wireless_output.strip():
            print(wireless_output)
        else:
            print("No wireless interfaces or clients found")
        
        # Close connection
        ssh.close()
        print("\n✓ Connection closed")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_active_devices()
